"""
Image View Module

Handles image display and canvas operations.
Demonstrates OOP concepts: Inheritance, Encapsulation, Class Interaction.
"""

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any


class BaseView:
    """Base view class - demonstrates inheritance"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self._theme: Dict[str, str] = {}
    
    def apply_theme(self, theme: Dict[str, str]):
        """Apply theme to view"""
        self._theme = theme
        self._update_theme()
    
    def _update_theme(self):
        """Update theme - to be overridden by subclasses"""
        pass


class ImageCanvasView(BaseView):
    """
    Canvas-based image viewer with zoom and coordinate mapping.
    Demonstrates OOP concepts: Inheritance, Encapsulation, Method Overriding.
    """
    
    def __init__(self, parent: tk.Widget, title: str = "Image"):
        """
        Initialize the image canvas view.
        
        Args:
            parent: Parent widget
            title: Title for the view frame
        """
        super().__init__(parent)
        
        # Create main frame
        self.frame = tk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        self.title_label = tk.Label(
            self.frame, 
            text=title, 
            font=("Arial", 11, "bold")
        )
        self.title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Create a container for canvas
        self.canvas_container = tk.Frame(self.frame)
        self.canvas_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Canvas for image display
        self.canvas = tk.Canvas(
            self.canvas_container, 
            bg="#222222", 
            highlightthickness=0,
            cursor="crosshair"  # Crosshair cursor for precise selection
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # State variables with private access - demonstrates encapsulation
        self._tk_image: Optional[ImageTk.PhotoImage] = None
        self._zoom: float = 1.0
        self._image_dimensions: Optional[Tuple[int, int]] = None
        self._current_image: Optional[np.ndarray] = None
        
        # Overlay items
        self._overlay_items = []
    
    def _update_theme(self):
        """Apply theme colors to the view - demonstrates polymorphism"""
        if not self._theme:
            return
        
        self.title_label.config(
            bg=self._theme.get("bg", "#222222"),
            fg=self._theme.get("fg", "#ffffff")
        )
        self.frame.config(bg=self._theme.get("bg", "#222222"))
        self.canvas_container.config(bg=self._theme.get("bg", "#222222"))
        self.canvas.config(bg=self._theme.get("canvas_bg", "#111111"))
    
    def display_image(self, image: Optional[np.ndarray]):
        """
        Display an image on the canvas.
        
        Args:
            image: BGR image array or None to clear
        """
        # Clear previous image
        self.canvas.delete("all")
        self._current_image = None
        
        if image is None:
            return
        
        # Store reference to prevent garbage collection
        self._current_image = image
        
        try:
            # Convert BGR to RGB for PIL
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            # Store original dimensions
            original_width, original_height = pil_image.size
            self._image_dimensions = (original_height, original_width)
            
            # Apply zoom
            new_width = max(1, int(original_width * self._zoom))
            new_height = max(1, int(original_height * self._zoom))
            
            # High-quality resize
            pil_image = pil_image.resize(
                (new_width, new_height), 
                Image.Resampling.LANCZOS
            )
            
            # Convert to PhotoImage
            self._tk_image = ImageTk.PhotoImage(pil_image)
            
            # Clear canvas and create image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self._tk_image, anchor="nw", tags="image")
            
            # Update canvas configuration
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def set_zoom(self, zoom_level: float):
        """Set zoom level and update display"""
        self._zoom = max(0.1, min(3.0, zoom_level))
        if self._current_image is not None:
            self.display_image(self._current_image)
    
    def get_zoom(self) -> float:
        """Get current zoom level"""
        return self._zoom
    
    def fit_to_window(self):
        """Fit image to window size"""
        if self._image_dimensions is None or self._current_image is None:
            return
        
        # Get current canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Use parent frame size if canvas not yet sized
            canvas_width = self.canvas_container.winfo_width()
            canvas_height = self.canvas_container.winfo_height()
        
        if canvas_width <= 10 or canvas_height <= 10:
            # Default size if still too small
            canvas_width = 400
            canvas_height = 300
        
        img_height, img_width = self._image_dimensions
        
        # Calculate zoom to fit with margins
        zoom_x = (canvas_width - 20) / img_width
        zoom_y = (canvas_height - 20) / img_height
        new_zoom = min(zoom_x, zoom_y, 3.0)  # Cap at 300%
        
        self.set_zoom(new_zoom)
    
    def canvas_to_image_coords(self, canvas_x: int, canvas_y: int) -> Optional[Tuple[int, int]]:
        """
        Convert canvas coordinates to image coordinates.
        
        Args:
            canvas_x: X coordinate on canvas
            canvas_y: Y coordinate on canvas
            
        Returns:
            (x, y) in image coordinates or None if outside image
        """
        if self._image_dimensions is None or self._tk_image is None:
            return None
        
        # Convert to image coordinates
        img_x = int(canvas_x / self._zoom)
        img_y = int(canvas_y / self._zoom)
        
        # Check bounds
        img_height, img_width = self._image_dimensions
        if 0 <= img_x < img_width and 0 <= img_y < img_height:
            return img_x, img_y
        
        return None
    
    def image_to_canvas_coords(self, img_x: int, img_y: int) -> Optional[Tuple[int, int]]:
        """
        Convert image coordinates to canvas coordinates.
        
        Args:
            img_x: X coordinate in image
            img_y: Y coordinate in image
            
        Returns:
            (x, y) in canvas coordinates or None if invalid
        """
        if self._image_dimensions is None:
            return None
        
        img_height, img_width = self._image_dimensions
        if not (0 <= img_x < img_width and 0 <= img_y < img_height):
            return None
        
        # Convert to canvas coordinates
        canvas_x = int(img_x * self._zoom)
        canvas_y = int(img_y * self._zoom)
        
        return canvas_x, canvas_y
    
    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, 
                      color: str = "#00ff00", width: int = 2):
        """Draw a rectangle overlay on the image"""
        # Clear previous rectangles
        self.canvas.delete("overlay_rect")
        
        # Convert to canvas coordinates
        p1 = self.image_to_canvas_coords(x1, y1)
        p2 = self.image_to_canvas_coords(x2, y2)
        
        if p1 is None or p2 is None:
            return
        
        cx1, cy1 = p1
        cx2, cy2 = p2
        
        # Draw rectangle
        self.canvas.create_rectangle(
            cx1, cy1, cx2, cy2,
            outline=color,
            width=width,
            tags="overlay_rect"
        )
    
    def clear_overlays(self):
        """Clear all overlay drawings"""
        self.canvas.delete("overlay_rect")
        self.canvas.delete("overlay_circle")
        self.canvas.delete("overlay")