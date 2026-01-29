"""Image model for storing image state and metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class ImageInfo:
    """Metadata about the currently loaded image."""
    path: Optional[str] = None
    width: int = 0
    height: int = 0


class ImageModel:
    """Stores original, current, and last-saved image states."""

    def __init__(self) -> None:
        self.original: Optional[np.ndarray] = None
        self.current: Optional[np.ndarray] = None
        self.last_saved: Optional[np.ndarray] = None  # snapshot of current at last save
        self.info: ImageInfo = ImageInfo()
        self.dirty: bool = False

    def has_image(self) -> bool:
        return self.current is not None

    def set_original(self, img: np.ndarray, path: Optional[str] = None) -> None:
        """Set original and current from loaded file."""
        self.original = img.copy()
        self.last_saved = None
        self.set_current(img.copy(), path=path, dirty=False)

    def set_current(self, img: np.ndarray, path: Optional[str] = None, dirty: bool = True) -> None:
        """Set current image and update metadata."""
        self.current = img
        h, w = img.shape[:2]
        self.info.width = w
        self.info.height = h
        if path is not None:
            self.info.path = path
        self.dirty = dirty

    def mark_saved(self) -> None:
        """Record the current image as last-saved snapshot."""
        if self.current is not None:
            self.last_saved = self.current.copy()
        self.dirty = False
