"""Undo/Redo history manager."""

from __future__ import annotations

from typing import Optional, List
import numpy as np


class HistoryManager:
    """Manages undo and redo stacks for image states."""

    def __init__(self) -> None:
        self._undo: List[np.ndarray] = []
        self._redo: List[np.ndarray] = []

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    def push_undo(self, img: np.ndarray) -> None:
        self._undo.append(img.copy())

    def pop_undo(self) -> Optional[np.ndarray]:
        return self._undo.pop() if self._undo else None

    def push_redo(self, img: np.ndarray) -> None:
        self._redo.append(img.copy())

    def pop_redo(self) -> Optional[np.ndarray]:
        return self._redo.pop() if self._redo else None
