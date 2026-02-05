
"""
Image Model Module

Core image data management with undo/redo functionality.
Demonstrates OOP concepts: Encapsulation, Composition, State Management.
"""

import os
import numpy as np
import cv2
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass


@dataclass
class ImageState:
    """
    Data class representing image state.
    Demonstrates encapsulation and data organization.
    """
    image: np.ndarray
    adjustments: Dict[str, Any]
    filename: str
    filepath: str
    
    def copy(self) -> 'ImageState':
        """Create a deep copy of the state"""
        return ImageState(
            image=self.image.copy() if self.image is not None else None,
            adjustments=self.adjustments.copy(),
            filename=self.filename,
            filepath=self.filepath
        )


class ImageModel:
    """
    Manages image data with comprehensive state tracking.
    Demonstrates OOP concepts: Encapsulation, State Management, Composition.
    """
    
    # Class constants - demonstrates encapsulation
    DEFAULT_ADJUSTMENTS = {
        "blur": 0,
        "brightness": 0,
        "contrast": 1.0,
        "gamma": 1.0,
        "saturation": 100,
    }
    
    def __init__(self):
        """
        Initialize the image model.
        Demonstrates constructor and private attributes.
        """
        # Core image data with private access - demonstrates encapsulation
        self._original: Optional[np.ndarray] = None
        self._committed: Optional[np.ndarray] = None
        self._preview: Optional[np.ndarray] = None
        self._preview_base: Optional[np.ndarray] = None
        
        # Metadata
        self.filename: Optional[str] = None
        self.filepath: Optional[str] = None
        self.is_dirty: bool = False
        
        # State management
        self.undo_stack: List[ImageState] = []
        self.redo_stack: List[ImageState] = []
        
        # Current adjustments
        self.adjustments = self.DEFAULT_ADJUSTMENTS.copy()
        
        # Drawing state for brush and eraser
        self._drawing_buffer: Optional[np.ndarray] = None
        self._is_drawing: bool = False
        
        # Preview state
        self._preview_active: bool = False
        self._slider_changes: Dict[str, Any] = {}
        
        # Store original zoom separately
        self._original_zoom: float = 1.0
        self._current_zoom: float = 1.0
    
    # PROPERTIES 
    @property
    def has_image(self) -> bool:
        """
        Check if an image is loaded.
        Demonstrates property decorator.
        """
        return self._committed is not None
    
    @property
    def image_dimensions(self) -> Optional[Tuple[int, int]]:
        """Get current image dimensions (height, width)"""
        if self._committed is None:
            return None
        return self._committed.shape[:2]
    
    @property
    def preview_active(self) -> bool:
        """Check if preview is currently active"""
        return self._preview_active
    
    @property
    def is_drawing(self) -> bool:
        """Check if currently drawing"""
        return self._is_drawing
    
    @property
    def current_zoom(self) -> float:
        """Get current zoom level"""
        return self._current_zoom
    
    @current_zoom.setter
    def current_zoom(self, value: float):
        """Set current zoom level"""
        self._current_zoom = max(0.1, min(3.0, value))
    
    # FILE OPERATIONS 
    def load(self, filepath: str) -> bool:
        """
        Load an image from file.
        
        Args:
            filepath: Path to the image file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read image using OpenCV
            img = cv2.imread(filepath, cv2.IMREAD_COLOR)
            if img is None:
                print(f"Failed to load image: {filepath}")
                return False
            
            # Store images
            self._original = img.copy()
            self._committed = img.copy()
            self.filename = os.path.basename(filepath)
            self.filepath = filepath
            
            # Reset state
            self.reset_state()
            self.is_dirty = False
            self._original_zoom = 1.0
            self._current_zoom = 1.0
            
            print(f"Successfully loaded image: {self.filename}, size: {img.shape}")
            return True
            
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            return False
    
    def save(self, filepath: Optional[str] = None) -> bool:
        """
        Save the current image.
        
        Args:
            filepath: Optional path to save to (uses current if None)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            save_path = filepath or self.filepath
            if save_path is None:
                print("No filepath specified for saving")
                return False
            
            # Get current display image
            img = self.get_display_image()
            if img is None:
                print("No image to save")
                return False
            
            # Save image
            success = cv2.imwrite(save_path, img)
            
            if success:
                self.filepath = save_path
                self.filename = os.path.basename(save_path)
                self.is_dirty = False
                print(f"Successfully saved image: {self.filename}")
            else:
                print(f"Failed to save image: {save_path}")
                
            return success
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def reset_to_original(self):
        """Reset the image to its original state"""
        if self._original is not None:
            self._committed = self._original.copy()
            self.clear_preview()
            self.reset_adjustments()
            self.clear_history()
            self._drawing_buffer = None
            self._is_drawing = False
            self._current_zoom = 1.0
            self.is_dirty = False
            print("Reset image to original state")
    
    # STATE MANAGEMENT 
    def get_display_image(self) -> Optional[np.ndarray]:
        """
        Get the image that should be displayed.
        Returns preview if active, otherwise committed image.
        """
        if self._preview is not None:
            return self._preview
        
        # Apply drawing buffer if exists
        if self._drawing_buffer is not None and self._committed is not None:
            return self._drawing_buffer
        
        return self._committed
    
    def get_committed_image(self) -> Optional[np.ndarray]:
        """Get the committed image (without preview)"""
        return self._committed
    
    def begin_preview(self):
        """Start a preview session"""
        if self._committed is not None:
            self._preview_base = self._committed.copy()
            self._preview = self._committed.copy()
            self._preview_active = True
            self._slider_changes = self.adjustments.copy()
            print("Started preview session")
    
    def update_preview(self, image: np.ndarray):
        """Update the preview image"""
        self._preview = image
    
    def commit_preview(self):
        """Commit the preview to the main image"""
        if self._preview is not None and self._preview_active:
            self._push_state()
            self._committed = self._preview.copy()
            # Update adjustments with slider changes
            self.adjustments = self._slider_changes.copy()
            self.clear_preview()
            self.is_dirty = True
            print("Committed preview to main image")
    
    def clear_preview(self):
        """Clear the current preview"""
        self._preview = None
        self._preview_base = None
        self._preview_active = False
        self._slider_changes = {}
        print("Cleared preview")
    
    # UNDO/REDO 
    def _create_state(self) -> ImageState:
        """Create current state object - demonstrates encapsulation"""
        return ImageState(
            image=self._committed.copy() if self._committed is not None else None,
            adjustments=self.adjustments.copy(),
            filename=self.filename or "",
            filepath=self.filepath or ""
        )
    
    def _restore_state(self, state: ImageState):
        """Restore from state object"""
        if state.image is not None:
            self._committed = state.image.copy()
        self.adjustments = state.adjustments.copy()
        if state.filename:
            self.filename = state.filename
        if state.filepath:
            self.filepath = state.filepath
    
    def _push_state(self):
        """Push current state to undo stack"""
        if self._committed is not None:
            # Don't push state during drawing (we'll push at the end)
            if not self._is_drawing:
                self.undo_stack.append(self._create_state())
                self.redo_stack.clear()
                print("Pushed state to undo stack")
    
    def undo(self) -> bool:
        """
        Undo the last operation.
        
        Returns:
            bool: True if undo was performed
        """
        if not self.undo_stack:
            print("Nothing to undo")
            return False
        
        # Save current state to redo stack
        if self._committed is not None:
            self.redo_stack.append(self._create_state())
        
        # Restore previous state
        state = self.undo_stack.pop()
        self._restore_state(state)
        
        self.clear_preview()
        self._drawing_buffer = None
        self._is_drawing = False
        self.is_dirty = True
        
        print("Undo performed")
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone operation.
        
        Returns:
            bool: True if redo was performed
        """
        if not self.redo_stack:
            print("Nothing to redo")
            return False
        
        # Save current state to undo stack
        if self._committed is not None:
            self.undo_stack.append(self._create_state())
        
        # Restore redone state
        state = self.redo_stack.pop()
        self._restore_state(state)
        
        self.clear_preview()
        self._drawing_buffer = None
        self._is_drawing = False
        self.is_dirty = True
        
        print("Redo performed")
        return True
    
    def clear_history(self):
        """Clear all undo/redo history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        print("Cleared history")
    
    # ADJUSTMENTS 
    def update_adjustment(self, name: str, value):
        """
        Update a specific adjustment value.
        
        Args:
            name: Adjustment name
            value: New value
        """
        if name in self.adjustments:
            old_value = self.adjustments[name]
            self.adjustments[name] = value
            if self._preview_active:
                self._slider_changes[name] = value
            print(f"Updated adjustment {name}: {old_value} -> {value}")
    
    def reset_adjustments(self):
        """Reset all adjustments to default values"""
        self.adjustments = self.DEFAULT_ADJUSTMENTS.copy()
        print("Reset all adjustments to defaults")
    
    def reset_state(self):
        """Reset model state (used when loading new image)"""
        self.clear_history()
        self.clear_preview()
        self.reset_adjustments()
        self._drawing_buffer = None
        self._is_drawing = False
        self._current_zoom = 1.0
        print("Reset model state")
    
    # IMAGE OPERATIONS =
    def rotate(self, angle: int):
        """
        Rotate the image.
        
        Args:
            angle: Rotation angle (90, 180, or 270)
        """
        if self._committed is None:
            print("No image to rotate")
            return
        
        self._push_state()
        
        # Apply rotation using OpenCV
        if angle == 90:
            self._committed = cv2.rotate(self._committed, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self._committed = cv2.rotate(self._committed, cv2.ROTATE_180)
        elif angle == 270:
            self._committed = cv2.rotate(self._committed, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        self.clear_preview()
        self.reset_adjustments()
        self.is_dirty = True
        print(f"Rotated image by {angle} degrees")
    
    def flip(self, mode: str):
        """
        Flip the image horizontally or vertically.
        
        Args:
            mode: "horizontal" or "vertical"
        """
        if self._committed is None:
            print("No image to flip")
            return
        
        self._push_state()
        
        if mode == "horizontal":
            self._committed = cv2.flip(self._committed, 1)
        elif mode == "vertical":
            self._committed = cv2.flip(self._committed, 0)
        
        self.clear_preview()
        self.reset_adjustments()
        self.is_dirty = True
        print(f"Flipped image {mode}ly")
    
    def resize(self, width: int, height: int):
        """
        Resize the image.
        
        Args:
            width: New width in pixels
            height: New height in pixels
        """
        if self._committed is None:
            print("No image to resize")
            return
        
        if width < 1 or height < 1:
            print(f"Invalid dimensions: {width}x{height}")
            return
        
        self._push_state()
        self._committed = cv2.resize(
            self._committed, 
            (width, height), 
            interpolation=cv2.INTER_AREA
        )
        
        self.clear_preview()
        self.reset_adjustments()
        self.is_dirty = True
        print(f"Resized image to {width}x{height}")
    
    def crop(self, x1: int, y1: int, x2: int, y2: int):
        """
        Crop the image.
        
        Args:
            x1, y1: Top-left coordinates
            x2, y2: Bottom-right coordinates
        """
        if self._committed is None:
            print("No image to crop")
            return
        
        # Ensure coordinates are valid
        h, w = self._committed.shape[:2]
        x1, x2 = sorted((max(0, min(w, x1)), max(0, min(w, x2))))
        y1, y2 = sorted((max(0, min(h, y1)), max(0, min(h, y2))))
        
        if x2 - x1 < 2 or y2 - y1 < 2:
            print(f"Crop area too small: {x2-x1}x{y2-y1}")
            return
        
        self._push_state()
        self._committed = self._committed[y1:y2, x1:x2].copy()
        
        self.clear_preview()
        self.reset_adjustments()
        self.is_dirty = True
        print(f"Cropped image to {x2-x1}x{y2-y1}")
    
    # DRAWING OPERATIONS 
    def start_drawing(self):
        """Start drawing operation"""
        if self._committed is None:
            print("No image to draw on")
            return
        
        # Save state only at the beginning of drawing
        if not self._is_drawing:
            self._push_state()
            self._is_drawing = True
            print("Started drawing operation")
        
        # Create drawing buffer
        self._drawing_buffer = self._committed.copy()
    
    def draw_point(self, x: int, y: int, color: Tuple[int, int, int], size: int):
        """Draw a point on the image"""
        if self._drawing_buffer is None:
            self.start_drawing()
        
        if self._drawing_buffer is None:
            return
        
        cv2.circle(self._drawing_buffer, (x, y), size, color, -1)
        self.is_dirty = True
    
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, 
                  color: Tuple[int, int, int], size: int):
        """Draw a line on the image"""
        if self._drawing_buffer is None:
            self.start_drawing()
        
        if self._drawing_buffer is None:
            return
        
        cv2.line(self._drawing_buffer, (x1, y1), (x2, y2), color, size)
        self.is_dirty = True
    
    def commit_drawing(self):
        """Commit drawing to main image"""
        if self._drawing_buffer is not None and self._committed is not None:
            self._committed = self._drawing_buffer.copy()
            self._drawing_buffer = None
            self._is_drawing = False
            self.is_dirty = True
            print("Committed drawing to main image")
    
    def cancel_drawing(self):
        """Cancel drawing operation"""
        self._drawing_buffer = None
        self._is_drawing = False
        print("Cancelled drawing operation")
