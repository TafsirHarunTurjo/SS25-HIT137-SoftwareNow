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
    """Stores original and current image state."""

    def __init__(self) -> None:
        self.original: Optional[np.ndarray] = None
        self.current: Optional[np.ndarray] = None
        self.info: ImageInfo = ImageInfo()
        self.dirty: bool = False

    def set_original(self, img: np.ndarray, path: Optional[str] = None) -> None:
        """Set original + current from a newly loaded image."""
        self.original = img.copy()
        self.set_current(img.copy(), path=path, dirty=False)

    def set_current(self, img: np.ndarray, path: Optional[str] = None, dirty: bool = True) -> None:
        """Update current image and metadata."""
        self.current = img
        h, w = img.shape[:2]
        self.info.width = w
        self.info.height = h
        if path is not None:
            self.info.path = path
        self.dirty = dirty

    def has_image(self) -> bool:
        return self.current is not None
