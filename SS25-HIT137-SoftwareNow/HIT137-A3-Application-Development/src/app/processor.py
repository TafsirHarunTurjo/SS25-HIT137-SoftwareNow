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

    def blur(self, img: np.ndarray, intensity: int = 3) -> np.ndarray:
        """Apply Gaussian blur with adjustable intensity (kernel must be odd)."""
        intensity = max(1, int(intensity))
        k = intensity * 2 + 1  # 1->3, 2->5, 3->7 ...
        return cv2.GaussianBlur(img, (k, k), 0)
