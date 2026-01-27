"""Tkinter GUI for the Image Editor application."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk
import cv2

from src.app.controller import EditorController


class ImageEditorGUI:
    """Main GUI class for the Image Editor."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("HIT137 A3 - Image Editor")
        self.root.geometry("900x600")

        self._tk_image: ImageTk.PhotoImage | None = None

        self._build_layout()

        self.controller = EditorController(self)
        self._build_menu()
        self._build_controls()

        self._placeholder_label = tk.Label(
            self.image_panel, text="GUI Loaded ✅", font=("Segoe UI", 18), bg="black", fg="white"
        )
        self._placeholder_label.pack(pady=40)

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

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    def _build_layout(self) -> None:
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(self.main_frame, width=220, bg="#f0f0f0")
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.image_panel = tk.Frame(self.main_frame, bg="black")
        self.image_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _build_controls(self) -> None:
        title = tk.Label(self.control_panel, text="Controls", bg="#f0f0f0", font=("Segoe UI", 12, "bold"))
        title.pack(pady=(10, 8))

        btn_gray = tk.Button(self.control_panel, text="Grayscale", command=self.controller.apply_grayscale)
        btn_gray.pack(fill=tk.X, padx=10, pady=5)

        blur_lbl = tk.Label(self.control_panel, text="Blur Intensity", bg="#f0f0f0")
        blur_lbl.pack(padx=10, pady=(15, 5), anchor="w")

        self.blur_var = tk.IntVar(value=0)
        blur_slider = tk.Scale(
            self.control_panel,
            from_=0,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.blur_var,
            command=self._on_blur_change,
        )
        blur_slider.pack(fill=tk.X, padx=10)

        reset_blur = tk.Button(self.control_panel, text="Reset Blur", command=self._reset_blur)
        reset_blur.pack(fill=tk.X, padx=10, pady=8)

    def _on_blur_change(self, _value: str) -> None:
        self.controller.apply_blur(self.blur_var.get())

    def _reset_blur(self) -> None:
        self.blur_var.set(0)
        self.controller.reset_blur()

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
