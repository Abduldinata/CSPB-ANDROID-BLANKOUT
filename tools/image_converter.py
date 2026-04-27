#!/usr/bin/env python3
"""Standalone image converter for CSPB toolset.

Supports PNG, JPG, BMP, and TGA conversion. BMP can be exported as indexed
8-bit using an adaptive palette.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from .i18n_en import TEXT as TEXT_EN
    from .i18n_id import TEXT as TEXT_ID
except Exception:
    from i18n_en import TEXT as TEXT_EN  # type: ignore
    from i18n_id import TEXT as TEXT_ID  # type: ignore

try:
    from .app_state import append_history, clear_cache, load_json, save_json
except Exception:
    from app_state import append_history, clear_cache, load_json, save_json  # type: ignore

try:
    from PIL import Image, ImageTk  # type: ignore
except Exception:
    Image = None  # type: ignore[assignment]
    ImageTk = None  # type: ignore[assignment]

try:
    from tkinterdnd2 import DND_FILES  # type: ignore
except Exception:
    DND_FILES = None  # type: ignore[assignment]

PIL_AVAILABLE = Image is not None and ImageTk is not None

_FORMAT_MAP = {
    "PNG": "PNG",
    "JPG": "JPEG",
    "JPEG": "JPEG",
    "BMP": "BMP",
    "TGA": "TGA",
}

TEXT_MAP = {"id": TEXT_ID, "en": TEXT_EN}


def _adaptive_palette() -> object:
    if Image is None:
        raise RuntimeError("Pillow is required.")
    palette = getattr(Image, "Palette", None)
    if palette is not None and hasattr(palette, "ADAPTIVE"):
        return palette.ADAPTIVE
    return getattr(Image, "ADAPTIVE", 1)


class ConverterApp:
    def __init__(self, root: tk.Toplevel | tk.Tk, lang: str = "id") -> None:
        self.root = root
        self.lang = lang if lang in TEXT_MAP else "id"
        self.root.title(self._t("converter_title"))
        self.root.geometry("860x560")
        self.root.minsize(860, 560)

        self.input_path_var = tk.StringVar(value="")
        self.output_dir_var = tk.StringVar(value="")
        self.format_var = tk.StringVar(value="PNG")
        self.index8_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value=self._t("converter_ready"))
        self.history_data: list[dict[str, str]] = load_json("converter_history.json", [])
        self.history_var = tk.StringVar(value="")

        self._build_ui()
        self._enable_drop_targets()

    def _t(self, key: str) -> str:
        return TEXT_MAP.get(self.lang, TEXT_ID).get(key, TEXT_ID.get(key, key))

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        scroll_canvas = tk.Canvas(container, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        outer = ttk.Frame(scroll_canvas)
        outer_id = scroll_canvas.create_window((0, 0), window=outer, anchor="nw")

        def on_frame_config(_event: tk.Event) -> None:
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        outer.bind("<Configure>", on_frame_config)

        def on_canvas_resize(_event: tk.Event) -> None:
            canvas_width = scroll_canvas.winfo_width()
            if canvas_width > 1:
                scroll_canvas.itemconfigure(outer_id, width=canvas_width)

        scroll_canvas.bind("<Configure>", on_canvas_resize)

        outer.configure(padding=16)

        header = ttk.Frame(outer)
        header.pack(fill=tk.X)
        ttk.Label(header, text=self._t("converter_title"), font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)

        step1 = ttk.LabelFrame(outer, text=self._t("converter_step1"))
        step1.pack(fill=tk.X, pady=(16, 8))
        ttk.Label(step1, text=self._t("converter_input")).grid(row=0, column=0, sticky="w", padx=8, pady=(10, 2))
        self.input_entry = ttk.Entry(step1, textvariable=self.input_path_var)
        self.input_entry.grid(row=1, column=0, sticky="we", padx=8)
        ttk.Button(step1, text=self._t("converter_browse"), command=self.pick_input).grid(row=1, column=1, padx=8)
        ttk.Label(step1, text=self._t("converter_output")).grid(row=2, column=0, sticky="w", padx=8, pady=(10, 2))
        ttk.Entry(step1, textvariable=self.output_dir_var).grid(row=3, column=0, sticky="we", padx=8, pady=(0, 10))
        ttk.Button(step1, text=self._t("converter_browse"), command=self.pick_output).grid(row=3, column=1, padx=8)
        folder_row = ttk.Frame(step1)
        folder_row.grid(row=4, column=0, columnspan=2, sticky="we", padx=8, pady=(0, 10))
        ttk.Button(folder_row, text=self._t("converter_open_source_folder"), command=self.open_source_folder).pack(side=tk.LEFT)
        ttk.Button(folder_row, text=self._t("open_assets_folder"), command=self.open_image_assets_folder).pack(side=tk.LEFT, padx=(6, 0))
        step1.grid_columnconfigure(0, weight=1)

        step2 = ttk.LabelFrame(outer, text=self._t("converter_step2"))
        step2.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(step2, text=self._t("converter_format")).grid(row=0, column=0, sticky="w", padx=8, pady=(10, 2))
        ttk.Combobox(
            step2,
            values=("PNG", "JPG", "BMP", "TGA"),
            textvariable=self.format_var,
            state="readonly",
            width=12,
        ).grid(row=1, column=0, sticky="w", padx=8)
        ttk.Checkbutton(step2, text=self._t("converter_indexed"), variable=self.index8_var).grid(
            row=2, column=0, sticky="w", padx=8, pady=(8, 10)
        )

        step3 = ttk.LabelFrame(outer, text=self._t("converter_step3"))
        step3.pack(fill=tk.X, pady=(0, 12))
        ttk.Button(step3, text=self._t("converter_convert"), command=self.convert).pack(side=tk.LEFT, padx=8, pady=10)
        ttk.Button(step3, text="Batch Convert", command=self.batch_convert).pack(side=tk.LEFT, padx=8, pady=10)
        ttk.Label(step3, textvariable=self.status_var).pack(side=tk.LEFT, padx=8)

    def batch_convert(self) -> None:
        if Image is None:
            messagebox.showerror(self._t("converter_error"), self._t("converter_pillow_required"))
            return
        file_paths = filedialog.askopenfilenames(
            title="Select images for batch convert",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.tga"), ("All files", "*.*")],
        )
        if not file_paths:
            return
        out_dir = self.output_dir_var.get().strip()
        if not out_dir:
            out_dir = filedialog.askdirectory(title=self._t("converter_select_output"))
            if not out_dir:
                return
            self.output_dir_var.set(out_dir)
        fmt = self.format_var.get().strip().upper()
        fmt = _FORMAT_MAP.get(fmt, fmt)
        indexed8 = bool(self.index8_var.get()) and fmt == "BMP"
        success, failed = 0, 0
        for source in file_paths:
            try:
                with Image.open(source) as img:
                    img.load()
                    work = img.copy()
                work = self._prepare_for_format(work, fmt, indexed8)
                output = Path(out_dir) / f"{Path(source).stem}.{fmt.lower() if fmt != 'JPEG' else 'jpg'}"
                save_format = fmt
                save_kwargs: dict[str, object] = {}
                if fmt == "BMP" and indexed8:
                    save_format = "BMP"
                elif fmt == "JPEG":
                    save_format = "JPEG"
                    save_kwargs.update({"quality": 95, "optimize": True})
                work.save(output, format=save_format, **save_kwargs)
                success += 1
            except Exception as exc:
                failed += 1
        msg = f"Batch convert done. Success: {success}, Failed: {failed}. Output: {out_dir}"
        self.status_var.set(msg)
        messagebox.showinfo(self._t("converter_converted"), msg)

        notes = ttk.LabelFrame(outer, text=self._t("converter_notes"))
        notes.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        ttk.Label(
            notes,
            text=self._t("converter_notes_text"),
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=16, pady=16)

        hist = ttk.LabelFrame(outer, text=self._t("converter_history"))
        hist.pack(fill=tk.X, pady=(0, 0))
        self.history_combo = ttk.Combobox(hist, textvariable=self.history_var, state="readonly")
        self.history_combo.pack(fill=tk.X, padx=8, pady=(8, 4))
        self._refresh_history_combo()

        hist_row = ttk.Frame(hist)
        hist_row.pack(fill=tk.X, padx=8, pady=(0, 8))
        ttk.Button(hist_row, text=self._t("converter_input"), command=self.use_history_source).pack(side=tk.LEFT)
        ttk.Button(hist_row, text=self._t("converter_output"), command=self.use_history_destination).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(hist_row, text=self._t("clear_history"), command=self.clear_history).pack(side=tk.RIGHT)
        ttk.Button(hist_row, text=self._t("clear_cache"), command=self.clear_converter_cache).pack(side=tk.RIGHT, padx=(0, 6))

        scroll_canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(scroll_canvas, e))
        scroll_canvas.bind_all("<Button-4>", lambda e: self._on_mousewheel(scroll_canvas, e))
        scroll_canvas.bind_all("<Button-5>", lambda e: self._on_mousewheel(scroll_canvas, e))

    def _on_mousewheel(self, canvas: tk.Canvas, event: tk.Event) -> None:
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(3, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-3, "units")
        return "break"

    def _runtime_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parent

    def _project_root(self) -> Path:
        start = self._runtime_dir()
        for candidate in (start, *start.parents):
            if (candidate / "files" / "cspb" / "addons" / "neda").exists():
                return candidate
        return start.parent if start.name == "tools" else start

    def _open_folder(self, path: Path) -> None:
        target = path if path.exists() else self._project_root()
        if os.name == "nt":
            os.startfile(str(target))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(target)])
        else:
            subprocess.Popen(["xdg-open", str(target)])

    def open_source_folder(self) -> None:
        source = self.input_path_var.get().strip()
        if source and Path(source).exists():
            self._open_folder(Path(source).resolve().parent)
            return
        self._open_folder(self._runtime_dir())

    def open_image_assets_folder(self) -> None:
        root = self._project_root()
        self._open_folder(root / "files" / "cspb" / "addons" / "neda" / "image")

    def _enable_drop_targets(self) -> None:
        if DND_FILES is None:
            return

        root_drop_register = getattr(self.root, "drop_target_register", None)
        root_dnd_bind = getattr(self.root, "dnd_bind", None)
        if root_drop_register is not None and root_dnd_bind is not None:
            try:
                root_drop_register(DND_FILES)
                root_dnd_bind("<<Drop>>", self._on_file_drop)
            except Exception:
                pass

        entry_drop_register = getattr(self.input_entry, "drop_target_register", None)
        entry_dnd_bind = getattr(self.input_entry, "dnd_bind", None)
        if entry_drop_register is not None and entry_dnd_bind is not None:
            try:
                entry_drop_register(DND_FILES)
                entry_dnd_bind("<<Drop>>", self._on_file_drop)
            except Exception:
                pass

    def _on_file_drop(self, event: tk.Event) -> None:
        data = getattr(event, "data", "")
        if not data:
            return
        try:
            paths = self.root.tk.splitlist(data)
        except Exception:
            paths = (data,)
        if not paths:
            return

        source = str(paths[0]).strip().strip("{}")
        if not source:
            return
        self.input_path_var.set(source)
        if not self.output_dir_var.get().strip():
            self.output_dir_var.set(str(Path(source).parent))

    def _refresh_history_combo(self) -> None:
        if not hasattr(self, "history_combo"):
            return
        values = []
        for item in self.history_data:
            source = item.get("source", "")
            dest = item.get("dest", "")
            when = item.get("time", "")
            values.append(f"{when} | {source} -> {dest}")
        self.history_combo.configure(values=values)

    def _selected_history_item(self) -> dict[str, str] | None:
        idx = self.history_combo.current() if hasattr(self, "history_combo") else -1
        if idx < 0 or idx >= len(self.history_data):
            return None
        return self.history_data[idx]

    def use_history_source(self) -> None:
        item = self._selected_history_item()
        if not item:
            return
        source = item.get("source", "")
        if source:
            self.input_path_var.set(source)

    def use_history_destination(self) -> None:
        item = self._selected_history_item()
        if not item:
            return
        dest = item.get("dest", "")
        if dest:
            self.output_dir_var.set(dest)

    def clear_history(self) -> None:
        self.history_data = []
        save_json("converter_history.json", self.history_data)
        self.history_var.set("")
        self._refresh_history_combo()

    def clear_converter_cache(self) -> None:
        clear_cache()
        self.history_data = []
        self.history_var.set("")
        self._refresh_history_combo()

    def pick_input(self) -> None:
        path = filedialog.askopenfilename(
            title=self._t("converter_select_image"),
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.tga"), ("All files", "*.*")],
        )
        if path:
            self.input_path_var.set(path)
            if not self.output_dir_var.get().strip():
                self.output_dir_var.set(str(Path(path).parent))

    def pick_output(self) -> None:
        path = filedialog.askdirectory(title=self._t("converter_select_output"))
        if path:
            self.output_dir_var.set(path)

    def _prepare_for_format(self, img: Any, fmt: str, indexed8: bool) -> Any:
        if fmt == "JPG":
            return img.convert("RGB") if img.mode != "RGB" else img

        if fmt == "BMP":
            if indexed8:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                return img.convert("P", palette=_adaptive_palette(), colors=256)
            if img.mode not in ("RGB", "RGBA"):
                return img.convert("RGBA") if "A" in img.getbands() else img.convert("RGB")
            return img

        if fmt == "TGA":
            if "A" in img.getbands():
                return img.convert("RGBA")
            return img.convert("RGB") if img.mode != "RGB" else img

        if fmt == "PNG" and img.mode == "P":
            return img.convert("RGBA")

        return img

    def convert(self) -> None:
        source = self.input_path_var.get().strip()
        if not source:
            messagebox.showwarning(self._t("converter_error"), self._t("converter_missing_input"))
            return
        if Image is None:
            messagebox.showerror(self._t("converter_error"), self._t("converter_pillow_required"))
            return

        out_dir = self.output_dir_var.get().strip()
        fmt = self.format_var.get().strip().upper()
        fmt = _FORMAT_MAP.get(fmt, fmt)
        indexed8 = bool(self.index8_var.get()) and fmt == "BMP"

        try:
            with Image.open(source) as img:
                img.load()
                work = img.copy()

            work = self._prepare_for_format(work, fmt, indexed8)

            if out_dir:
                output = Path(out_dir) / f"{Path(source).stem}.{fmt.lower() if fmt != 'JPEG' else 'jpg'}"
            else:
                save_ext = ".jpg" if fmt == "JPEG" else f".{fmt.lower()}"
                save_path = filedialog.asksaveasfilename(
                    title=self._t("converter_save_as"),
                    defaultextension=save_ext,
                    filetypes=[(f"{fmt} file", f"*{save_ext}"), ("All files", "*.*")],
                )
                if not save_path:
                    return
                output = Path(save_path)

            save_format = fmt
            save_kwargs: dict[str, object] = {}
            if fmt == "BMP" and indexed8:
                save_format = "BMP"
            elif fmt == "JPEG":
                save_format = "JPEG"
                save_kwargs.update({"quality": 95, "optimize": True})

            work.save(output, format=save_format, **save_kwargs)

            self.history_data = append_history(
                "converter_history.json",
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": source,
                    "dest": str(output.parent),
                },
                limit=50,
            )
            self._refresh_history_combo()
            if self.history_data:
                self.history_combo.current(0)

            self.status_var.set(f"{self._t('converter_saved')} {output}")
            messagebox.showinfo(self._t("converter_converted"), f"{self._t('converter_saved')} {output}")
        except Exception as exc:
            self.status_var.set(self._t("converter_failed"))
            messagebox.showerror(self._t("converter_error"), str(exc))


def launch_converter(parent: tk.Tk | tk.Toplevel | None = None, lang: str = "id") -> None:
    if parent is None:
        root = tk.Tk()
        ConverterApp(root, lang=lang)
        root.mainloop()
        return

    window = tk.Toplevel(parent)
    ConverterApp(window, lang=lang)


def main() -> None:
    launch_converter(None)


if __name__ == "__main__":
    main()
