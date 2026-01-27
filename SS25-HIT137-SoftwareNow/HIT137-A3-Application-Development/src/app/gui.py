"""Tkinter GUI for the Image Editor application."""

from __future__ import annotations

import tkinter as tk
from PIL import Image, ImageTk
import cv2

from src.app.controller import EditorController


class ImageEditorGUI:
    """Main GUI class for the Image Editor."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI."""
        self.root = root
        self.root.title("HIT137 A3 - Image Editor")
        self.root.geometry("900x600")

        # Build UI first
        self._build_layout()

        # Controller (after UI exists)
        self.controller = EditorController(self)

        # Menu (needs controller)
        self._build_menu()

        # Placeholder content
        self._placeholder_label = tk.Label(
            self.image_panel, text="GUI Loaded ✅", font=("Segoe UI", 18), bg="black", fg="white"
        )
        self._placeholder_label.pack(pady=40)

        # Keep reference to avoid garbage collection
        self._tk_image: ImageTk.PhotoImage | None = None

    def _build_menu(self) -> None:
        """Create menu bar."""
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
        """Build basic layout including status bar."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = tk.Frame(self.main_frame, width=220, bg="#f0f0f0")
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.image_panel = tk.Frame(self.main_frame, bg="black")
        self.image_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, text: str) -> None:
        """Update the status bar."""
        self.status_var.set(text)

    def display_image(self, img) -> None:
        """Display an OpenCV BGR image in the image panel."""
        if img is None:
            return

        # Remove placeholder label if present
        if hasattr(self, "_placeholder_label") and self._placeholder_label.winfo_exists():
            self._placeholder_label.destroy()

        # Convert BGR -> RGB -> PIL -> PhotoImage
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        # Fit image into the panel (simple scale-to-fit)
        panel_w = max(1, self.image_panel.winfo_width())
        panel_h = max(1, self.image_panel.winfo_height())

        # If geometry not ready, force update then re-check
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
