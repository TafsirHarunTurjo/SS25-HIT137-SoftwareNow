"""Controller layer connecting GUI, model, processor, and history."""

from __future__ import annotations

from tkinter import filedialog, messagebox
import cv2

from src.app.model import ImageModel
from src.app.processor import ImageProcessor
from src.app.history import HistoryManager


class EditorController:
    """Coordinates interactions between GUI and application logic."""

    def __init__(self, gui) -> None:
        self.gui = gui
        self.model = ImageModel()
        self.processor = ImageProcessor()
        self.history = HistoryManager()

    def open_image(self) -> None:
        """Open an image and display it."""
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
                ("All Files", "*.*"),
            ],
        )

        if not path:
            return

        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Error", "Failed to load image. Choose a valid JPG/PNG/BMP.")
            return

        self.model.set_original(img, path)
        self.history.clear()

        self.gui.display_image(img)
        self.gui.update_status(f"Loaded: {path} ({img.shape[1]}x{img.shape[0]})")

    def save_image(self) -> None:
        """Save current image to original path (stub)."""
        messagebox.showinfo("Info", "Save not implemented yet.")

    def save_image_as(self) -> None:
        """Save current image to a new file (stub)."""
        messagebox.showinfo("Info", "Save As not implemented yet.")

    def undo(self) -> None:
        """Undo last action (stub)."""
        messagebox.showinfo("Info", "Undo not implemented yet.")

    def redo(self) -> None:
        """Redo last undone action (stub)."""
        messagebox.showinfo("Info", "Redo not implemented yet.")
