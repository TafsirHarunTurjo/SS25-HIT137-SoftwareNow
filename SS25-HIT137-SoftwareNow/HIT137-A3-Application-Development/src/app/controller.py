"""Controller layer connecting GUI, model, processor, and history."""

from __future__ import annotations

from tkinter import filedialog, messagebox
import cv2
import numpy as np

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

        # Slider state: keep a stable base image so slider doesn't compound blur
        self._blur_base: np.ndarray | None = None

    def _require_image(self) -> bool:
        if not self.model.has_image():
            messagebox.showwarning("No Image", "Please open an image first.")
            return False
        return True

    def _reset_slider_states(self) -> None:
        self._blur_base = None

    def _status_with_history(self, msg: str) -> None:
        self.gui.update_status(
            f"{msg} | undo={self.history.undo_count()} redo={self.history.redo_count()}"
        )

    def open_image(self) -> None:
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
        self._reset_slider_states()

        self.gui.display_image(img)
        self._status_with_history(f"Loaded: {path} ({img.shape[1]}x{img.shape[0]})")

    def apply_grayscale(self) -> None:
        """Apply grayscale and push the PREVIOUS state to undo."""
        if not self._require_image():
            return

        self._reset_slider_states()

        # IMPORTANT: push the state BEFORE mutation
        before = self.model.current.copy()
        self.history.push_undo(before)
        self.history.clear_redo()

        out = self.processor.grayscale(before)
        self.model.set_current(out, dirty=True)

        self.gui.display_image(out)
        self._status_with_history("Applied: Grayscale")

    def apply_blur(self, intensity: int) -> None:
        """Apply blur using a stable base image so the slider doesn't stack blur."""
        if not self._require_image():
            return

        intensity = int(intensity)

        if intensity == 0:
            if self._blur_base is not None:
                restored = self._blur_base.copy()
                self.model.set_current(restored, dirty=True)
                self.gui.display_image(restored)
                self._status_with_history("Blur reset to 0")
                self._blur_base = None
            else:
                self._status_with_history("Blur: 0")
            return

        if self._blur_base is None:
            # First time blur starts, capture base and push undo ONCE
            self._blur_base = self.model.current.copy()
            self.history.push_undo(self._blur_base)
            self.history.clear_redo()

        out = self.processor.blur(self._blur_base, intensity=intensity)
        self.model.set_current(out, dirty=True)

        self.gui.display_image(out)
        self._status_with_history(f"Applied: Blur (intensity={intensity})")

    def reset_blur(self) -> None:
        if not self._require_image():
            return

        if self._blur_base is not None:
            restored = self._blur_base.copy()
            self.model.set_current(restored, dirty=True)
            self.gui.display_image(restored)
            self._blur_base = None
            self._status_with_history("Blur reset")
        else:
            self._status_with_history("Blur already at default")

    def undo(self) -> None:
        if not self._require_image():
            return

        self._reset_slider_states()

        prev = self.history.undo(self.model.current)
        if prev is None:
            self._status_with_history("Undo: nothing to undo")
            return

        self.model.set_current(prev, dirty=True)
        self.gui.display_image(prev)
        self._status_with_history("Undo applied")

    def redo(self) -> None:
        if not self._require_image():
            return

        self._reset_slider_states()

        nxt = self.history.redo(self.model.current)
        if nxt is None:
            self._status_with_history("Redo: nothing to redo")
            return

        self.model.set_current(nxt, dirty=True)
        self.gui.display_image(nxt)
        self._status_with_history("Redo applied")

    def save_image(self) -> None:
        messagebox.showinfo("Info", "Save not implemented yet.")

    def save_image_as(self) -> None:
        messagebox.showinfo("Info", "Save As not implemented yet.")
