"""OpenCV image processing operations for HIT137 A3."""

from __future__ import annotations

import cv2
import numpy as np


class ImageProcessor:
    """Applies image processing operations using OpenCV."""

    def grayscale(self, img: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, img: np.ndarray, intensity: int) -> np.ndarray:
        intensity = int(intensity)
        if intensity <= 0:
            return img.copy()
        k = intensity * 2 + 1  # 1->3, 2->5, ...
        return cv2.GaussianBlur(img, (k, k), 0)

    def edge(self, img: np.ndarray, t1: int = 100, t2: int = 200) -> np.ndarray:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, int(t1), int(t2))
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness(self, img: np.ndarray, beta: int) -> np.ndarray:
        return cv2.convertScaleAbs(img, alpha=1.0, beta=int(beta))

    def adjust_contrast(self, img: np.ndarray, alpha: float) -> np.ndarray:
        return cv2.convertScaleAbs(img, alpha=float(alpha), beta=0)

    def rotate(self, img: np.ndarray, angle: int) -> np.ndarray:
        angle = int(angle)
        if angle == 90:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180:
            return cv2.rotate(img, cv2.ROTATE_180)
        if angle == 270:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        raise ValueError("angle must be 90, 180, or 270")

    def flip(self, img: np.ndarray, mode: str) -> np.ndarray:
        mode = mode.strip().lower()
        if mode == "horizontal":
            return cv2.flip(img, 1)
        if mode == "vertical":
            return cv2.flip(img, 0)
        raise ValueError("mode must be 'horizontal' or 'vertical'")

    def resize(self, img: np.ndarray, width: int, height: int) -> np.ndarray:
        w = int(width)
        h = int(height)
        if w <= 0 or h <= 0:
            raise ValueError("width and height must be > 0")
        return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
