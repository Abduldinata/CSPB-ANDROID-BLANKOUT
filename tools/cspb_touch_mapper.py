#!/usr/bin/env python3
"""CSPB Touch Mapper.

Use this tool to open an image, drag a rectangle, and generate
`touch_addbutton` coordinates in CSPB format.

Features:
- Home page with a button to launch the separate image converter tool.
- Open PNG/JPG/BMP/GIF/TGA images if Pillow is installed.
- Right-click drag to define button area.
- Grid overlay and optional grid snapping.
- Palette buttons for outline color.
- Auto-generated touch_addbutton lines.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
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
    from .credits import open_credits
except Exception:
    from app_state import append_history, clear_cache, load_json, save_json  # type: ignore
    from credits import open_credits  # type: ignore

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore
except Exception:
    DND_FILES = None  # type: ignore[assignment]
    TkinterDnD = None  # type: ignore[assignment]

try:
    from PIL import Image, ImageTk  # type: ignore
except Exception:
    Image = None  # type: ignore[assignment]
    ImageTk = None  # type: ignore[assignment]

PIL_AVAILABLE = Image is not None and ImageTk is not None

DEFAULT_TEMPLATE = (
    'touch_addbutton "{name}" "{texture}" "{command}" '
    '{x1:.6f} {y1:.6f} {x2:.6f} {y2:.6f} {r} {g} {b} {a} {rounding}'
)

TEXT_MAP = {"id": TEXT_ID, "en": TEXT_EN}


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CSPB Touch Mapper")
        self.root.geometry("1290x720")
        self.root.minsize(1290, 720)
        self.lang_var = tk.StringVar(value="id")
        self._icon_ref = None

        self.image_path = ""
        self.image_w = 1280
        self.image_h = 720
        self.display_scale = 1.0
        self.display_offset_x = 0
        self.display_offset_y = 0
        self.zoom_fit_mode = True
        self.tk_image = None
        self.pan_drag_start: tuple[int, int] | None = None
        self.pan_drag_origin: tuple[int, int] | None = None

        self.max_overlays = 10
        self.overlay_order: list[str] = []
        self.layer_paths: dict[str, str] = {}
        self.layer_visible: dict[str, bool] = {}
        self.layer_offsets: dict[str, tuple[int, int]] = {}
        self.layer_sizes: dict[str, tuple[int, int]] = {}
        self.layer_opacity: dict[str, int] = {}
        self.layer_names: dict[str, str] = {}
        self.layer_photo_refs: dict[str, object] = {}
        self.layer_item_ids: dict[str, int] = {}
        self.layer_cards: dict[str, dict[str, object]] = {}
        self.layer_collapsed: dict[str, bool] = {}
        self.layer_visible_vars: dict[str, tk.BooleanVar] = {}
        self.layer_opacity_vars: dict[str, tk.IntVar] = {}
        self.layer_scale_vars: dict[str, tk.DoubleVar] = {}
        self.layer_x_vars: dict[str, tk.StringVar] = {}
        self.layer_y_vars: dict[str, tk.StringVar] = {}
        self.layer_x_slider_vars: dict[str, tk.DoubleVar] = {}
        self.layer_y_slider_vars: dict[str, tk.DoubleVar] = {}
        self.base_name_var = tk.StringVar(value="Base")
        self.mapper_history: list[dict[str, str]] = load_json("mapper_history.json", [])
        self.overlay_guide_ids: list[int] = []

        self.drag_start: tuple[int, int] | None = None
        self.drag_rect_id: int | None = None
        self.rect_px = (0, 0, 0, 0)
        self.rect_drag_start: tuple[int, int] | None = None
        self.rect_drag_origin: tuple[int, int, int, int] | None = None
        self.overlay_drag_start: tuple[int, int] | None = None
        self.overlay_drag_origin: tuple[int, int] | None = None

        self.zoom_level_var = tk.DoubleVar(value=1.0)
        self.grid_size_presets = [16, 32, 64, 128, 256]

        self.pages: dict[str, ttk.Frame] = {}
        self.current_page = "home"

        self._build_style()
        self._build_shell()
        self._enable_drop_targets()
        self.set_app_icon()
        self.show_home()

    def _build_style(self) -> None:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")

        style.configure("HomeTitle.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Hero.TButton", font=("Segoe UI", 14, "bold"), padding=(18, 14))
        style.configure("PageHeader.TLabel", font=("Segoe UI", 16, "bold"))

    def _build_shell(self) -> None:
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)

        self._build_home_page()
        self._build_touch_page()

    def _t(self, key: str) -> str:
        lang = self.lang_var.get() if hasattr(self, "lang_var") else "id"
        return TEXT_MAP.get(lang, TEXT_ID).get(key, TEXT_ID.get(key, key))

    def _apply_language(self) -> None:
        self.root.title(self._t("app_title"))
        if hasattr(self, "home_title_label"):
            self.home_title_label.configure(text=self._t("home_title"))
        if hasattr(self, "home_subtitle_label"):
            self.home_subtitle_label.configure(text=self._t("home_subtitle"))
        if hasattr(self, "home_mapper_label"):
            self.home_mapper_label.configure(text=self._t("home_mapper_card"))
        if hasattr(self, "home_converter_label"):
            self.home_converter_label.configure(text=self._t("home_converter_card"))
        if hasattr(self, "home_settings_frame"):
            self.home_settings_frame.configure(text=self._t("home_settings"))
        if hasattr(self, "lang_label"):
            self.lang_label.configure(text=self._t("lang_label"))
        if hasattr(self, "lang_id_radio"):
            self.lang_id_radio.configure(text=self._t("lang_id"))
        if hasattr(self, "lang_en_radio"):
            self.lang_en_radio.configure(text=self._t("lang_en"))
        if hasattr(self, "palette_frame"):
            self.palette_frame.configure(text=self._t("section_palette"))
        if hasattr(self, "layers_frame"):
            self.layers_frame.configure(text=self._t("section_layers"))
        if hasattr(self, "base_frame"):
            self.base_frame.configure(text=self._t("section_base"))
        if hasattr(self, "source_frame"):
            self.source_frame.configure(text=self._t("section_source"))
        if hasattr(self, "touch_mapper_label"):
            self.touch_mapper_label.configure(text=self._t("touch_mapper_label"))
        if hasattr(self, "home_button"):
            self.home_button.configure(text=self._t("home_button"))

    def _on_language_change(self) -> None:
        self._apply_language()
        self._rebuild_touch_page()

    def _rebuild_touch_page(self) -> None:
        page = self.pages.get("touch")
        if page is not None:
            page.destroy()
            del self.pages["touch"]
        self._build_touch_page()
        if self.current_page == "touch":
            self._show_page("touch")

    def _clear_pages(self) -> None:
        for frame in self.pages.values():
            frame.pack_forget()

    def _show_page(self, name: str) -> None:
        self._clear_pages()
        self.pages[name].pack(fill=tk.BOTH, expand=True)
        self.current_page = name

    def show_home(self) -> None:
        self.root.title(f"{self._t('app_title')} - {self._t('home_title')}")
        self._apply_language()
        self._show_page("home")

    def show_touch_mapper(self) -> None:
        self.root.title(f"{self._t('app_title')} - {self._t('home_title')}")
        self._apply_language()
        self._show_page("touch")

    def open_image_converter(self) -> None:
        try:
            import image_converter
        except Exception as exc:
            messagebox.showerror("Converter Error", f"Cannot load image_converter.py\n\n{exc}")
            return
        image_converter.launch_converter(self.root, lang=self.lang_var.get())

    def open_credits_page(self) -> None:
        open_credits(self.root)

    def clear_app_cache(self) -> None:
        clear_cache()
        self.mapper_history = []
        self._refresh_mapper_history_combo()
        messagebox.showinfo(self._t("open_credits"), self._t("cache_cleared"))

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

    def _resource_path(self, *parts: str) -> Path:
        base = Path(getattr(sys, "_MEIPASS", self._runtime_dir())) if getattr(sys, "frozen", False) else self._runtime_dir()
        return base.joinpath(*parts)

    def _open_folder(self, path: Path) -> None:
        target = path if path.exists() else self._project_root()
        import os
        import subprocess
        if os.name == "nt":
            os.startfile(str(target))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(target)])
        else:
            subprocess.Popen(["xdg-open", str(target)])

    def open_image_assets_folder(self) -> None:
        root = self._project_root()
        target = root / "files" / "cspb" / "addons" / "neda" / "image"
        self._open_folder(target)

    def open_cache_folder(self) -> None:
        try:
            from app_state import CACHE_DIR
        except Exception:
            from .app_state import CACHE_DIR  # type: ignore
        
        cache_path = CACHE_DIR
        cache_path.mkdir(parents=True, exist_ok=True)
        
        import os
        import subprocess
        if os.name == 'nt':
            subprocess.Popen(['explorer', str(cache_path)])
        else:
            subprocess.Popen(['open', str(cache_path)])

    def set_app_icon(self) -> None:
        path = self._resource_path("icon.png")

        try:
            icon_img = tk.PhotoImage(file=str(path))
            self.root.iconphoto(True, icon_img)
            self._icon_ref = icon_img
        except Exception:
            return

    def _add_mapper_history(self, kind: str, path: str) -> None:
        if not path:
            return
        entry = {
            "kind": kind,
            "path": path,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.mapper_history = append_history("mapper_history.json", entry, limit=80)
        self._refresh_mapper_history_combo()

    def _refresh_mapper_history_combo(self) -> None:
        if not hasattr(self, "mapper_history_combo"):
            return
        values = [entry.get("path", "") for entry in self.mapper_history if entry.get("path")]
        self.mapper_history_combo.configure(values=values)

    def use_history_as_base(self) -> None:
        path = self.mapper_history_var.get().strip()
        if not path:
            return
        self.image_path = path
        self._add_mapper_history("base", path)
        self._load_image_for_canvas()
        self._add_mapper_history("base", path)

    def use_history_as_overlay(self) -> None:
        path = self.mapper_history_var.get().strip()
        key = self.active_layer_var.get()
        if not path or not key:
            return
        self.layer_paths[key] = path
        self.layer_offsets[key] = (0, 0)
        self.layer_visible[key] = True
        self._load_image_for_canvas()
        self._add_mapper_history("overlay", path)

    def clear_mapper_history(self) -> None:
        self.mapper_history = []
        save_json("mapper_history.json", self.mapper_history)
        self.mapper_history_var.set("")
        self._refresh_mapper_history_combo()

    def _build_home_page(self) -> None:
        page = ttk.Frame(self.container)
        self.pages["home"] = page

        outer = ttk.Frame(page, padding=24)
        outer.pack(fill=tk.BOTH, expand=True)

        self.home_title_label = ttk.Label(outer, text=self._t("home_title"), style="HomeTitle.TLabel")
        self.home_title_label.pack(anchor=tk.W)

        self.home_subtitle_label = ttk.Label(
            outer,
            text=self._t("home_subtitle"),
        )
        self.home_subtitle_label.pack(anchor=tk.W, pady=(6, 18))

        self.home_settings_frame = ttk.LabelFrame(outer, text=self._t("home_settings"))
        self.home_settings_frame.pack(fill=tk.X, pady=(0, 14))
        settings_row = ttk.Frame(self.home_settings_frame, padding=10)
        settings_row.pack(fill=tk.X)
        self.lang_label = ttk.Label(settings_row, text=self._t("lang_label"))
        self.lang_label.pack(side=tk.LEFT)
        self.lang_id_radio = ttk.Radiobutton(settings_row, text=self._t("lang_id"), value="id", variable=self.lang_var, command=self._on_language_change)
        self.lang_id_radio.pack(side=tk.LEFT, padx=(10, 4))
        self.lang_en_radio = ttk.Radiobutton(settings_row, text=self._t("lang_en"), value="en", variable=self.lang_var, command=self._on_language_change)
        self.lang_en_radio.pack(side=tk.LEFT, padx=4)
        ttk.Button(settings_row, text=self._t("open_credits"), command=self.open_credits_page).pack(side=tk.RIGHT, padx=(0, 6))

        hero = ttk.Frame(outer)
        hero.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(hero, text=self._t("home_title"))
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
        self.home_mapper_label = ttk.Label(
            left,
            text=self._t("home_mapper_card"),
            wraplength=360,
        )
        self.home_mapper_label.pack(anchor=tk.W, padx=16, pady=(16, 10))
        ttk.Button(left, text=self._t("open_touch_mapper"), style="Hero.TButton", command=self.show_touch_mapper).pack(
            anchor=tk.W, padx=16, pady=(0, 16)
        )

        right = ttk.LabelFrame(hero, text=self._t("image_converter_title"))
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0))
        self.home_converter_label = ttk.Label(
            right,
            text=self._t("home_converter_card"),
            wraplength=360,
        )
        self.home_converter_label.pack(anchor=tk.W, padx=16, pady=(16, 10))
        ttk.Button(right, text=self._t("open_image_converter"), style="Hero.TButton", command=self.open_image_converter).pack(
            anchor=tk.W, padx=16, pady=(0, 16)
        )

    def _build_touch_page(self) -> None:
        page = ttk.Frame(self.container)
        self.pages["touch"] = page

        header = ttk.Frame(page, padding=(16, 14))
        header.pack(fill=tk.X)
        self.touch_mapper_label = ttk.Label(header, text=self._t("touch_mapper_label"), style="PageHeader.TLabel")
        self.touch_mapper_label.pack(side=tk.LEFT)
        self.home_button = ttk.Button(header, text=self._t("home_button"), command=self.show_home)
        self.home_button.pack(side=tk.RIGHT)
        ttk.Button(header, text=self._t("open_assets_folder"), command=self.open_image_assets_folder).pack(side=tk.RIGHT, padx=(0, 6))

        body = ttk.Frame(page, padding=(16, 0, 16, 16))
        body.pack(fill=tk.BOTH, expand=True)

        workspace = tk.PanedWindow(body, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        workspace.pack(fill=tk.BOTH, expand=True)

        left = ttk.LabelFrame(workspace, text=self._t("canvas_label"))
        left_view = ttk.Frame(left)
        left_view.pack(fill=tk.BOTH, expand=True)
        left_view.grid_columnconfigure(0, weight=1)
        left_view.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(left_view, bg="#1b1b1b", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas_h_scroll = ttk.Scrollbar(left_view, orient=tk.HORIZONTAL, command=self._on_canvas_hscroll)
        self.canvas_h_scroll.grid(row=1, column=0, sticky="ew")
        self.canvas_v_scroll = ttk.Scrollbar(left_view, orient=tk.VERTICAL, command=self._on_canvas_vscroll)
        self.canvas_v_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_pointer_down)
        self.canvas.bind("<B1-Motion>", self._on_pointer_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_pointer_up)
        self.canvas.bind("<ButtonPress-3>", self._on_pointer_down)
        self.canvas.bind("<B3-Motion>", self._on_pointer_drag)
        self.canvas.bind("<ButtonRelease-3>", self._on_pointer_up)
        self.canvas.bind("<ButtonPress-2>", self._on_pointer_down)
        self.canvas.bind("<B2-Motion>", self._on_pointer_drag)
        self.canvas.bind("<ButtonRelease-2>", self._on_pointer_up)
        self.canvas.bind("<MouseWheel>", self._on_canvas_mouse_wheel)
        self.canvas.bind("<Button-4>", self._on_canvas_mouse_wheel)
        self.canvas.bind("<Button-5>", self._on_canvas_mouse_wheel)

        right_shell = ttk.LabelFrame(workspace, text=self._t("touch_generator_label"))
        right = ttk.Frame(right_shell, padding=8)
        right.pack(fill=tk.BOTH, expand=True)

        workspace.add(left, stretch="always", minsize=520)
        workspace.add(right_shell, stretch="never", minsize=360)

        self.base_w_var = tk.StringVar(value="1920")
        self.base_h_var = tk.StringVar(value="1080")
        self.base_source_var = tk.StringVar(value="")
        self.name_prefix_var = tk.StringVar(value="_lobby_notice_")
        self.name_start_index_var = tk.StringVar(value="1")
        self.texture_var = tk.StringVar(value="")
        self.command_var = tk.StringVar(value="")
        self.r_var = tk.StringVar(value="255")
        self.g_var = tk.StringVar(value="255")
        self.b_var = tk.StringVar(value="255")
        self.a_var = tk.StringVar(value="255")
        self.round_var = tk.StringVar(value="6")
        self.info_var = tk.StringVar(value="Rect: -")
        self.name_info_var = tk.StringVar(value="")
        self.auto_base_var = tk.BooleanVar(value=True)
        self.fixed_size_var = tk.BooleanVar(value=True)
        self.button_w_var = tk.StringVar(value="128")
        self.button_h_var = tk.StringVar(value="128")
        self.click_mode_var = tk.StringVar(value="right")
        self.rect_move_mode_var = tk.BooleanVar(value=True)
        self.rect_lock_var = tk.BooleanVar(value=False)
        self.rect_nudge_step_var = tk.StringVar(value="1")
        self.move_layer_mode_var = tk.BooleanVar(value=False)
        self.simple_mode_var = tk.BooleanVar(value=True)
        self.auto_center_scale_var = tk.BooleanVar(value=True)
        self.show_overlay_guides_var = tk.BooleanVar(value=True)
        self.active_layer_var = tk.StringVar(value="")
        self.base_visible_var = tk.BooleanVar(value=True)
        self.grid_visible_var = tk.BooleanVar(value=False)
        self.grid_snap_var = tk.BooleanVar(value=False)
        self.pan_mode_var = tk.BooleanVar(value=False)
        self.show_grid_tools_var = tk.BooleanVar(value=False)
        self.auto_grid_size_var = tk.BooleanVar(value=True)
        self.grid_step_var = tk.StringVar(value="32")
        self.outline_color_var = tk.StringVar(value="#00d5ff")
        self.grid_color_var = tk.StringVar(value="#385060")
        self.export_format_var = tk.StringVar(value="PNG")

        tabs = ttk.Notebook(right)
        tabs.pack(fill=tk.BOTH, expand=True)

        settings_tab = ttk.Frame(tabs, padding=8)
        layers_tab = ttk.Frame(tabs, padding=8)
        render_tab = ttk.Frame(tabs, padding=8)
        tabs.add(settings_tab, text=self._t("tab_settings"))
        tabs.add(layers_tab, text=self._t("tab_layers"))
        tabs.add(render_tab, text=self._t("tab_render"))

        self.palette_frame = ttk.LabelFrame(settings_tab, text=self._t("section_palette"))
        palette = self.palette_frame
        palette.pack(fill=tk.X, pady=(0, 8))
        ttk.Checkbutton(palette, text="Show Grid", variable=self.grid_visible_var, command=self._redraw_canvas).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Checkbutton(palette, text="Snap To Grid", variable=self.grid_snap_var).pack(anchor=tk.W, padx=8, pady=2)
        
        grid_row = ttk.Frame(palette)
        grid_row.pack(fill=tk.X, padx=8, pady=(2, 6))
        ttk.Label(grid_row, text="Grid Size").pack(side=tk.LEFT)
        self.grid_step_combo = ttk.Combobox(grid_row, width=6, textvariable=self.grid_step_var, values=[str(x) for x in self.grid_size_presets], state="readonly")
        self.grid_step_combo.pack(side=tk.LEFT, padx=(6, 6))
        self.grid_step_combo.bind("<<ComboboxSelected>>", lambda e: self._draw_grid())
        ttk.Button(grid_row, text="Custom", width=7, command=self._on_custom_grid_size).pack(side=tk.LEFT)
        
        zoom_row = ttk.Frame(palette)
        zoom_row.pack(fill=tk.X, padx=8, pady=(6, 2))
        ttk.Label(zoom_row, text="Zoom").pack(side=tk.LEFT)
        ttk.Button(zoom_row, text="−", width=3, command=lambda: self._zoom_image(-0.2)).pack(side=tk.LEFT, padx=(6, 2))
        ttk.Button(zoom_row, text="+", width=3, command=lambda: self._zoom_image(0.2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_row, text="Fit", width=4, command=self._zoom_fit).pack(side=tk.LEFT, padx=(2, 6))
        self.zoom_label = ttk.Label(zoom_row, text="100%", width=6)
        self.zoom_label.pack(side=tk.LEFT)
        ttk.Checkbutton(palette, text="Hand Pan (MMB / aktifkan lalu drag L/R)", variable=self.pan_mode_var).pack(anchor=tk.W, padx=8, pady=(2, 6))

        click_row = ttk.Frame(palette)
        click_row.pack(fill=tk.X, padx=8, pady=(2, 2))
        ttk.Label(click_row, text=self._t("drag_click_label")).pack(side=tk.LEFT)
        ttk.Radiobutton(click_row, text=self._t("drag_click_left"), value="left", variable=self.click_mode_var).pack(side=tk.LEFT, padx=(8, 2))
        ttk.Radiobutton(click_row, text=self._t("drag_click_right"), value="right", variable=self.click_mode_var).pack(side=tk.LEFT, padx=2)
        ttk.Checkbutton(palette, text=self._t("fixed_button_label"), variable=self.fixed_size_var, command=self._on_fixed_size_toggle).pack(anchor=tk.W, padx=8, pady=2)
        fixed_size_row = ttk.Frame(palette)
        fixed_size_row.pack(fill=tk.X, padx=8, pady=(2, 8))
        ttk.Entry(fixed_size_row, width=6, textvariable=self.button_w_var).pack(side=tk.LEFT)
        ttk.Label(fixed_size_row, text="x").pack(side=tk.LEFT, padx=(6, 6))
        ttk.Entry(fixed_size_row, width=6, textvariable=self.button_h_var).pack(side=tk.LEFT)

        tools_row = ttk.Frame(settings_tab)
        tools_row.pack(fill=tk.X, pady=(0, 8))
        self.rect_move_check = ttk.Checkbutton(tools_row, text=self._t("move_rect_mode"), variable=self.rect_move_mode_var)
        self.rect_move_check.pack(side=tk.LEFT)
        self.rect_lock_check = ttk.Checkbutton(tools_row, text=self._t("lock_rect_drag"), variable=self.rect_lock_var)
        self.rect_lock_check.pack(side=tk.LEFT, padx=(8, 0))

        nudge_frame = ttk.LabelFrame(settings_tab, text=self._t("rect_nudge_step"))
        nudge_frame.pack(fill=tk.X, pady=(0, 8))
        self.nudge_row = ttk.Frame(nudge_frame, padding=8)
        self.nudge_row.pack(fill=tk.X)
        ttk.Entry(self.nudge_row, width=6, textvariable=self.rect_nudge_step_var).pack(side=tk.LEFT)
        ttk.Button(self.nudge_row, text="<", width=3, command=lambda: self._nudge_rect(-1, 0)).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(self.nudge_row, text=">", width=3, command=lambda: self._nudge_rect(1, 0)).pack(side=tk.LEFT, padx=(4, 0))
        ttk.Button(self.nudge_row, text="^", width=3, command=lambda: self._nudge_rect(0, -1)).pack(side=tk.LEFT, padx=(4, 0))
        ttk.Button(self.nudge_row, text="v", width=3, command=lambda: self._nudge_rect(0, 1)).pack(side=tk.LEFT, padx=(4, 0))

        color_frame = ttk.LabelFrame(settings_tab, text="Outline Color")
        color_frame.pack(fill=tk.X, pady=(0, 8))
        color_row = ttk.Frame(color_frame, padding=8)
        color_row.pack(fill=tk.X)
        for color in ("#00d5ff", "#00ff99", "#ff9900", "#ff66cc", "#ffffff"):
            swatch = tk.Button(
                color_row,
                bg=color,
                activebackground=color,
                width=2,
                height=1,
                relief=tk.FLAT,
                bd=0,
                command=lambda c=color: self._set_outline_color(c),
            )
            swatch.pack(side=tk.LEFT, padx=3)
        ttk.Label(settings_tab, textvariable=self.info_var, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 4))

        self.source_frame = ttk.LabelFrame(settings_tab, text=self._t("section_source"))
        self.source_frame.pack(fill=tk.X, pady=(0, 8))
        source_row = ttk.Frame(self.source_frame)
        source_row.pack(fill=tk.X, padx=8, pady=(8, 8))
        ttk.Label(source_row, text=self._t("base_source_label")).pack(side=tk.LEFT)
        self.base_source_entry = ttk.Entry(source_row, textvariable=self.base_source_var)
        self.base_source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 6))
        ttk.Button(source_row, text=self._t("import_image"), command=self.open_image).pack(side=tk.LEFT)
        ttk.Button(source_row, text=self._t("open_source_folder"), command=self.open_current_image_folder).pack(side=tk.LEFT, padx=(6, 0))
        self.base_source_entry.bind("<Return>", lambda _event: self._load_base_from_entry())

        self.base_frame = ttk.LabelFrame(settings_tab, text=self._t("section_base"))
        base = self.base_frame
        base.pack(fill=tk.X, pady=(0, 8))
        ttk.Checkbutton(base, text=self._t("auto_base_label"), variable=self.auto_base_var, command=self._sync_base_to_image).pack(anchor=tk.W, padx=8, pady=(8, 2))
        ttk.Label(base, text=self._t("custom_base_label")).pack(anchor=tk.W, padx=8, pady=(0, 6))
        base_fields = ttk.Frame(base)
        base_fields.pack(fill=tk.X, padx=8, pady=(0, 8))
        ttk.Label(base_fields, text=self._t("base_w_label")).pack(side=tk.LEFT)
        self.base_w_entry = ttk.Entry(base_fields, width=10, textvariable=self.base_w_var)
        self.base_w_entry.pack(side=tk.LEFT, padx=(6, 12))
        ttk.Label(base_fields, text=self._t("base_h_label")).pack(side=tk.LEFT)
        self.base_h_entry = ttk.Entry(base_fields, width=10, textvariable=self.base_h_var)
        self.base_h_entry.pack(side=tk.LEFT, padx=(6, 0))

        self.layers_frame = ttk.LabelFrame(layers_tab, text=self._t("section_layers"))
        layers = self.layers_frame
        layers.pack(fill=tk.X, pady=(0, 8))

        base_row = ttk.Frame(layers)
        base_row.grid(row=0, column=0, sticky="we", padx=8, pady=(8, 4))
        self.base_name_label = ttk.Label(base_row, textvariable=self.base_name_var)
        self.base_name_label.pack(side=tk.LEFT)
        ttk.Checkbutton(base_row, text=self._t("base_show"), variable=self.base_visible_var, command=self._redraw_canvas).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(base_row, text="Rename", command=self.rename_base).pack(side=tk.RIGHT)
        ttk.Button(base_row, text=self._t("change_source"), command=self.open_image).pack(side=tk.RIGHT, padx=(0, 6))

        overlay_top = ttk.Frame(layers)
        overlay_top.grid(row=1, column=0, sticky="we", padx=8, pady=(0, 6))
        self.add_overlay_btn = ttk.Button(overlay_top, text=self._t("add_overlay"), command=self.add_overlay)
        self.add_overlay_btn.pack(side=tk.LEFT)
        ttk.Checkbutton(overlay_top, text=self._t("auto_center_scale"), variable=self.auto_center_scale_var).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Checkbutton(overlay_top, text=self._t("show_overlay_guides"), variable=self.show_overlay_guides_var).pack(side=tk.LEFT, padx=(8, 0))
        self.move_layer_check = ttk.Checkbutton(overlay_top, text=self._t("move_selected_layer"), variable=self.move_layer_mode_var)
        self.move_layer_check.pack(side=tk.RIGHT)

        self.overlays_list_frame = ttk.Frame(layers)
        self.overlays_list_frame.grid(row=2, column=0, sticky="we", padx=8, pady=(0, 8))

        layers.grid_columnconfigure(0, weight=1)
        self._render_overlay_cards()

        self.history_frame = ttk.LabelFrame(layers_tab, text=self._t("history"))
        self.history_frame.pack(fill=tk.X, pady=(0, 8))
        self.mapper_history_var = tk.StringVar(value="")
        history_values = [entry.get("path", "") for entry in self.mapper_history if entry.get("path")]
        self.mapper_history_combo = ttk.Combobox(self.history_frame, textvariable=self.mapper_history_var, values=history_values, state="readonly")
        self.mapper_history_combo.grid(row=0, column=0, columnspan=3, sticky="we", padx=8, pady=(8, 4))
        ttk.Button(self.history_frame, text=self._t("use_as_base"), command=self.use_history_as_base).grid(row=1, column=0, sticky="we", padx=8, pady=(0, 8))
        ttk.Button(self.history_frame, text=self._t("use_as_overlay"), command=self.use_history_as_overlay).grid(row=1, column=1, sticky="we", padx=8, pady=(0, 8))
        ttk.Button(self.history_frame, text=self._t("clear_history"), command=self.clear_mapper_history).grid(row=1, column=2, sticky="we", padx=8, pady=(0, 8))
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(1, weight=1)
        self.history_frame.grid_columnconfigure(2, weight=1)

        self._update_base_entry_state()

        form = ttk.LabelFrame(render_tab, text=self._t("touch_generator_label"))
        form.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(form, text=self._t("name_prefix_label")).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        prefix_row = ttk.Frame(form)
        prefix_row.grid(row=1, column=0, columnspan=3, sticky="we", padx=8)
        ttk.Entry(prefix_row, width=28, textvariable=self.name_prefix_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(form, text=self._t("texture_label")).grid(row=2, column=0, sticky="w", padx=8, pady=(10, 2))
        ttk.Entry(form, width=34, textvariable=self.texture_var).grid(row=3, column=0, columnspan=3, sticky="we", padx=8)

        ttk.Label(form, text=self._t("command_label")).grid(row=4, column=0, sticky="w", padx=8, pady=(10, 2))
        ttk.Entry(form, width=34, textvariable=self.command_var).grid(row=5, column=0, columnspan=3, sticky="we", padx=8)

        ttk.Label(form, text="RGBA + Round").grid(row=6, column=0, sticky="w", padx=8, pady=(10, 2))
        rgba = ttk.Frame(form)
        rgba.grid(row=7, column=0, columnspan=3, sticky="we", padx=8, pady=(0, 8))
        for i, var in enumerate((self.r_var, self.g_var, self.b_var, self.a_var, self.round_var)):
            ttk.Entry(rgba, width=5, textvariable=var).grid(row=0, column=i, padx=(0, 4))
        form.grid_columnconfigure(0, weight=1)

        actions = ttk.Frame(render_tab)
        actions.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(actions, text="Generate Line", command=self.generate_line).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(actions, text="Append To Batch", command=self.append_batch).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        ttk.Button(actions, text="Copy Output", command=self.copy_output).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        ttk.Button(actions, text="Export Batch .txt", command=self.export_batch).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        render_export = ttk.LabelFrame(render_tab, text="Export Merged Preview")
        render_export.pack(fill=tk.X, pady=(0, 8))
        export_row = ttk.Frame(render_export)
        export_row.pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(export_row, text="Format").pack(side=tk.LEFT)
        ttk.Combobox(export_row, width=8, textvariable=self.export_format_var, state="readonly", values=["PNG", "JPG", "BMP", "TGA"]).pack(side=tk.LEFT, padx=(6, 8))
        ttk.Button(export_row, text="Export Image", command=self.export_merged_preview).pack(side=tk.LEFT)

        outputs = ttk.Frame(render_tab)
        outputs.pack(fill=tk.BOTH, expand=True)
        ttk.Label(outputs, text=self._t("current_output")).pack(anchor=tk.W)
        self.out_text = tk.Text(outputs, height=5, wrap=tk.WORD)
        self.out_text.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(outputs, text=self._t("batch_output")).pack(anchor=tk.W)
        self.batch_text = tk.Text(outputs, height=10, wrap=tk.NONE)
        self.batch_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        self.button_w_var.trace_add("write", lambda *_: self._on_button_size_change())
        self.button_h_var.trace_add("write", lambda *_: self._on_button_size_change())
        self._on_active_layer_change()
        self._update_grid_step_from_button()

    def _set_outline_color(self, color: str) -> None:
        self.outline_color_var.set(color)
        self._redraw_canvas()

    def _bind_mousewheel(self, widget: tk.Widget) -> None:
        yview_scroll = getattr(widget, "yview_scroll", None)

        def _on_mousewheel(event: tk.Event) -> str | None:
            delta = getattr(event, "delta", 0)
            if delta and yview_scroll is not None:
                yview_scroll(int(-1 * (delta / 120)), "units")
                return "break"
            return None

        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", lambda _event: yview_scroll(-1, "units") if yview_scroll is not None else None)
        widget.bind("<Button-5>", lambda _event: yview_scroll(1, "units") if yview_scroll is not None else None)

    def open_image(self) -> None:
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tga"),
            ("All files", "*.*"),
        ]
        initial_dir = self._image_dialog_dir(self.image_path)
        path = filedialog.askopenfilename(title=self._t("open_image"), filetypes=filetypes, initialdir=initial_dir)
        if not path:
            return

        self._set_base_image(path)
        self._load_image_for_canvas(fit_to_canvas=True)

    def _image_dialog_dir(self, current_path: str = "") -> str:
        if current_path and Path(current_path).exists():
            return str(Path(current_path).resolve().parent)
        if self.base_source_var.get().strip() and Path(self.base_source_var.get().strip()).exists():
            return str(Path(self.base_source_var.get().strip()).resolve().parent)
        return str(self._project_root())

    def _set_base_image(self, path: str) -> None:
        self.image_path = path
        self.base_source_var.set(path)

    def _load_base_from_entry(self) -> None:
        path = self.base_source_var.get().strip()
        if not path:
            return
        candidate = Path(path)
        if not candidate.exists():
            messagebox.showwarning("Missing File", "Image source path does not exist.")
            return
        self.image_path = str(candidate)
        self._load_image_for_canvas(fit_to_canvas=True)

    def open_current_image_folder(self) -> None:
        path = self.base_source_var.get().strip() or self.image_path
        if path and Path(path).exists():
            self._open_folder(Path(path).resolve().parent)
            return
        self._open_folder(self._project_root())

    def rename_base(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Rename Base")
        win.transient(self.root)

        name_var = tk.StringVar(value=self.base_name_var.get())
        row = ttk.Frame(win, padding=12)
        row.pack(fill=tk.BOTH, expand=True)
        ttk.Entry(row, textvariable=name_var, width=28).pack(side=tk.LEFT)

        def _apply() -> None:
            value = name_var.get().strip()
            if value:
                self.base_name_var.set(value)
            win.destroy()

        ttk.Button(row, text="OK", command=_apply).pack(side=tk.LEFT, padx=(8, 0))

    def rename_prefix(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Rename Prefix")
        win.transient(self.root)

        name_var = tk.StringVar(value=self.name_prefix_var.get())
        row = ttk.Frame(win, padding=12)
        row.pack(fill=tk.BOTH, expand=True)
        ttk.Entry(row, textvariable=name_var, width=28).pack(side=tk.LEFT)

        def _apply() -> None:
            value = name_var.get().strip()
            if value:
                self.name_prefix_var.set(value)
            win.destroy()

        ttk.Button(row, text="OK", command=_apply).pack(side=tk.LEFT, padx=(8, 0))

    def add_overlay(self) -> None:
        if len(self.overlay_order) >= self.max_overlays:
            messagebox.showinfo("Limit", f"{self._t('max_overlay_limit')} {self.max_overlays} overlays.")
            return

        index = len(self.overlay_order) + 1
        key = f"overlay{index}"
        self.overlay_order.append(key)
        self.layer_paths[key] = ""
        self.layer_visible[key] = True
        self.layer_offsets[key] = (0, 0)
        self.layer_sizes[key] = (0, 0)
        self.layer_opacity[key] = 100
        self.layer_names[key] = f"Overlay-{index}"
        self.layer_visible_vars[key] = tk.BooleanVar(value=True)
        self.layer_opacity_vars[key] = tk.IntVar(value=100)
        self.layer_scale_vars[key] = tk.DoubleVar(value=1.0)
        self.layer_x_vars[key] = tk.StringVar(value="0")
        self.layer_y_vars[key] = tk.StringVar(value="0")
        self.layer_x_slider_vars[key] = tk.DoubleVar(value=0.0)
        self.layer_y_slider_vars[key] = tk.DoubleVar(value=0.0)
        self.layer_collapsed[key] = False

        if not self.active_layer_var.get():
            self.active_layer_var.set(key)

        self._render_overlay_cards()
        self._redraw_canvas()

    def _rename_overlay(self, key: str) -> None:
        win = tk.Toplevel(self.root)
        win.title(self._t("rename_overlay"))
        win.transient(self.root)

        name_var = tk.StringVar(value=self.layer_names.get(key, key))
        row = ttk.Frame(win, padding=12)
        row.pack(fill=tk.BOTH, expand=True)
        ttk.Entry(row, textvariable=name_var, width=28).pack(side=tk.LEFT)

        def _apply() -> None:
            value = name_var.get().strip()
            if value:
                self.layer_names[key] = value
                self._render_overlay_cards()
            win.destroy()

        ttk.Button(row, text="OK", command=_apply).pack(side=tk.LEFT, padx=(8, 0))

    def _render_overlay_cards(self) -> None:
        if not hasattr(self, "overlays_list_frame"):
            return

        for child in self.overlays_list_frame.winfo_children():
            child.destroy()

        for idx, key in enumerate(self.overlay_order, start=1):
            if key not in self.layer_x_slider_vars:
                self.layer_x_slider_vars[key] = tk.DoubleVar(value=float(self.layer_offsets.get(key, (0, 0))[0]))
            if key not in self.layer_y_slider_vars:
                self.layer_y_slider_vars[key] = tk.DoubleVar(value=float(self.layer_offsets.get(key, (0, 0))[1]))

            card = ttk.LabelFrame(self.overlays_list_frame, text=f"{self._t('layer_label')} {idx}")
            card.pack(fill=tk.X, expand=True, pady=(0, 8))

            header = ttk.Frame(card)
            header.pack(fill=tk.X, padx=8, pady=(6, 4))

            ttk.Radiobutton(header, value=key, variable=self.active_layer_var, command=self._on_active_layer_change).pack(side=tk.LEFT)
            ttk.Checkbutton(header, text=self._t("layer_show"), variable=self.layer_visible_vars[key], command=lambda k=key: self._on_layer_visibility_change(k)).pack(side=tk.LEFT)
            ttk.Button(header, text="v", width=3, command=lambda k=key: self.move_overlay_down(k)).pack(side=tk.RIGHT)
            ttk.Button(header, text="^", width=3, command=lambda k=key: self.move_overlay_up(k)).pack(side=tk.RIGHT, padx=(0, 4))
            ttk.Button(header, text=self._t("remove_overlay"), command=lambda k=key: self.remove_overlay(k)).pack(side=tk.RIGHT, padx=(0, 6))
            ttk.Button(
                header,
                text=self._t("expand") if self.layer_collapsed.get(key, False) else self._t("collapse"),
                command=lambda k=key: self.toggle_overlay_card(k),
            ).pack(side=tk.RIGHT, padx=(0, 6))

            if self.layer_collapsed.get(key, False):
                continue

            row1 = ttk.Frame(card)
            row1.pack(fill=tk.X, padx=8, pady=(0, 4))
            ttk.Label(row1, text=self._t("opacity")).pack(side=tk.LEFT)
            ttk.Scale(row1, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.layer_opacity_vars[key], command=lambda v, k=key: self._on_opacity_slider(v, k)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

            if not self.simple_mode_var.get():
                max_range_x = max(1, self.image_w)
                max_range_y = max(1, self.image_h)
                row_xy = ttk.Frame(card)
                row_xy.pack(fill=tk.X, padx=8, pady=(0, 4))
                ttk.Label(row_xy, text=self._t("overlay_x_label")).pack(side=tk.LEFT)
                ttk.Scale(
                    row_xy,
                    from_=-max_range_x,
                    to=max_range_x,
                    orient=tk.HORIZONTAL,
                    variable=self.layer_x_slider_vars[key],
                    command=lambda v, k=key: self._on_offset_slider(v, k, axis="x"),
                ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
                ttk.Label(row_xy, textvariable=self.layer_x_vars[key], width=6).pack(side=tk.LEFT)

                row_xy2 = ttk.Frame(card)
                row_xy2.pack(fill=tk.X, padx=8, pady=(0, 4))
                ttk.Label(row_xy2, text=self._t("overlay_y_label")).pack(side=tk.LEFT)
                ttk.Scale(
                    row_xy2,
                    from_=-max_range_y,
                    to=max_range_y,
                    orient=tk.HORIZONTAL,
                    variable=self.layer_y_slider_vars[key],
                    command=lambda v, k=key: self._on_offset_slider(v, k, axis="y"),
                ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
                ttk.Label(row_xy2, textvariable=self.layer_y_vars[key], width=6).pack(side=tk.LEFT)

                row_scale = ttk.Frame(card)
                row_scale.pack(fill=tk.X, padx=8, pady=(0, 4))
                ttk.Label(row_scale, text=self._t("overlay_scale_label")).pack(side=tk.LEFT)
                ttk.Scale(row_scale, from_=0.1, to=3.0, orient=tk.HORIZONTAL, variable=self.layer_scale_vars[key], command=lambda v, k=key: self._on_scale_slider(v, k)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
                ttk.Button(row_scale, text=self._t("center_overlay"), command=lambda k=key: self.center_overlay(k)).pack(side=tk.LEFT, padx=(0, 4))
                ttk.Button(row_scale, text=self._t("reset_transform"), command=lambda k=key: self.reset_overlay_transform(k)).pack(side=tk.LEFT)

            row2 = ttk.Frame(card)
            row2.pack(fill=tk.X, padx=8, pady=(0, 6))
            ttk.Button(row2, text=self._t("load_button"), command=lambda k=key: self.open_overlay(k)).pack(side=tk.LEFT, fill=tk.X, expand=True)
            ttk.Button(row2, text=self._t("clear_button"), command=lambda k=key: self.clear_overlay(k)).pack(side=tk.LEFT, padx=(6, 0))
            ttk.Button(row2, text=self._t("reset_pos_button"), command=lambda k=key: self.reset_overlay_position(k)).pack(side=tk.LEFT, padx=(6, 0))
            ttk.Button(row2, text=self._t("auto_select_png"), command=lambda k=key: self.auto_select_from_overlay(k)).pack(side=tk.RIGHT)

        if hasattr(self, "add_overlay_btn"):
            self.add_overlay_btn.configure(state=tk.DISABLED if len(self.overlay_order) >= self.max_overlays else tk.NORMAL)

    def move_overlay_up(self, key: str) -> None:
        if key not in self.overlay_order:
            return
        idx = self.overlay_order.index(key)
        if idx <= 0:
            return
        self.overlay_order[idx - 1], self.overlay_order[idx] = self.overlay_order[idx], self.overlay_order[idx - 1]
        self._render_overlay_cards()
        self._redraw_canvas()

    def move_overlay_down(self, key: str) -> None:
        if key not in self.overlay_order:
            return
        idx = self.overlay_order.index(key)
        if idx >= len(self.overlay_order) - 1:
            return
        self.overlay_order[idx + 1], self.overlay_order[idx] = self.overlay_order[idx], self.overlay_order[idx + 1]
        self._render_overlay_cards()
        self._redraw_canvas()

    def toggle_overlay_card(self, key: str) -> None:
        self.layer_collapsed[key] = not self.layer_collapsed.get(key, False)
        self._render_overlay_cards()

    def remove_overlay(self, key: str) -> None:
        if key not in self.overlay_order:
            return
        self.overlay_order.remove(key)
        self.layer_paths.pop(key, None)
        self.layer_visible.pop(key, None)
        self.layer_offsets.pop(key, None)
        self.layer_sizes.pop(key, None)
        self.layer_opacity.pop(key, None)
        self.layer_names.pop(key, None)
        self.layer_photo_refs.pop(key, None)
        self.layer_item_ids.pop(key, None)
        self.layer_visible_vars.pop(key, None)
        self.layer_opacity_vars.pop(key, None)
        self.layer_scale_vars.pop(key, None)
        self.layer_x_vars.pop(key, None)
        self.layer_y_vars.pop(key, None)
        self.layer_x_slider_vars.pop(key, None)
        self.layer_y_slider_vars.pop(key, None)
        self.layer_collapsed.pop(key, None)

        if self.active_layer_var.get() == key:
            self.active_layer_var.set(self.overlay_order[0] if self.overlay_order else "")

        self._render_overlay_cards()
        self._redraw_canvas()

    def open_overlay(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            messagebox.showinfo(self._t("no_overlay_error"), self._t("add_overlay_first"))
            return

        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tga"),
            ("All files", "*.*"),
        ]
        initial_dir = self._image_dialog_dir(self.layer_paths.get(key, ""))
        path = filedialog.askopenfilename(title=self._t("open_image"), filetypes=filetypes, initialdir=initial_dir)
        if not path:
            return
        self.layer_paths[key] = path
        self.layer_offsets[key] = (0, 0)
        self.layer_x_vars[key].set("0")
        self.layer_y_vars[key].set("0")
        self.layer_x_slider_vars[key].set(0.0)
        self.layer_y_slider_vars[key].set(0.0)
        self.layer_scale_vars[key].set(1.0)
        self.layer_visible[key] = self.layer_visible_vars.get(key, tk.BooleanVar(value=True)).get()
        self._add_mapper_history("overlay", path)
        if PIL_AVAILABLE:
            assert Image is not None
            try:
                with Image.open(path) as ov:
                    ov.load()
                    self.layer_sizes[key] = ov.size
            except Exception:
                self.layer_sizes[key] = (0, 0)
        if self.auto_center_scale_var.get():
            self.center_overlay(key)
        else:
            self._load_image_for_canvas()

    def clear_overlay(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            return
        self.layer_paths[key] = ""
        self.layer_offsets[key] = (0, 0)
        if key in self.layer_x_vars:
            self.layer_x_vars[key].set("0")
        if key in self.layer_y_vars:
            self.layer_y_vars[key].set("0")
        if key in self.layer_scale_vars:
            self.layer_scale_vars[key].set(1.0)
        if key in self.layer_x_slider_vars:
            self.layer_x_slider_vars[key].set(0.0)
        if key in self.layer_y_slider_vars:
            self.layer_y_slider_vars[key].set(0.0)
        self.layer_sizes[key] = (0, 0)
        self.layer_photo_refs.pop(key, None)
        self.layer_item_ids.pop(key, None)
        self._load_image_for_canvas()

    def reset_overlay_position(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            return
        if not self.layer_paths.get(key):
            return
        self.layer_offsets[key] = (0, 0)
        if key in self.layer_x_vars:
            self.layer_x_vars[key].set("0")
        if key in self.layer_y_vars:
            self.layer_y_vars[key].set("0")
        if key in self.layer_x_slider_vars:
            self.layer_x_slider_vars[key].set(0.0)
        if key in self.layer_y_slider_vars:
            self.layer_y_slider_vars[key].set(0.0)
        self._load_image_for_canvas()

    def reset_overlay_transform(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            return
        self.layer_scale_vars[key].set(1.0)
        self.layer_offsets[key] = (0, 0)
        self.layer_x_vars[key].set("0")
        self.layer_y_vars[key].set("0")
        self.layer_x_slider_vars[key].set(0.0)
        self.layer_y_slider_vars[key].set(0.0)
        self._load_image_for_canvas()

    def center_overlay(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            return
        ow, oh = self.layer_sizes.get(key, (0, 0))
        if (ow <= 0 or oh <= 0) and self.layer_paths.get(key):
            if PIL_AVAILABLE:
                assert Image is not None
                try:
                    with Image.open(self.layer_paths[key]) as ov:
                        ov.load()
                        ow, oh = ov.size
                        self.layer_sizes[key] = (ow, oh)
                except Exception:
                    return
        if ow <= 0 or oh <= 0:
            return
        scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
        scaled_w = max(1, int(round(ow * scale_factor)))
        scaled_h = max(1, int(round(oh * scale_factor)))
        cx = int(round((self.image_w - scaled_w) / 2))
        cy = int(round((self.image_h - scaled_h) / 2))
        cx, cy = self._clamp_overlay_offset(key, cx, cy)
        self.layer_offsets[key] = (cx, cy)
        self.layer_x_vars[key].set(str(cx))
        self.layer_y_vars[key].set(str(cy))
        self.layer_x_slider_vars[key].set(float(cx))
        self.layer_y_slider_vars[key].set(float(cy))
        self._load_image_for_canvas()

    def _on_active_layer_change(self) -> None:
        key = self.active_layer_var.get()
        if key and key in self.layer_opacity_vars:
            self.layer_opacity_vars[key].set(int(self.layer_opacity.get(key, 100)))
        if key and key in self.layer_scale_vars:
            self.layer_scale_vars[key].set(float(self.layer_scale_vars[key].get()))
        if key and key in self.layer_x_vars and key in self.layer_y_vars:
            ox, oy = self.layer_offsets.get(key, (0, 0))
            self.layer_x_vars[key].set(str(ox))
            self.layer_y_vars[key].set(str(oy))
            if key in self.layer_x_slider_vars:
                self.layer_x_slider_vars[key].set(float(ox))
            if key in self.layer_y_slider_vars:
                self.layer_y_slider_vars[key].set(float(oy))

    def _on_layer_visibility_change(self, key: str | None = None) -> None:
        if key:
            if key in self.layer_visible_vars:
                self.layer_visible[key] = bool(self.layer_visible_vars[key].get())
        else:
            for item in self.overlay_order:
                if item in self.layer_visible_vars:
                    self.layer_visible[item] = bool(self.layer_visible_vars[item].get())
        self._load_image_for_canvas()

    def _on_opacity_slider(self, _value: str, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key or key not in self.layer_opacity_vars:
            return
        self.layer_opacity[key] = int(self.layer_opacity_vars[key].get())
        self._load_image_for_canvas()

    def _on_scale_slider(self, value: str, key: str) -> None:
        try:
            self.layer_scale_vars[key].set(float(value))
        except Exception:
            return
        if self.auto_center_scale_var.get():
            self.center_overlay(key)
        else:
            ox, oy = self.layer_offsets.get(key, (0, 0))
            ox, oy = self._clamp_overlay_offset(key, ox, oy)
            self.layer_offsets[key] = (ox, oy)
            self.layer_x_vars[key].set(str(ox))
            self.layer_y_vars[key].set(str(oy))
            self.layer_x_slider_vars[key].set(float(ox))
            self.layer_y_slider_vars[key].set(float(oy))
            self._load_image_for_canvas()

    def _on_offset_slider(self, value: str, key: str, axis: str) -> None:
        try:
            ivalue = int(round(float(value)))
        except Exception:
            return
        ox, oy = self.layer_offsets.get(key, (0, 0))
        if axis == "x":
            ox = ivalue
        else:
            oy = ivalue
        ox, oy = self._clamp_overlay_offset(key, ox, oy)
        self.layer_offsets[key] = (ox, oy)
        self.layer_x_vars[key].set(str(ox))
        self.layer_y_vars[key].set(str(oy))
        self.layer_x_slider_vars[key].set(float(ox))
        self.layer_y_slider_vars[key].set(float(oy))
        self._load_image_for_canvas()

    def _apply_overlay_transform(self, key: str) -> None:
        try:
            x = int(self.layer_x_vars[key].get())
            y = int(self.layer_y_vars[key].get())
            nx, ny = self._clamp_overlay_offset(key, x, y)
            self.layer_offsets[key] = (nx, ny)
            self.layer_x_vars[key].set(str(nx))
            self.layer_y_vars[key].set(str(ny))
        except ValueError:
            messagebox.showwarning("Invalid XY", "X and Y must be integers.")
            return
        self._load_image_for_canvas()

    def _on_button_size_change(self) -> None:
        self._update_grid_step_from_button()
        self._update_info()

    def auto_select_from_overlay(self, key: str | None = None) -> None:
        key = key or self.active_layer_var.get()
        if not key:
            return
        path = self.layer_paths.get(key, "")
        if not path:
            messagebox.showinfo("No Overlay", "Load selected overlay first.")
            return
        if not PIL_AVAILABLE:
            messagebox.showerror("Pillow Required", "Install Pillow to use auto select from PNG alpha.")
            return

        assert Image is not None
        try:
            with Image.open(path) as ov:
                ov.load()
                rgba = ov.convert("RGBA")
                alpha = rgba.split()[-1]
                bbox = alpha.getbbox()
                if not bbox:
                    messagebox.showinfo("No Pixels", "Overlay has no visible pixels.")
                    return

                ox, oy = self.layer_offsets.get(key, (0, 0))
                scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
                left, top, right, bottom = bbox
                left = ox + int(round(left * scale_factor))
                right = ox + int(round(right * scale_factor))
                top = oy + int(round(top * scale_factor))
                bottom = oy + int(round(bottom * scale_factor))

                left = max(0, min(self.image_w, left))
                top = max(0, min(self.image_h, top))
                right = max(0, min(self.image_w, right))
                bottom = max(0, min(self.image_h, bottom))

                if self.grid_snap_var.get():
                    left = self._snap_value(left)
                    top = self._snap_value(top)
                    right = self._snap_value(right)
                    bottom = self._snap_value(bottom)

                self.rect_px = (left, top, right, bottom)
                self._draw_selection_rect()
                self._update_info()
        except Exception as exc:
            messagebox.showerror("Auto Select Error", str(exc))

    def _enable_drop_targets(self) -> None:
        if DND_FILES is None:
            return
        drop_target_register = getattr(self.root, "drop_target_register", None)
        dnd_bind = getattr(self.root, "dnd_bind", None)
        if drop_target_register is None or dnd_bind is None:
            return

        try:
            drop_target_register(DND_FILES)
            dnd_bind("<<Drop>>", self._on_file_drop)
        except Exception:
            return

        if hasattr(self, "canvas"):
            canvas_drop_register = getattr(self.canvas, "drop_target_register", None)
            canvas_dnd_bind = getattr(self.canvas, "dnd_bind", None)
            if canvas_drop_register is not None and canvas_dnd_bind is not None:
                try:
                    canvas_drop_register(DND_FILES)
                    canvas_dnd_bind("<<Drop>>", self._on_file_drop)
                except Exception:
                    pass

        if hasattr(self, "base_source_entry"):
            entry_drop_register = getattr(self.base_source_entry, "drop_target_register", None)
            entry_dnd_bind = getattr(self.base_source_entry, "dnd_bind", None)
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

        raw_path = str(paths[0]).strip().strip("{}")
        if not raw_path:
            return

        self._set_base_image(raw_path)
        self._load_image_for_canvas()

    def _sync_base_to_image(self) -> None:
        self._update_base_entry_state()
        if self.auto_base_var.get() and self.image_path:
            self.base_w_var.set(str(self.image_w))
            self.base_h_var.set(str(self.image_h))
            self._update_info()

    def _update_base_entry_state(self) -> None:
        state = tk.DISABLED if self.auto_base_var.get() else tk.NORMAL
        if hasattr(self, "base_w_entry"):
            self.base_w_entry.configure(state=state)
        if hasattr(self, "base_h_entry"):
            self.base_h_entry.configure(state=state)

    def _on_fixed_size_toggle(self) -> None:
        self._update_grid_step_from_button()
        self._update_info()

    def _update_grid_step_from_button(self) -> None:
        if self.auto_grid_size_var.get() and self.fixed_size_var.get():
            w, h = self._image_sizes()
            step = max(1, min(w, h))
            self.grid_step_var.set(str(step))
            if hasattr(self, "grid_step_combo") and str(step) in self.grid_step_combo["values"]:
                try:
                    idx = list(self.grid_step_combo["values"]).index(str(step))
                    self.grid_step_combo.current(idx)
                except (ValueError, IndexError):
                    pass

    def _grid_step(self) -> int:
        try:
            step = int(self.grid_step_var.get().strip())
            return max(1, step)
        except Exception:
            return 32

    def _snap_value(self, value: int) -> int:
        if not self.grid_snap_var.get():
            return value
        step = self._grid_step()
        return int(round(value / step) * step)

    def _draw_grid(self) -> None:
        self.canvas.delete("grid")
        if not self.image_path or not self.grid_visible_var.get():
            return

        step = self._grid_step()
        left = self.display_offset_x
        top = self.display_offset_y
        right = left + int(self.image_w * self.display_scale)
        bottom = top + int(self.image_h * self.display_scale)

        for px in range(0, self.image_w + 1, step):
            cx = int(round(px * self.display_scale + self.display_offset_x))
            self.canvas.create_line(cx, top, cx, bottom, fill=self.grid_color_var.get(), width=1, tags=("grid",))

        for py in range(0, self.image_h + 1, step):
            cy = int(round(py * self.display_scale + self.display_offset_y))
            self.canvas.create_line(left, cy, right, cy, fill=self.grid_color_var.get(), width=1, tags=("grid",))

    def _clamp_display_offset(self, ox: float, oy: float) -> tuple[int, int]:
        canvas_w = max(1, self.canvas.winfo_width())
        canvas_h = max(1, self.canvas.winfo_height())
        disp_w = max(1, int(self.image_w * self.display_scale))
        disp_h = max(1, int(self.image_h * self.display_scale))

        if disp_w <= canvas_w:
            min_x = max_x = int((canvas_w - disp_w) / 2)
        else:
            min_x = canvas_w - disp_w
            max_x = 0

        if disp_h <= canvas_h:
            min_y = max_y = int((canvas_h - disp_h) / 2)
        else:
            min_y = canvas_h - disp_h
            max_y = 0

        nx = int(max(min_x, min(max_x, int(round(ox)))))
        ny = int(max(min_y, min(max_y, int(round(oy)))))
        return nx, ny

    def _update_pan_scrollbars(self) -> None:
        if not hasattr(self, "canvas_h_scroll") or not hasattr(self, "canvas_v_scroll"):
            return
        if not self.image_path:
            self.canvas_h_scroll.set(0.0, 1.0)
            self.canvas_v_scroll.set(0.0, 1.0)
            return

        canvas_w = max(1, self.canvas.winfo_width())
        canvas_h = max(1, self.canvas.winfo_height())
        disp_w = max(1, int(self.image_w * self.display_scale))
        disp_h = max(1, int(self.image_h * self.display_scale))

        if disp_w <= canvas_w:
            self.canvas_h_scroll.set(0.0, 1.0)
        else:
            first_x = max(0.0, min(1.0, -self.display_offset_x / disp_w))
            last_x = max(first_x, min(1.0, first_x + (canvas_w / disp_w)))
            self.canvas_h_scroll.set(first_x, last_x)

        if disp_h <= canvas_h:
            self.canvas_v_scroll.set(0.0, 1.0)
        else:
            first_y = max(0.0, min(1.0, -self.display_offset_y / disp_h))
            last_y = max(first_y, min(1.0, first_y + (canvas_h / disp_h)))
            self.canvas_v_scroll.set(first_y, last_y)

    def _set_display_offset(self, ox: float, oy: float, redraw: bool = False) -> None:
        if not self.image_path:
            return
        nx, ny = self._clamp_display_offset(ox, oy)
        dx = nx - self.display_offset_x
        dy = ny - self.display_offset_y
        if dx == 0 and dy == 0:
            return
        self.display_offset_x = nx
        self.display_offset_y = ny
        if redraw:
            self._redraw_canvas()
            return
        self.canvas.move("all", dx, dy)
        self._update_pan_scrollbars()

    def _on_canvas_hscroll(self, *args: str) -> None:
        if not self.image_path:
            return
        disp_w = max(1, int(self.image_w * self.display_scale))
        canvas_w = max(1, self.canvas.winfo_width())
        if disp_w <= canvas_w:
            return

        if args and args[0] == "moveto" and len(args) >= 2:
            frac = max(0.0, min(1.0, float(args[1])))
            target_x = -int(round(frac * disp_w))
            self._set_display_offset(target_x, self.display_offset_y, redraw=False)
            return

        if args and args[0] == "scroll" and len(args) >= 3:
            amount = int(args[1])
            unit = args[2]
            step = max(20, int(canvas_w * (0.9 if unit == "pages" else 0.08)))
            self._set_display_offset(self.display_offset_x - (amount * step), self.display_offset_y, redraw=False)

    def _on_canvas_vscroll(self, *args: str) -> None:
        if not self.image_path:
            return
        disp_h = max(1, int(self.image_h * self.display_scale))
        canvas_h = max(1, self.canvas.winfo_height())
        if disp_h <= canvas_h:
            return

        if args and args[0] == "moveto" and len(args) >= 2:
            frac = max(0.0, min(1.0, float(args[1])))
            target_y = -int(round(frac * disp_h))
            self._set_display_offset(self.display_offset_x, target_y, redraw=False)
            return

        if args and args[0] == "scroll" and len(args) >= 3:
            amount = int(args[1])
            unit = args[2]
            step = max(20, int(canvas_h * (0.9 if unit == "pages" else 0.08)))
            self._set_display_offset(self.display_offset_x, self.display_offset_y - (amount * step), redraw=False)

    def _redraw_canvas(self) -> None:
        if self.image_path:
            self._load_image_for_canvas(fit_to_canvas=False)

    def _on_custom_grid_size(self) -> None:
        """Open dialog to set custom grid size."""
        from tkinter import simpledialog
        try:
            current = int(self.grid_step_var.get())
        except (ValueError, AttributeError):
            current = 32
        value = simpledialog.askinteger("Grid Size", "Enter custom grid size (1-256):", initialvalue=current)
        if value and 1 <= value <= 256:
            self.grid_step_var.set(str(value))
            self._draw_grid()

    def _zoom_image(self, delta: float) -> None:
        """Zoom image by delta amount."""
        if not self.image_path:
            return
        
        new_scale = self.display_scale + delta
        if new_scale < 0.2:
            new_scale = 0.2
        elif new_scale > 3.0:
            new_scale = 3.0
        
        if new_scale == self.display_scale:
            return

        self.zoom_fit_mode = False
        
        # Zoom towards center of canvas
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        canvas_cx = canvas_w / 2
        canvas_cy = canvas_h / 2
        
        # Convert canvas center to image coordinates
        img_px, img_py = self._canvas_to_image_px(canvas_cx, canvas_cy)
        
        # Update scale
        self.display_scale = new_scale
        
        # Recalculate display offset to keep same image point in center
        self.display_offset_x = canvas_cx - img_px * self.display_scale
        self.display_offset_y = canvas_cy - img_py * self.display_scale
        
        self.zoom_level_var.set(new_scale)
        self._update_zoom_label()
        self._redraw_canvas()

    def _zoom_fit(self) -> None:
        """Fit entire image in canvas."""
        if not self.image_path:
            return

        self.zoom_fit_mode = True
        
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        if canvas_w <= 1 or canvas_h <= 1:
            self.display_scale = 1.0
            self.display_offset_x = 0
            self.display_offset_y = 0
        else:
            scale_x = canvas_w / self.image_w
            scale_y = canvas_h / self.image_h
            self.display_scale = min(scale_x, scale_y)
            if self.display_scale < 0.2:
                self.display_scale = 0.2
            
            img_w_disp = int(self.image_w * self.display_scale)
            img_h_disp = int(self.image_h * self.display_scale)
            self.display_offset_x = max(0, (canvas_w - img_w_disp) / 2)
            self.display_offset_y = max(0, (canvas_h - img_h_disp) / 2)
        
        self.zoom_level_var.set(self.display_scale)
        self._update_zoom_label()
        self._redraw_canvas()

    def _update_zoom_label(self) -> None:
        """Update zoom percentage label."""
        if hasattr(self, "zoom_label"):
            zoom_pct = int(self.zoom_level_var.get() * 100)
            self.zoom_label.configure(text=f"{zoom_pct}%")

    def _on_canvas_mouse_wheel(self, event: tk.Event) -> None:
        """Handle mouse wheel zoom (Ctrl+Wheel)."""
        try:
            state = int(event.state)
        except (ValueError, TypeError):
            return
        
        if state & 0x4 == 0:  # Ctrl not pressed
            return
        
        if event.num == 5 or event.delta < 0:
            self._zoom_image(-0.1)
        else:
            self._zoom_image(0.1)

    def _image_sizes(self) -> tuple[int, int]:
        try:
            width = max(1, int(self.button_w_var.get().strip()))
            height = max(1, int(self.button_h_var.get().strip()))
            return width, height
        except Exception:
            return 128, 128

    def _draw_selection_rect(self) -> None:
        left, top, right, bottom = self.rect_px
        c1x, c1y = self._image_px_to_canvas(left, top)
        c2x, c2y = self._image_px_to_canvas(right, bottom)

        if self.drag_rect_id is None:
            self.drag_rect_id = self.canvas.create_rectangle(
                c1x, c1y, c2x, c2y, outline=self.outline_color_var.get(), width=2
            )
        else:
            self.canvas.coords(self.drag_rect_id, c1x, c1y, c2x, c2y)
            self.canvas.itemconfigure(self.drag_rect_id, outline=self.outline_color_var.get())

    def _clamp_overlay_offset(self, key: str, x: int, y: int) -> tuple[int, int]:
        ow, oh = self.layer_sizes.get(key, (0, 0))
        if ow <= 0 or oh <= 0:
            return 0, 0
        scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
        scaled_w = max(1, int(round(ow * scale_factor)))
        scaled_h = max(1, int(round(oh * scale_factor)))
        min_x = -scaled_w + 1
        min_y = -scaled_h + 1
        max_x = self.image_w - 1
        max_y = self.image_h - 1
        return max(min_x, min(x, max_x)), max(min_y, min(y, max_y))

    def _load_image_for_canvas(self, fit_to_canvas: bool = True) -> None:
        if not self.image_path:
            return

        if not PIL_AVAILABLE:
            try:
                self.tk_image = tk.PhotoImage(file=self.image_path)
            except Exception as exc:
                messagebox.showerror(
                    self._t("unsupported_image"),
                    f"{self._t('pillow_required_detail')} {exc}",
                )
                return

            self.image_w = self.tk_image.width()
            self.image_h = self.tk_image.height()
            if fit_to_canvas:
                canvas_w = max(1, self.canvas.winfo_width())
                canvas_h = max(1, self.canvas.winfo_height())
                scale = min(canvas_w / self.image_w, canvas_h / self.image_h)
                self.display_scale = max(scale, 0.01)
        else:
            assert Image is not None and ImageTk is not None
            with Image.open(self.image_path) as img:
                img.load()
                self.image_w, self.image_h = img.size

                if fit_to_canvas:
                    canvas_w = max(1, self.canvas.winfo_width())
                    canvas_h = max(1, self.canvas.winfo_height())
                    scale = min(canvas_w / self.image_w, canvas_h / self.image_h)
                    self.display_scale = max(scale, 0.01)

                target_w = max(1, int(self.image_w * self.display_scale))
                target_h = max(1, int(self.image_h * self.display_scale))
                resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                self.tk_image = ImageTk.PhotoImage(resized)

        if self.auto_base_var.get():
            self.base_w_var.set(str(self.image_w))
            self.base_h_var.set(str(self.image_h))

        self._update_grid_step_from_button()

        if fit_to_canvas:
            canvas_w = max(1, self.canvas.winfo_width())
            canvas_h = max(1, self.canvas.winfo_height())
            self.display_offset_x = int((canvas_w - int(self.image_w * self.display_scale)) / 2)
            self.display_offset_y = int((canvas_h - int(self.image_h * self.display_scale)) / 2)

        self.display_offset_x, self.display_offset_y = self._clamp_display_offset(self.display_offset_x, self.display_offset_y)

        self.zoom_level_var.set(self.display_scale)
        self._update_zoom_label()

        prev_rect = self.rect_px
        has_prev_rect = prev_rect[2] > prev_rect[0] and prev_rect[3] > prev_rect[1]

        self.canvas.delete("all")
        self.overlay_guide_ids.clear()
        if self.base_visible_var.get():
            self.canvas.create_image(
                self.display_offset_x,
                self.display_offset_y,
                image=self.tk_image,
                anchor=tk.NW,
                tags=("image",),
            )

        self.layer_photo_refs.clear()
        self.layer_item_ids.clear()
        if PIL_AVAILABLE:
            assert Image is not None and ImageTk is not None
            for key in self.overlay_order:
                path = self.layer_paths.get(key, "")
                if not path or not self.layer_visible.get(key, True):
                    continue
                try:
                    with Image.open(path) as ov_img:
                        ov_img.load()
                        ov_rgba = ov_img.convert("RGBA")
                        self.layer_sizes[key] = ov_rgba.size
                        opacity = max(0, min(100, int(self.layer_opacity.get(key, 100))))
                        if opacity < 100:
                            alpha = ov_rgba.getchannel("A").point(lambda p: int(p * (opacity / 100.0)))
                            ov_rgba.putalpha(alpha)

                        ow, oh = ov_rgba.size
                        scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
                        disp_w = max(1, int(ow * self.display_scale * scale_factor))
                        disp_h = max(1, int(oh * self.display_scale * scale_factor))
                        ov_resized = ov_rgba.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(ov_resized)
                        self.layer_photo_refs[key] = photo

                        ox, oy = self.layer_offsets.get(key, (0, 0))
                        ox, oy = self._clamp_overlay_offset(key, ox, oy)
                        self.layer_offsets[key] = (ox, oy)

                        cx = int(round(self.display_offset_x + ox * self.display_scale))
                        cy = int(round(self.display_offset_y + oy * self.display_scale))
                        item_id = self.canvas.create_image(cx, cy, image=photo, anchor=tk.NW, tags=(key, "overlay"))
                        self.layer_item_ids[key] = item_id
                except Exception:
                    continue
        self._draw_grid()
        self.drag_rect_id = None
        if has_prev_rect:
            self.rect_px = prev_rect
            self._draw_selection_rect()
        else:
            self.rect_px = (0, 0, 0, 0)
        self._update_pan_scrollbars()
        self._update_info()

    def _on_canvas_resize(self, _event: tk.Event) -> None:
        if self.image_path:
            self._load_image_for_canvas(fit_to_canvas=self.zoom_fit_mode)

    def _canvas_to_image_px(self, cx: float, cy: float) -> tuple[int, int]:
        x = (cx - self.display_offset_x) / self.display_scale
        y = (cy - self.display_offset_y) / self.display_scale
        x = min(max(x, 0), self.image_w)
        y = min(max(y, 0), self.image_h)
        return int(round(x)), int(round(y))

    def _image_px_to_canvas(self, px: int, py: int) -> tuple[int, int]:
        cx = int(round(px * self.display_scale + self.display_offset_x))
        cy = int(round(py * self.display_scale + self.display_offset_y))
        return cx, cy

    def _event_matches_click_mode(self, event: tk.Event) -> bool:
        button = getattr(event, "num", None)
        if self.click_mode_var.get() == "left":
            return button == 1
        return button == 3

    def _on_pointer_down(self, event: tk.Event) -> None:
        if not self.image_path:
            return
        button = getattr(event, "num", None)
        if button == 2 or self.pan_mode_var.get():
            self.pan_drag_start = (event.x, event.y)
            self.pan_drag_origin = (int(self.display_offset_x), int(self.display_offset_y))
            return
        if not self._event_matches_click_mode(event):
            return

        if self.move_layer_mode_var.get():
            key = self.active_layer_var.get()
            if key and self.layer_paths.get(key, ""):
                self.overlay_drag_start = (event.x, event.y)
                self.overlay_drag_origin = self.layer_offsets.get(key, (0, 0))
                return

        if self.rect_move_mode_var.get() and not self.rect_lock_var.get():
            px, py = self._canvas_to_image_px(event.x, event.y)
            if self._point_inside_rect(px, py):
                self.rect_drag_start = (event.x, event.y)
                self.rect_drag_origin = self.rect_px
                return

        self.drag_start = self._canvas_to_image_px(event.x, event.y)
        if self.fixed_size_var.get():
            self._update_fixed_rect(event.x, event.y)

    def _on_pointer_drag(self, event: tk.Event) -> None:
        if self.pan_drag_start is not None and self.pan_drag_origin is not None:
            sx, sy = self.pan_drag_start
            ox, oy = self.pan_drag_origin
            self._set_display_offset(ox + (event.x - sx), oy + (event.y - sy), redraw=False)
            return

        if not self.image_path or self.drag_start is None:
            if self.overlay_drag_start is None:
                return

        if self.overlay_drag_start is not None and self.overlay_drag_origin is not None:
            key = self.active_layer_var.get()
            if not key:
                return
            sx, sy = self.overlay_drag_start
            ox, oy = self.overlay_drag_origin
            dx = int(round((event.x - sx) / max(self.display_scale, 0.01)))
            dy = int(round((event.y - sy) / max(self.display_scale, 0.01)))
            nx, ny = self._clamp_overlay_offset(key, ox + dx, oy + dy)
            self.layer_offsets[key] = (nx, ny)
            if key in self.layer_x_vars:
                self.layer_x_vars[key].set(str(nx))
            if key in self.layer_y_vars:
                self.layer_y_vars[key].set(str(ny))
            if key in self.layer_x_slider_vars:
                self.layer_x_slider_vars[key].set(float(nx))
            if key in self.layer_y_slider_vars:
                self.layer_y_slider_vars[key].set(float(ny))
            item_id = self.layer_item_ids.get(key)
            if item_id is not None:
                cx = int(round(self.display_offset_x + nx * self.display_scale))
                cy = int(round(self.display_offset_y + ny * self.display_scale))
                self.canvas.coords(item_id, cx, cy)
                self._draw_overlay_guides(key)
                self._update_info()
            else:
                self._load_image_for_canvas()
            return

        if self.rect_drag_start is not None and self.rect_drag_origin is not None:
            sx, sy = self.rect_drag_start
            dx = int(round((event.x - sx) / max(self.display_scale, 0.01)))
            dy = int(round((event.y - sy) / max(self.display_scale, 0.01)))
            x1, y1, x2, y2 = self.rect_drag_origin
            w = x2 - x1
            h = y2 - y1
            if w > 0 and h > 0:
                nx1 = max(0, min(self.image_w - w, x1 + dx))
                ny1 = max(0, min(self.image_h - h, y1 + dy))
                if self.grid_snap_var.get():
                    nx1 = self._snap_value(nx1)
                    ny1 = self._snap_value(ny1)
                    nx1 = max(0, min(self.image_w - w, nx1))
                    ny1 = max(0, min(self.image_h - h, ny1))
                self.rect_px = (nx1, ny1, nx1 + w, ny1 + h)
                self._draw_selection_rect()
                self._update_info()
            return

        if self.fixed_size_var.get():
            self._update_fixed_rect(event.x, event.y)
            return

        assert self.drag_start is not None
        x0, y0 = self.drag_start
        x1, y1 = self._canvas_to_image_px(event.x, event.y)

        x0 = self._snap_value(x0)
        y0 = self._snap_value(y0)
        x1 = self._snap_value(x1)
        y1 = self._snap_value(y1)

        left, right = sorted((x0, x1))
        top, bottom = sorted((y0, y1))
        self.rect_px = (left, top, right, bottom)
        self._draw_selection_rect()
        self._update_info()

    def _on_pointer_up(self, _event: tk.Event) -> None:
        self.drag_start = None
        self.rect_drag_start = None
        self.rect_drag_origin = None
        self.overlay_drag_start = None
        self.overlay_drag_origin = None
        self.pan_drag_start = None
        self.pan_drag_origin = None
        self._clear_overlay_guides()

    def _clear_overlay_guides(self) -> None:
        if not hasattr(self, "overlay_guide_ids"):
            return
        for item_id in self.overlay_guide_ids:
            self.canvas.delete(item_id)
        self.overlay_guide_ids.clear()

    def _draw_overlay_guides(self, key: str) -> None:
        if not self.show_overlay_guides_var.get():
            self._clear_overlay_guides()
            return
        ow, oh = self.layer_sizes.get(key, (0, 0))
        if ow <= 0 or oh <= 0:
            self._clear_overlay_guides()
            return
        scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
        scaled_w = max(1, int(round(ow * scale_factor)))
        scaled_h = max(1, int(round(oh * scale_factor)))
        ox, oy = self.layer_offsets.get(key, (0, 0))
        ov_center_x = ox + (scaled_w / 2.0)
        ov_center_y = oy + (scaled_h / 2.0)
        base_center_x = self.image_w / 2.0
        base_center_y = self.image_h / 2.0

        bx, by = self._image_px_to_canvas(int(round(base_center_x)), int(round(base_center_y)))
        oxc, oyc = self._image_px_to_canvas(int(round(ov_center_x)), int(round(ov_center_y)))
        left = self.display_offset_x
        top = self.display_offset_y
        right = left + int(self.image_w * self.display_scale)
        bottom = top + int(self.image_h * self.display_scale)

        self._clear_overlay_guides()
        self.overlay_guide_ids.append(self.canvas.create_line(left, by, right, by, fill="#00bcd4", dash=(3, 3), tags=("guide",)))
        self.overlay_guide_ids.append(self.canvas.create_line(bx, top, bx, bottom, fill="#00bcd4", dash=(3, 3), tags=("guide",)))
        self.overlay_guide_ids.append(self.canvas.create_line(left, oyc, right, oyc, fill="#ffd54f", dash=(2, 4), tags=("guide",)))
        self.overlay_guide_ids.append(self.canvas.create_line(oxc, top, oxc, bottom, fill="#ffd54f", dash=(2, 4), tags=("guide",)))
        self.overlay_guide_ids.append(self.canvas.create_line(bx, by, oxc, oyc, fill="#ff6f91", dash=(2, 2), tags=("guide",)))

    def _point_inside_rect(self, x: int, y: int) -> bool:
        x1, y1, x2, y2 = self.rect_px
        return x2 > x1 and y2 > y1 and x1 <= x <= x2 and y1 <= y <= y2

    def _nudge_rect(self, dx_dir: int, dy_dir: int) -> None:
        x1, y1, x2, y2 = self.rect_px
        if x2 <= x1 or y2 <= y1:
            return
        try:
            step = int(self.rect_nudge_step_var.get().strip())
        except Exception:
            step = 1
        step = max(1, step)
        w = x2 - x1
        h = y2 - y1
        nx1 = max(0, min(self.image_w - w, x1 + dx_dir * step))
        ny1 = max(0, min(self.image_h - h, y1 + dy_dir * step))
        if self.grid_snap_var.get():
            nx1 = self._snap_value(nx1)
            ny1 = self._snap_value(ny1)
            nx1 = max(0, min(self.image_w - w, nx1))
            ny1 = max(0, min(self.image_h - h, ny1))
        self.rect_px = (nx1, ny1, nx1 + w, ny1 + h)
        self._draw_selection_rect()
        self._update_info()

    def _toggle_grid_tools(self, force_hide: bool = False) -> None:
        self.show_grid_tools_var.set(False)

    def _apply_ui_mode(self) -> None:
        self._render_overlay_cards()

    def _update_fixed_rect(self, cx: float, cy: float) -> None:
        if not self.image_path:
            return

        width, height = self._image_sizes()
        center_x, center_y = self._canvas_to_image_px(cx, cy)

        left = center_x - width // 2
        top = center_y - height // 2
        right = left + width
        bottom = top + height

        if left < 0:
            right -= left
            left = 0
        if top < 0:
            bottom -= top
            top = 0
        if right > self.image_w:
            left -= right - self.image_w
            right = self.image_w
        if bottom > self.image_h:
            top -= bottom - self.image_h
            bottom = self.image_h

        left = max(0, left)
        top = max(0, top)
        right = min(self.image_w, right)
        bottom = min(self.image_h, bottom)

        if self.grid_snap_var.get():
            left = self._snap_value(left)
            top = self._snap_value(top)
            right = self._snap_value(right)
            bottom = self._snap_value(bottom)
            if right <= left:
                right = min(self.image_w, left + width)
            if bottom <= top:
                bottom = min(self.image_h, top + height)

        self.rect_px = (left, top, right, bottom)
        self._draw_selection_rect()
        self._update_info()

    def _base_resolution(self) -> tuple[int, int]:
        try:
            bw = int(self.base_w_var.get().strip())
            bh = int(self.base_h_var.get().strip())
            if bw <= 0 or bh <= 0:
                raise ValueError
            return bw, bh
        except Exception:
            messagebox.showerror("Invalid Resolution", "Base width/height must be positive integers.")
            raise

    def _current_rect(self) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = self.rect_px
        if x2 <= x1 or y2 <= y1:
            raise ValueError("No rectangle selected")
        return x1, y1, x2, y2

    def _normalized(self) -> tuple[float, float, float, float]:
        bw, bh = self._base_resolution()
        x1, y1, x2, y2 = self._current_rect()
        return x1 / bw, y1 / bh, x2 / bw, y2 / bh

    def _update_info(self) -> None:
        try:
            x1, y1, x2, y2 = self._current_rect()
            w = x2 - x1
            h = y2 - y1
            nx1, ny1, nx2, ny2 = self._normalized()
            bw, bh = self._image_sizes()
            base_w, base_h = self._base_resolution()
            active_layer = self.active_layer_var.get() or "base"
            offx, offy = self.layer_offsets.get(active_layer, (0, 0))
            self.info_var.set(
                f"Button px: {w} x {h}  target {bw} x {bh}\n"
                f"Rect px: ({x1}, {y1}) -> ({x2}, {y2})\n"
                f"Base: {base_w} x {base_h} | {active_layer} pos: {offx}, {offy}\n"
                f"Norm: {nx1:.6f} {ny1:.6f} {nx2:.6f} {ny2:.6f}"
            )
        except Exception:
            self.info_var.set("Rect: -")

        self.name_info_var.set("Manual name")

    def _next_name(self) -> str:
        prefix = self.name_prefix_var.get().strip()
        if not prefix:
            prefix = "button"
        return prefix

    def _build_line(self) -> str:
        nx1, ny1, nx2, ny2 = self._normalized()
        name = self._next_name()
        texture = self.texture_var.get().strip()
        command = self.command_var.get().strip()
        r = int(self.r_var.get().strip())
        g = int(self.g_var.get().strip())
        b = int(self.b_var.get().strip())
        a = int(self.a_var.get().strip())
        rounding = int(self.round_var.get().strip())

        return DEFAULT_TEMPLATE.format(
            name=name,
            texture=texture,
            command=command,
            x1=nx1,
            y1=ny1,
            x2=nx2,
            y2=ny2,
            r=r,
            g=g,
            b=b,
            a=a,
            rounding=rounding,
        )

    def generate_line(self) -> None:
        try:
            line = self._build_line()
        except ValueError:
            messagebox.showwarning("No Selection", "Select an area first by right-click dragging.")
            return
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        self.out_text.delete("1.0", tk.END)
        self.out_text.insert(tk.END, line)

    def append_batch(self) -> None:
        self.generate_line()
        line = self.out_text.get("1.0", tk.END).strip()
        if not line:
            return
        if self.batch_text.get("1.0", tk.END).strip():
            self.batch_text.insert(tk.END, "\n")
        self.batch_text.insert(tk.END, line)

    def copy_output(self) -> None:
        text = self.out_text.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def export_batch(self) -> None:
        text = self.batch_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("No Data", "Batch output is empty.")
            return

        path = filedialog.asksaveasfilename(
            title="Export Batch",
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("CFG File", "*.cfg"), ("All files", "*.*")],
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")

        messagebox.showinfo("Exported", f"Saved: {path}")

    def _compose_merged_preview(self):
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow is required for merged preview export.")
        if not self.image_path:
            raise RuntimeError("Load a base image first.")

        assert Image is not None
        with Image.open(self.image_path) as base_img:
            base = base_img.convert("RGBA")

        for key in self.overlay_order:
            path = self.layer_paths.get(key, "")
            if not path or not self.layer_visible.get(key, True):
                continue

            try:
                with Image.open(path) as ov_img:
                    ov = ov_img.convert("RGBA")
            except Exception:
                continue

            opacity = max(0, min(100, int(self.layer_opacity.get(key, 100))))
            if opacity < 100:
                alpha = ov.getchannel("A").point(lambda p: int(p * (opacity / 100.0)))
                ov.putalpha(alpha)

            scale_factor = self.layer_scale_vars[key].get() if key in self.layer_scale_vars else 1.0
            if scale_factor != 1.0:
                ow, oh = ov.size
                nw = max(1, int(round(ow * scale_factor)))
                nh = max(1, int(round(oh * scale_factor)))
                ov = ov.resize((nw, nh), Image.Resampling.LANCZOS)

            ox, oy = self.layer_offsets.get(key, (0, 0))
            base.paste(ov, (int(ox), int(oy)), ov)

        return base

    def export_merged_preview(self) -> None:
        if not self.image_path:
            messagebox.showinfo("No Image", "Load base image first.")
            return
        if not PIL_AVAILABLE:
            messagebox.showerror("Pillow Required", "Install Pillow to export merged preview image.")
            return
        assert Image is not None

        fmt = self.export_format_var.get().strip().upper() or "PNG"
        ext_map = {"PNG": ".png", "JPG": ".jpg", "BMP": ".bmp", "TGA": ".tga"}
        pil_fmt = {"PNG": "PNG", "JPG": "JPEG", "BMP": "BMP", "TGA": "TGA"}
        ext = ext_map.get(fmt, ".png")

        path = filedialog.asksaveasfilename(
            title="Export Merged Preview",
            defaultextension=ext,
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("BMP", "*.bmp"), ("TGA", "*.tga"), ("All files", "*.*")],
            initialdir=self._image_dialog_dir(self.image_path),
        )
        if not path:
            return

        try:
            merged = self._compose_merged_preview()
            if fmt == "JPG":
                rgb = Image.new("RGB", merged.size, (0, 0, 0))
                rgb.paste(merged, mask=merged.split()[-1])
                rgb.save(path, format=pil_fmt[fmt], quality=95)
            else:
                merged.save(path, format=pil_fmt.get(fmt, "PNG"))
        except Exception as exc:
            messagebox.showerror("Export Failed", str(exc))
            return

        messagebox.showinfo("Exported", f"Saved: {path}")


def main() -> None:
    if TkinterDnD is not None:
        root = TkinterDnD.Tk()  # type: ignore[assignment]
    else:
        root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
