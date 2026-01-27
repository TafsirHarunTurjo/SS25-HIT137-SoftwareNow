"""Undo/Redo history manager.

Stores image states as numpy arrays. Provides a clean API for undo/redo.
"""

from __future__ import annotations

from typing import Optional, List
import numpy as np


class HistoryManager:
    """Manages undo/redo stacks for image states."""

    def __init__(self) -> None:
        self._undo: List[np.ndarray] = []
        self._redo: List[np.ndarray] = []

    def clear(self) -> None:
        """Clear all history."""
        self._undo.clear()
        self._redo.clear()

    def clear_redo(self) -> None:
        """Clear redo history when a new action occurs."""
        self._redo.clear()

    def undo_count(self) -> int:
        return len(self._undo)

    def redo_count(self) -> int:
        return len(self._redo)

    def push_undo(self, img: np.ndarray) -> None:
        """Push a state onto the undo stack."""
        if img is None:
            return
        self._undo.append(img.copy())

    def undo(self, current: np.ndarray) -> Optional[np.ndarray]:
        """Undo to the previous state.

        Moves current -> redo stack and returns previous state.
        """
        if not self._undo:
            return None
        if current is not None:
            self._redo.append(current.copy())
        return self._undo.pop()

    def redo(self, current: np.ndarray) -> Optional[np.ndarray]:
        """Redo to the next state.

        Moves current -> undo stack and returns next state.
        """
        if not self._redo:
            return None
        if current is not None:
            self._undo.append(current.copy())
        return self._redo.pop()
