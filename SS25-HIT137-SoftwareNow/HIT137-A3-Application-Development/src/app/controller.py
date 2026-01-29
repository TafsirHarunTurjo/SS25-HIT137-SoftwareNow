"""Controller layer connecting GUI, model, processor, and history.

Fixes:
- Reliable undo/redo across buttons AND sliders (commit-on-release)
- Reset buttons actually revert effects
- Confirm dialog before save/save-as
- Restore original image (undoable)
- After saving, you can restore original and undo back to edited state
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from tkinter import filedialog, messagebox
import os

import cv2
import numpy as np

from src.app.model import ImageModel
from src.app.processor import ImageProcessor
from src.app.history import HistoryManager


@dataclass
class SliderSession:
    """Represents one slider transaction."""
    name: str
    base: np.ndarray


class EditorController:
    """Coordinates interactions between GUI and application logic."""

    def __init__(self, gui) -> None:
        self.gui = gui
        self.model = ImageModel()
        self.processor = ImageProcessor()
        self.history = HistoryManager()

        self._slider_session: Optional[SliderSession] = None

    # ---------------- helpers ----------------

    def _require_image(self) -> bool:
        if not self.model.has_image():
            messagebox.showwarning("No Image", "Please open an image first.")
            return False
        return True

    def _clear_slider_session(self) -> None:
        self._slider_session = None

    def _status(self, msg: str) -> None:
        filename = os.path.basename(self.model.info.path) if self.model.info.path else "No file"
        dims = f"{self.model.info.width}x{self.model.info.height}" if self.model.has_image() else "-"
        dirty = "*" if self.model.dirty else ""
        u, r = self.history.counts()
        self.gui.update_status(f"{msg} | {filename} ({dims}){dirty} | undo={u} redo={r}")

    def _apply_new_state(self, label: str, out: np.ndarray) -> None:
        """Push undo once, clear redo, set current, display."""
        self._clear_slider_session()
        self.history.push_undo(self.model.current)
        self.history.clear_redo()

        self.model.set_current(out, dirty=True)
        self.gui.display_image(out)
        self._status(f"Applied: {label}")

    # ---------------- file menu ----------------

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
        self._clear_slider_session()

        self.gui.reset_all_controls()
        self.gui.display_image(img)
        self._status("Loaded")

    def save_image(self) -> None:
        if not self._require_image():
            return

        if not self.model.info.path:
            self.save_image_as()
            return

        if not messagebox.askyesno("Confirm Save", "Save changes to the current file?"):
            self._status("Save cancelled")
            return

        ok = cv2.imwrite(self.model.info.path, self.model.current)
        if not ok:
            messagebox.showerror("Error", "Save failed.")
            return

        self.model.mark_saved()
        self._status("Saved")

    def save_image_as(self) -> None:
        if not self._require_image():
            return

        if not messagebox.askyesno("Confirm Save As", "Save the edited image as a new file?"):
            self._status("Save As cancelled")
            return

        path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPG", "*.jpg"),
                ("BMP", "*.bmp"),
                ("All Files", "*.*"),
            ],
        )
        if not path:
            self._status("Save As cancelled")
            return

        ok = cv2.imwrite(path, self.model.current)
        if not ok:
            messagebox.showerror("Error", "Save As failed.")
            return

        self.model.info.path = path
        self.model.mark_saved()
        self._status("Saved As")

    # ---------------- edit menu ----------------

    def undo(self) -> None:
        if not self._require_image():
            return

        self._clear_slider_session()
        prev = self.history.undo(self.model.current)
        if prev is None:
            self._status("Undo: nothing to undo")
            return

        self.model.set_current(prev, dirty=True)
        self.gui.display_image(prev)
        self._status("Undo applied")

    def redo(self) -> None:
        if not self._require_image():
            return

        self._clear_slider_session()
        nxt = self.history.redo(self.model.current)
        if nxt is None:
            self._status("Redo: nothing to redo")
            return

        self.model.set_current(nxt, dirty=True)
        self.gui.display_image(nxt)
        self._status("Redo applied")

    def restore_original(self) -> None:
        """Restore the initial loaded image (undoable)."""
        if not self._require_image():
            return
        if self.model.original is None:
            self._status("No original image available")
            return

        self._clear_slider_session()
        # Undoable action: push current to undo then set to original
        self.history.push_undo(self.model.current)
        self.history.clear_redo()

        out = self.model.original.copy()
        self.model.set_current(out, dirty=True)
        self.gui.reset_all_controls()
        self.gui.display_image(out)
        self._status("Restored original (undo to go back)")

    # ---------------- button actions ----------------

    def apply_grayscale(self) -> None:
        if not self._require_image():
            return
        out = self.processor.grayscale(self.model.current)
        self._apply_new_state("Grayscale", out)

    def apply_edge(self) -> None:
        if not self._require_image():
            return
        out = self.processor.edge(self.model.current, 100, 200)
        self._apply_new_state("Edge Detection", out)

    def rotate(self, angle: int) -> None:
        if not self._require_image():
            return
        try:
            out = self.processor.rotate(self.model.current, angle)
        except Exception as e:
            messagebox.showerror("Rotate Error", str(e))
            return
        self._apply_new_state(f"Rotate {angle}°", out)

    def flip(self, mode: str) -> None:
        if not self._require_image():
            return
        try:
            out = self.processor.flip(self.model.current, mode)
        except Exception as e:
            messagebox.showerror("Flip Error", str(e))
            return
        self._apply_new_state(f"Flip {mode.title()}", out)

    def resize_to(self, width: int, height: int) -> None:
        if not self._require_image():
            return
        try:
            out = self.processor.resize(self.model.current, width, height)
        except Exception as e:
            messagebox.showerror("Resize Error", str(e))
            return
        self._apply_new_state(f"Resize {width}x{height}", out)

    # ---------------- slider actions (robust) ----------------

    def slider_begin(self, name: str) -> None:
        """Begin a slider transaction and push undo ONCE."""
        if not self._require_image():
            return

        # Start session using current as base
        self._slider_session = SliderSession(name=name, base=self.model.current.copy())

        # Push undo once for the whole drag
        self.history.push_undo(self.model.current)
        self.history.clear_redo()
        self._status(f"{name.title()} adjust started")

    def slider_preview(self, name: str, value: int) -> None:
        """Preview slider effect WITHOUT pushing more undo entries."""
        if not self._require_image():
            return

        if self._slider_session is None or self._slider_session.name != name:
            # If user drags without press event (rare), start session
            self.slider_begin(name)

        base = self._slider_session.base
        value = int(value)

        if name == "blur":
            out = self.processor.blur(base, value)
        elif name == "brightness":
            out = self.processor.adjust_brightness(base, value)
        elif name == "contrast":
            # slider 0..200 -> alpha 0.1..2.0, default 100 -> 1.0
            alpha = max(0.1, value / 100.0)
            out = self.processor.adjust_contrast(base, alpha)
        else:
            return

        self.model.set_current(out, dirty=True)
        self.gui.display_image(out)
        self._status(f"{name.title()} preview: {value}")

    def slider_commit(self, name: str) -> None:
        """End slider transaction."""
        if not self._require_image():
            return
        if self._slider_session is None or self._slider_session.name != name:
            return
        self._slider_session = None
        self._status(f"{name.title()} committed")

    def slider_reset(self, name: str) -> None:
        """Reset slider effect back to base state in a clean, undoable way."""
        if not self._require_image():
            return

        # If currently in a session, revert to base from session (which is the pre-drag state).
        if self._slider_session is not None and self._slider_session.name == name:
            base = self._slider_session.base.copy()
            self.model.set_current(base, dirty=True)
            self.gui.display_image(base)
            self._slider_session = None
            self._status(f"{name.title()} reset (undo returns to previous)")
            return

        # If no active session: make reset an undoable action by pushing current then applying "identity"
        self.history.push_undo(self.model.current)
        self.history.clear_redo()

        # Identity based on current (effectively no change) doesn't help; so reset means:
        # return to the LAST undo state (one step back) if exists.
        prev = self.history.undo(self.model.current)
        if prev is None:
            self._status(f"{name.title()} reset: nothing to revert")
            return

        self.model.set_current(prev, dirty=True)
        self.gui.display_image(prev)
        self._status(f"{name.title()} reset via undo")
