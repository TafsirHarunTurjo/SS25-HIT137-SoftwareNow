"""OpenCV image processing operations."""

from __future__ import annotations

import cv2
import numpy as np


class ImageProcessor:
    """Applies image processing operations using OpenCV."""

    def grayscale(self, img: np.ndarray) -> np.ndarray:
        """Convert BGR image to grayscale and return as BGR for display consistency."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
