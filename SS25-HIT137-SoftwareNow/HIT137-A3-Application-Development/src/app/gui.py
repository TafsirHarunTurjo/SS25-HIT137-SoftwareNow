"""Tkinter GUI for the Image Editor application."""

from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog

from PIL import Image, ImageTk
import cv2

from src.app.controller import EditorController


class ImageEditorGUI:
    """Main GUI class for the Image Editor."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("HIT137 A3 - Image Editor")
        self.root.geometry("1050x680")

        self._tk_image: ImageTk.PhotoImage | None = None

        self._build_layout()

        self.controller = EditorController(self)
        self._build_menu()
        self._build_controls()

        self._placeholder_label = tk.Label(
            self.image_panel,
            text="Open an image from File → Open",
            font=("Segoe UI", 16),
            bg="black",
            fg="white",
        )
        self._placeholder_label.pack(pady=40)

    # ---------------- UI build ----------------

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.controller.open_image)
        file_menu.add_command(label="Save", command=self.controller.save_image)
        file_menu.add_command(label="Save As", command=self.controller.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.controller.undo)
        edit_menu.add_command(label="Redo", command=self.controller.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Restore Original", command=self.controller.restore_original)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    def _build_layout(self) -> None:
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(self.main_frame, width=280, bg="#f0f0f0")
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.image_panel = tk.Frame(self.main_frame, bg="black")
        self.image_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _build_controls(self) -> None:
        title = tk.Label(self.control_panel, text="Controls", bg="#f0f0f0", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(10, 8))

        # --- Buttons ---
        tk.Button(self.control_panel, text="Grayscale", command=self.controller.apply_grayscale).pack(fill=tk.X, padx=10, pady=4)
        tk.Button(self.control_panel, text="Edge Detection", command=self.controller.apply_edge).pack(fill=tk.X, padx=10, pady=4)

        tk.Label(self.control_panel, text="Rotate", bg="#f0f0f0", font=("Segoe UI", 10, "bold")).pack(padx=10, pady=(12, 2), anchor="w")
        rot_row = tk.Frame(self.control_panel, bg="#f0f0f0")
        rot_row.pack(fill=tk.X, padx=10)
        tk.Button(rot_row, text="90°", command=lambda: self.controller.rotate(90)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(rot_row, text="180°", command=lambda: self.controller.rotate(180)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(rot_row, text="270°", command=lambda: self.controller.rotate(270)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        tk.Label(self.control_panel, text="Flip", bg="#f0f0f0", font=("Segoe UI", 10, "bold")).pack(padx=10, pady=(12, 2), anchor="w")
        flip_row = tk.Frame(self.control_panel, bg="#f0f0f0")
        flip_row.pack(fill=tk.X, padx=10)
        tk.Button(flip_row, text="Horizontal", command=lambda: self.controller.flip("horizontal")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        tk.Button(flip_row, text="Vertical", command=lambda: self.controller.flip("vertical")).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        tk.Button(self.control_panel, text="Resize...", command=self._resize_dialog).pack(fill=tk.X, padx=10, pady=(12, 6))
        tk.Button(self.control_panel, text="Restore Original", command=self.controller.restore_original).pack(fill=tk.X, padx=10, pady=(0, 10))

        # --- Sliders (commit-on-release) ---
        self._make_slider(
            name="blur",
            label="Blur (0..10)",
            from_=0,
            to=10,
            default=0,
        )
        self._make_slider(
            name="brightness",
            label="Brightness (-100..100)",
            from_=-100,
            to=100,
            default=0,
        )
        self._make_slider(
            name="contrast",
            label="Contrast (0..200 => 0.1..2.0)",
            from_=0,
            to=200,
            default=100,
        )

    def _make_slider(self, name: str, label: str, from_: int, to: int, default: int) -> None:
        tk.Label(self.control_panel, text=label, bg="#f0f0f0").pack(padx=10, pady=(10, 2), anchor="w")

        var = tk.IntVar(value=default)
        slider = tk.Scale(
            self.control_panel,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            variable=var,
            command=lambda v, n=name: self.controller.slider_preview(n, int(float(v))),
        )
        slider.pack(fill=tk.X, padx=10)

        slider.bind("<ButtonPress-1>", lambda _e, n=name: self.controller.slider_begin(n))
        slider.bind("<ButtonRelease-1>", lambda _e, n=name: self.controller.slider_commit(n))

        tk.Button(
            self.control_panel,
            text=f"Reset {name.title()}",
            command=lambda n=name, s=slider, d=default: self._reset_slider(n, s, d),
        ).pack(fill=tk.X, padx=10, pady=(4, 0))

        setattr(self, f"{name}_var", var)
        setattr(self, f"{name}_slider", slider)
        setattr(self, f"{name}_default", default)

    def _reset_slider(self, name: str, slider: tk.Scale, default: int) -> None:
        slider.set(default)
        self.controller.slider_reset(name)

    def reset_all_controls(self) -> None:
        """Reset slider UI values to defaults (called after open/restore)."""
        for name in ("blur", "brightness", "contrast"):
            slider = getattr(self, f"{name}_slider", None)
            default = getattr(self, f"{name}_default", None)
            if slider is not None and default is not None:
                slider.set(default)

    def _resize_dialog(self) -> None:
        w = simpledialog.askinteger("Resize", "Enter new width (px):", minvalue=1)
        if w is None:
            return
        h = simpledialog.askinteger("Resize", "Enter new height (px):", minvalue=1)
        if h is None:
            return
        self.controller.resize_to(w, h)

    # ---------------- UI updates ----------------

    def update_status(self, text: str) -> None:
        self.status_var.set(text)

    def display_image(self, img) -> None:
        if img is None:
            return

        if hasattr(self, "_placeholder_label") and self._placeholder_label.winfo_exists():
            self._placeholder_label.destroy()

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        panel_w = max(1, self.image_panel.winfo_width())
        panel_h = max(1, self.image_panel.winfo_height())
        if panel_w == 1 and panel_h == 1:
            self.root.update_idletasks()
            panel_w = max(1, self.image_panel.winfo_width())
            panel_h = max(1, self.image_panel.winfo_height())

        img_w, img_h = pil_img.size
        scale = min(panel_w / img_w, panel_h / img_h)
        new_size = (max(1, int(img_w * scale)), max(1, int(img_h * scale)))
        pil_img = pil_img.resize(new_size)

        self._tk_image = ImageTk.PhotoImage(pil_img)

        if hasattr(self, "image_label") and self.image_label.winfo_exists():
            self.image_label.config(image=self._tk_image)
        else:
            self.image_label = tk.Label(self.image_panel, image=self._tk_image, bg="black")
            self.image_label.pack(expand=True)
