from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import webbrowser

YOUTUBE_URL = "https://www.youtube.com/@sheesh5576"


def open_credits(parent: tk.Misc | None = None) -> None:
    root = tk.Toplevel(parent) if parent is not None else tk.Tk()
    root.title("Credits")
    root.geometry("560x320")
    root.minsize(560, 320)

    outer = ttk.Frame(root, padding=18)
    outer.pack(fill=tk.BOTH, expand=True)

    ttk.Label(outer, text="CSPB Modder Tool Credits", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    ttk.Label(
        outer,
        text=(
            "Thanks for using this tool.\n\n"
            "Built to help CSPB modders map touch UI faster, cleaner, and with less trial-and-error.\n\n"
            "Credits to AI GitHub Copilot for development assistance.\n"
            "Creator channel: @sheesh5576"
        ),
        justify=tk.LEFT,
    ).pack(anchor=tk.W, pady=(12, 16))

    btn_row = ttk.Frame(outer)
    btn_row.pack(fill=tk.X)

    ttk.Button(btn_row, text="Open YouTube Channel", command=lambda: webbrowser.open(YOUTUBE_URL)).pack(side=tk.LEFT)
    ttk.Button(btn_row, text="Close", command=root.destroy).pack(side=tk.RIGHT)

    if parent is None:
        root.mainloop()


if __name__ == "__main__":
    open_credits(None)
