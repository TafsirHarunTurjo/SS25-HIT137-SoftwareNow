"""Undo/Redo history manager.

This manager stores full image states (numpy arrays) for undo/redo.
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
        """Clear undo and redo stacks."""
        self._undo.clear()
        self._redo.clear()

    def clear_redo(self) -> None:
        """Clear redo stack when a new action happens."""
        self._redo.clear()

    def push_undo(self, img: np.ndarray) -> None:
        """Push current state to undo stack."""
        self._undo.append(img.copy())

    def can_undo(self) -> bool:
        return len(self._undo) > 0

    def can_redo(self) -> bool:
        return len(self._redo) > 0

    def undo(self, current: np.ndarray) -> Optional[np.ndarray]:
        """Undo and return previous state; current moves to redo."""
        if not self._undo:
            return None
        self._redo.append(current.copy())
        return self._undo.pop()

    def redo(self, current: np.ndarray) -> Optional[np.ndarray]:
        """Redo and return next state; current moves to undo."""
        if not self._redo:
            return None
        self._undo.append(current.copy())
        return self._redo.pop()

    def counts(self) -> tuple[int, int]:
        """Return (undo_count, redo_count)."""
        return (len(self._undo), len(self._redo))
