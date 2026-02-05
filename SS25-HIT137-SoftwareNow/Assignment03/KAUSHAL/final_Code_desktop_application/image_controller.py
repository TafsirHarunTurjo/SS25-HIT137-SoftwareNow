
"""
Image Controller Module

Main application controller that coordinates all components.
Demonstrates OOP concepts: MVC Pattern, Class Interaction, Event Handling.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from typing import Optional, Tuple, Dict, Any
import cv2
import numpy as np

from image_model import ImageModel
from image_view import ImageCanvasView
from effects_processor import EffectsProcessor
from theme_manager import ThemeManager


class ImageController:
    """
    Main controller for the Photoshop mini application.
    Demonstrates Model-View-Controller pattern and class interaction.
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize the controller and setup UI"""
        self.root = root
        self.root.title("Photoshop Photoshop Mini Application")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Initialize components - demonstrates composition
        self.model = ImageModel()
        self.effects = EffectsProcessor()
        self.theme_manager = ThemeManager()
        
        # Tool state - demonstrates encapsulation with tkinter variables
        self.current_tool = tk.StringVar(value="select")
        self.brush_size = tk.IntVar(value=10)
        self.brush_color = "#ff3b30"
        self.text_content = tk.StringVar(value="Sample Text")
        self.text_size = tk.IntVar(value=24)
        
        # Adjustment state 
        self.adjustment_values = {
            "blur": tk.IntVar(value=0),
            "brightness": tk.IntVar(value=0),
            "contrast": tk.DoubleVar(value=1.0),
            "gamma": tk.DoubleVar(value=1.0),
            "saturation": tk.IntVar(value=100),
            "zoom": tk.DoubleVar(value=100.0),  # Zoom slider (percentage)
        }
        
        # View settings
        self.zoom_level = tk.DoubleVar(value=1.0)
        self.auto_apply = tk.BooleanVar(value=True)
        
        # Tool runtime state - demonstrates private attributes
        self._is_drawing = False
        self._last_point: Optional[Tuple[int, int]] = None
        self._crop_start: Optional[Tuple[int, int]] = None
        self._crop_end: Optional[Tuple[int, int]] = None
        
        
        self._active_sliders = set()  # Track which sliders are being actively adjusted
        self._preview_created = False  # Track if preview has been created
        
        # Build UI
        self._create_ui()
        self._bind_events()
        self._apply_theme()
        
        # Initial status
        self._update_status("Ready. Open an image to begin.")
    
    # UI CONSTRUCTION 
    def _create_ui(self):
        """Create the main user interface"""
        # Menu bar
        self._create_menu_bar()
        
        # Toolbar
        self._create_toolbar()
        
        # Main content area
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left control panel - Tools only
        self._create_tools_section(main_frame)
        
        # Middle image area - with paned window
        self._create_middle_image_area(main_frame)
        
        # Right panel - Filters and adjustments
        right_panel = tk.Frame(main_frame, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # Right panel sections
        self._create_adjustments_section(right_panel)  # Adjustments at the top
        self._create_filters_section(right_panel)       # Filters below adjustments
        self._create_transform_section(right_panel)     # Transform below filters
        
        # Status bar
        self._create_status_bar()
    
    def _create_middle_image_area(self, parent):
        """Create middle area with paned window for original and edited views"""
        middle_frame = tk.Frame(parent)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create paned window for resizable split
        self.paned_window = tk.PanedWindow(
            middle_frame, 
            orient=tk.HORIZONTAL, 
            sashwidth=10,
            sashrelief=tk.RAISED,
            showhandle=True
        )
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for each view
        original_frame = tk.Frame(self.paned_window)
        edited_frame = tk.Frame(self.paned_window)
        
        # Create image views
        self.original_view = ImageCanvasView(original_frame, "Original Image")
        self.edited_view = ImageCanvasView(edited_frame, "Edited Image")
        
        # Pack views in their frames
        self.original_view.frame.pack(fill=tk.BOTH, expand=True)
        self.edited_view.frame.pack(fill=tk.BOTH, expand=True)
        
        # Add frames to paned window with initial weights
        self.paned_window.add(original_frame, minsize=200, stretch="always")
        self.paned_window.add(edited_frame, minsize=200, stretch="always")
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open...", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_image)
        file_menu.add_separator()
        file_menu.add_command(label="Export...", command=self.export_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset Image", command=self.reset_image)
        edit_menu.add_command(label="Reset Adjustments", command=self.reset_adjustments)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Fit to Window", command=self.fit_to_window)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        for theme_name in self.theme_manager.get_theme_names():
            theme_menu.add_command(
                label=theme_name,
                command=lambda n=theme_name: self.change_theme(n)
            )
        theme_menu.add_separator()
        theme_menu.add_command(label="Custom Theme...", command=self.create_custom_theme)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Select Tool", command=lambda: self.set_tool("select"))
        tools_menu.add_command(label="Brush Tool", command=lambda: self.set_tool("brush"))
        tools_menu.add_command(label="Eraser Tool", command=lambda: self.set_tool("eraser"))
        tools_menu.add_command(label="Crop Tool", command=lambda: self.set_tool("crop"))
        tools_menu.add_command(label="Text Tool", command=lambda: self.set_tool("text"))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Shortcuts", command=self.show_shortcuts)
        
        # Add menus to menubar
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="View", menu=view_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _create_toolbar(self):
        """Create the toolbar with common actions"""
        toolbar = tk.Frame(self.root, height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Toolbar buttons
        toolbar_buttons = [
            ("📁 Open", self.open_image),
            ("💾 Save", self.save_image),
            ("↶ Undo", self.undo),
            ("↷ Redo", self.redo),
            ("🔄 Reset", self.reset_image),
            ("🔍 Fit", self.fit_to_window),
            ("🎨 Theme", lambda: self.create_custom_theme()),
        ]
        
        for text, command in toolbar_buttons:
            btn = tk.Button(
                toolbar, 
                text=text, 
                command=command,
                relief=tk.RAISED,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Auto-apply checkbox
        tk.Checkbutton(
            toolbar,
            text="Auto-apply adjustments",
            variable=self.auto_apply,
            onvalue=True,
            offvalue=False
        ).pack(side=tk.RIGHT, padx=10)
    
    def _create_tools_section(self, parent: tk.Widget):
        """Create tools section in control panel"""
        control_panel = tk.Frame(parent, width=300)
        control_panel.pack(side=tk.LEFT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        frame = tk.LabelFrame(control_panel, text="Tools", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Tool selection
        tools = [
            ("Select Tool", "select"),
            ("Brush Tool", "brush"),
            ("Eraser Tool", "eraser"),
            ("Crop Tool", "crop"),
            ("Text Tool", "text"),
        ]
        
        for label, value in tools:
            tk.Radiobutton(
                frame,
                text=label,
                variable=self.current_tool,
                value=value,
                command=self._on_tool_changed
            ).pack(anchor=tk.W, pady=2)
        
        # Brush controls
        brush_frame = tk.Frame(frame)
        brush_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(brush_frame, text="Brush Size:").pack(side=tk.LEFT)
        tk.Scale(
            brush_frame,
            from_=1,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.brush_size,
            showvalue=True
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Color picker
        color_frame = tk.Frame(frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            color_frame,
            text="Pick Color",
            command=self.pick_color
        ).pack(side=tk.LEFT)
        
        self.color_preview = tk.Label(
            color_frame,
            text="   ",
            bg=self.brush_color,
            relief=tk.SUNKEN,
            bd=2,
            width=8
        )
        self.color_preview.pack(side=tk.LEFT, padx=10)
        
        # Text controls
        text_frame = tk.Frame(frame)
        text_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(text_frame, text="Text Size:").pack(side=tk.LEFT)
        tk.Scale(
            text_frame,
            from_=10,
            to=72,
            orient=tk.HORIZONTAL,
            variable=self.text_size,
            showvalue=True
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Crop actions
        crop_frame = tk.Frame(frame)
        crop_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            crop_frame,
            text="Apply Crop",
            command=self.apply_crop
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(
            crop_frame,
            text="Cancel Crop",
            command=self.cancel_crop
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    def _create_adjustments_section(self, parent: tk.Widget):
        """Create adjustments section with 6 sliders (5 image + 1 zoom) - REMOVED sharpen"""
        frame = tk.LabelFrame(parent, text="Adjustments", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 6 adjustment sliders with proper ranges
        adjustments = [
            ("Blur", "blur", 0, 31, 1),
            ("Brightness", "brightness", -100, 100, 1),
            ("Contrast", "contrast", 0.1, 3.0, 0.1),
            ("Gamma", "gamma", 0.1, 3.0, 0.1),
            ("Saturation", "saturation", 0, 200, 1),
            ("Zoom (%)", "zoom", 10, 300, 1),
        ]
        
        self.sliders = {}  # Store slider references
        
        for label, var_name, min_val, max_val, resolution in adjustments:
            row = tk.Frame(frame)
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(row, text=label, width=12, anchor=tk.W).pack(side=tk.LEFT)
            
            var = self.adjustment_values[var_name]
            slider = tk.Scale(
                row,
                from_=min_val,
                to=max_val,
                resolution=resolution,
                orient=tk.HORIZONTAL,
                variable=var,
                showvalue=True,
                command=lambda v, n=var_name: self._on_slider_change(n, v),
                length=250
            )
            slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            
            # Store slider reference
            self.sliders[var_name] = slider
            
            # Bind events for image adjustments
            if var_name != "zoom":
                slider.bind("<ButtonPress-1>", lambda e, n=var_name: self._on_slider_start(n))
                slider.bind("<ButtonRelease-1>", lambda e, n=var_name: self._on_slider_end(n))
    
    def _create_filters_section(self, parent: tk.Widget):
        """Create filters section with all 8 required filters"""
        frame = tk.LabelFrame(parent, text="Quick Filters", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # All filters
        filters = [
            ("Grayscale", self.apply_grayscale),
            ("Edge Detection", self.apply_edge_detection),
            ("Sepia Tone", self.apply_sepia),
            ("Invert Colors", self.apply_invert),
            ("Pencil Sketch", self.apply_sketch),
            ("Emboss", self.apply_emboss),
            ("Boundary Extract", self.apply_boundary_extraction),
            ("Black & White", self.apply_black_white),
        ]
        
        # Create 2 columns for filters
        left_column = tk.Frame(frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        right_column = tk.Frame(frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=2)
        
        # Distribute filters between columns
        for i, (label, command) in enumerate(filters):
            column = left_column if i < 4 else right_column
            btn = tk.Button(
                column,
                text=label,
                command=command,
                height=2,
                width=15
            )
            btn.pack(fill=tk.X, pady=2)
    
    def _create_transform_section(self, parent: tk.Widget):
        """Create transform section with rotation, flip, resize"""
        frame = tk.LabelFrame(parent, text="Transform", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Rotation
        rotation_frame = tk.Frame(frame)
        rotation_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(rotation_frame, text="Rotation:").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            rotation_frame,
            text="90°",
            command=lambda: self.rotate_image(90),
            width=5
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            rotation_frame,
            text="180°",
            command=lambda: self.rotate_image(180),
            width=5
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            rotation_frame,
            text="270°",
            command=lambda: self.rotate_image(270),
            width=5
        ).pack(side=tk.LEFT, padx=2)
        
        # Flipping
        flip_frame = tk.Frame(frame)
        flip_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(flip_frame, text="Flip:").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            flip_frame,
            text="Horizontal",
            command=lambda: self.flip_image("horizontal"),
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            flip_frame,
            text="Vertical",
            command=lambda: self.flip_image("vertical"),
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        # Resize
        resize_frame = tk.Frame(frame)
        resize_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            resize_frame,
            text="Resize...",
            command=self.resize_dialog
        ).pack(fill=tk.X)
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # EVENT HANDLING 
    def _bind_events(self):
        """Bind keyboard and mouse events"""
        # Keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-r>", lambda e: self.reset_image())
        self.root.bind("<Control-0>", lambda e: self.fit_to_window())
        
        # Tool shortcuts
        self.root.bind("<KeyPress-b>", lambda e: self.set_tool("brush"))
        self.root.bind("<KeyPress-e>", lambda e: self.set_tool("eraser"))
        self.root.bind("<KeyPress-c>", lambda e: self.set_tool("crop"))
        self.root.bind("<KeyPress-t>", lambda e: self.set_tool("text"))
        self.root.bind("<KeyPress-v>", lambda e: self.set_tool("select"))
        
        # Mouse events for edited view
        self.edited_view.canvas.bind("<ButtonPress-1>", self._on_canvas_press)
        self.edited_view.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.edited_view.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
    
    def _on_tool_changed(self):
        """Handle tool change"""
        tool = self.current_tool.get()
        self._update_status(f"Tool: {tool.capitalize()}")
        
        # Clear overlays when switching from crop
        if tool != "crop":
            self.cancel_crop()
        
        # Clear drawing state
        self._is_drawing = False
        self._last_point = None
        
        # Commit any pending drawing
        if tool not in ["brush", "eraser"] and self.model._drawing_buffer is not None:
            self.model.commit_drawing()
            self._refresh_views()
    
    # SLIDER HANDLING 
    def _on_slider_start(self, slider_name: str):
        """Start slider adjustment for image adjustments (not zoom)"""
        if not self.model.has_image:
            return
        
        print(f"Slider {slider_name} started")
        self._active_sliders.add(slider_name)
        
        if not self.model.preview_active and slider_name != "zoom":
            # Start a new preview session
            self.model.begin_preview()
            self._preview_created = True
            print(f"Started preview for {slider_name}")
    
    def _on_slider_change(self, slider_name: str, value: str):
        """Handle slider change - FIXED for all 6 sliders"""
        if not self.model.has_image:
            return
        
        try:
            # Parse value based on slider type
            if slider_name in ["contrast", "gamma", "zoom"]:
                parsed_value = float(value)
            else:
                parsed_value = int(float(value))
            
            if slider_name == "zoom":
                # Handle zoom slider - update view zoom without affecting image
                zoom = parsed_value / 100.0
                self.zoom_level.set(zoom)
                self.model.current_zoom = zoom
                self.original_view.set_zoom(zoom)
                self.edited_view.set_zoom(zoom)
                self._refresh_views()
            else:
                # Handle image adjustment sliders
                if slider_name in self._active_sliders and self.model.preview_active:
                    # Update model adjustment
                    self.model.update_adjustment(slider_name, parsed_value)
                    
                    # Get all current slider values (including blur) - FIXED: Now includes blur
                    adjustments = {
                        "blur": int(self.adjustment_values["blur"].get()),  # Make sure it's an integer
                        "brightness": int(self.adjustment_values["brightness"].get()),
                        "contrast": float(self.adjustment_values["contrast"].get()),
                        "gamma": float(self.adjustment_values["gamma"].get()),
                        "saturation": int(self.adjustment_values["saturation"].get()),
                    }
                    
                    print(f"Applying adjustments: {adjustments}")
                    
                    # Apply all adjustments together - FIXED: Now passes correct adjustments
                    if self.model._preview_base is not None:
                        preview_image = self.effects.render_adjustments(
                            self.model._preview_base,
                            adjustments
                        )
                        if preview_image is not None:
                            self.model.update_preview(preview_image)
                            self._refresh_views()
            
        except ValueError as e:
            print(f"Error parsing slider value {slider_name}={value}: {e}")
    
    def _on_slider_end(self, slider_name: str):
        """End slider adjustment for image adjustments (not zoom)"""
        if not self.model.has_image:
            return
        
        print(f"Slider {slider_name} ended")
        
        if slider_name != "zoom":
            self._active_sliders.discard(slider_name)
            
            if self.model.preview_active and self._preview_created:
                if self.auto_apply.get():
                    # Apply the changes
                    self.model.commit_preview()
                    print(f"Adjustments applied for {slider_name}")
                else:
                    # Clear preview if not auto-applying
                    self.model.clear_preview()
                    print("Adjustment preview cleared")
                
                self._preview_created = False
                self._refresh_views()
    
    def _on_canvas_press(self, event):
        """Handle canvas mouse press"""
        if not self.model.has_image:
            return
        
        img_coords = self.edited_view.canvas_to_image_coords(event.x, event.y)
        if img_coords is None:
            return
        
        x, y = img_coords
        tool = self.current_tool.get()
        
        if tool == "brush":
            self._start_brush_stroke(x, y)
        elif tool == "eraser":
            self._start_eraser_stroke(x, y)
        elif tool == "crop":
            self._start_crop_selection(x, y)
        elif tool == "text":
            self._add_text(x, y)
    
    def _on_canvas_drag(self, event):
        """Handle canvas mouse drag"""
        if not self.model.has_image:
            return
        
        img_coords = self.edited_view.canvas_to_image_coords(event.x, event.y)
        if img_coords is None:
            return
        
        x, y = img_coords
        tool = self.current_tool.get()
        
        if tool == "brush" and self._is_drawing:
            self._continue_brush_stroke(x, y)
        elif tool == "eraser" and self._is_drawing:
            self._continue_eraser_stroke(x, y)
        elif tool == "crop" and self._crop_start is not None:
            self._update_crop_selection(x, y)
    
    def _on_canvas_release(self, event):
        """Handle canvas mouse release"""
        if not self.model.has_image:
            return
        
        tool = self.current_tool.get()
        
        if tool in ["brush", "eraser"]:
            self._end_drawing_stroke()
        elif tool == "crop":
            self._end_crop_selection()
    
    # TOOL IMPLEMENTATIONS 
    def _start_brush_stroke(self, x: int, y: int):
        """Start a brush stroke"""
        self._is_drawing = True
        self._last_point = (x, y)
        
        # Draw initial point
        color = self._hex_to_bgr(self.brush_color)
        size = self.brush_size.get()
        self.model.start_drawing()
        self.model.draw_point(x, y, color, size)
        self._refresh_views()
    
    def _continue_brush_stroke(self, x: int, y: int):
        """Continue a brush stroke"""
        if self._last_point is None:
            return
        
        x1, y1 = self._last_point
        color = self._hex_to_bgr(self.brush_color)
        size = self.brush_size.get()
        
        # Draw line between points
        self.model.draw_line(x1, y1, x, y, color, size)
        self._last_point = (x, y)
        self._refresh_views()
    
    def _end_drawing_stroke(self):
        """End the drawing stroke"""
        self._is_drawing = False
        self._last_point = None
        self.model.commit_drawing()
        self._refresh_views()
    
    def _start_eraser_stroke(self, x: int, y: int):
        """Start an eraser stroke"""
        self._is_drawing = True
        self._last_point = (x, y)
        
        # Draw initial point (white for eraser)
        size = self.brush_size.get()
        self.model.start_drawing()
        self.model.draw_point(x, y, (255, 255, 255), size)
        self._refresh_views()
    
    def _continue_eraser_stroke(self, x: int, y: int):
        """Continue an eraser stroke"""
        if self._last_point is None:
            return
        
        x1, y1 = self._last_point
        size = self.brush_size.get()
        
        # Draw white line (eraser)
        self.model.draw_line(x1, y1, x, y, (255, 255, 255), size)
        self._last_point = (x, y)
        self._refresh_views()
    
    def _start_crop_selection(self, x: int, y: int):
        """Start crop selection"""
        self._crop_start = (x, y)
        self._crop_end = (x, y)
        self.edited_view.draw_rectangle(x, y, x, y)
    
    def _update_crop_selection(self, x: int, y: int):
        """Update crop selection rectangle"""
        if self._crop_start is None:
            return
        
        self._crop_end = (x, y)
        x1, y1 = self._crop_start
        self.edited_view.draw_rectangle(x1, y1, x, y)
    
    def _end_crop_selection(self):
        """End crop selection"""
        if self._crop_start is not None and self._crop_end is not None:
            x1, y1 = self._crop_start
            x2, y2 = self._crop_end
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            self._update_status(f"Crop selection: {width}×{height} pixels")
    
    def _add_text(self, x: int, y: int):
        """Add text at specified location"""
        text = simpledialog.askstring("Add Text", "Enter text:", initialvalue=self.text_content.get())
        if not text:
            return
        
        self.text_content.set(text)
        self.model._push_state()
        
        # Convert hex to BGR
        color = self._hex_to_bgr(self.brush_color)
        size = self.text_size.get()
        
        # Add text to image
        cv2.putText(
            self.model._committed,
            text,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            size / 20.0,  # Scale factor
            color,
            max(1, size // 10),
            cv2.LINE_AA
        )
        
        self._refresh_views()
        self._update_status(f"Text added: {text}")
    
    # FILE OPERATIONS 
    def open_image(self):
        """Open an image file"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Open Image",
            filetypes=filetypes
        )
        
        if not filepath:
            return
        
        if self.model.load(filepath):
            self._refresh_views()
            self.reset_adjustment_sliders()
            self.cancel_crop()
            self.fit_to_window()
            self._update_status(f"Opened: {self.model.filename}")
        else:
            messagebox.showerror("Error", "Failed to open image file.")
    
    def save_image(self):
        """Save the current image"""
        if not self.model.has_image:
            messagebox.showwarning("No Image", "No image to save.")
            return
        
        try:
            if self.model.filepath is None:
                self.save_as_image()
            else:
                if self.model.save():
                    self._update_status(f"Saved: {self.model.filename}")
                else:
                    messagebox.showerror("Error", "Failed to save image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def save_as_image(self):
        """Save the current image with a new filename"""
        if not self.model.has_image:
            messagebox.showwarning("No Image", "No image to save.")
            return
        
        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=filetypes,
            initialfile=self.model.filename
        )
        
        if not filepath:
            return
        
        try:
            if self.model.save(filepath):
                self._update_status(f"Saved as: {self.model.filename}")
            else:
                messagebox.showerror("Error", "Failed to save image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def export_image(self):
        """Export image in different formats"""
        self.save_as_image()
    
    # EDIT OPERATIONS 
    def undo(self):
        """Undo the last operation"""
        if self.model.undo():
            self._refresh_views()
            self._sync_adjustment_sliders()
            # Update zoom from model
            self.zoom_level.set(self.model.current_zoom)
            self.adjustment_values["zoom"].set(self.model.current_zoom * 100)
            self._update_status("Undo performed")
    
    def redo(self):
        """Redo the last undone operation"""
        if self.model.redo():
            self._refresh_views()
            self._sync_adjustment_sliders()
            # Update zoom from model
            self.zoom_level.set(self.model.current_zoom)
            self.adjustment_values["zoom"].set(self.model.current_zoom * 100)
            self._update_status("Redo performed")
    
    def reset_image(self):
        """Reset image to original state - FIXED zoom reset"""
        if not self.model.has_image:
            return
        
        if messagebox.askyesno("Reset Image", "Reset image to original state?"):
            self.model.reset_to_original()
            self._refresh_views()
            self.reset_adjustment_sliders()
            self.cancel_crop()
            
            # Reset zoom views
            self.original_view.set_zoom(1.0)
            self.edited_view.set_zoom(1.0)
            self._update_status("Image reset to original")
    
    # ADJUSTMENT OPERATIONS 
    def reset_adjustments(self):
        """Reset all adjustments"""
        self.reset_adjustment_sliders()
        if self.model.preview_active:
            self.model.clear_preview()
            self._refresh_views()
        self._update_status("Adjustments reset")
    
    def reset_adjustment_sliders(self):
        """Reset adjustment sliders to default values - FIXED"""
        defaults = {
            "blur": 0,
            "brightness": 0,
            "contrast": 1.0,
            "gamma": 1.0,
            "saturation": 100,
            "zoom": 100.0,
        }
        
        for name, value in defaults.items():
            if name in self.adjustment_values:
                self.adjustment_values[name].set(value)
        
        # model adjustments
        self.model.reset_adjustments()
        
        # views with default zoom
        self.zoom_level.set(1.0)
        self.original_view.set_zoom(1.0)
        self.edited_view.set_zoom(1.0)
        self.model.current_zoom = 1.0
        
        print("All sliders reset to defaults")
    
    def _sync_adjustment_sliders(self):
        """Sync sliders with model's current adjustments"""
        for name, value in self.model.adjustments.items():
            if name in self.adjustment_values:
                self.adjustment_values[name].set(value)
    
    # FILTER OPERATIONS 
    def apply_grayscale(self):
        """Apply grayscale filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_grayscale(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Grayscale")
    
    def apply_sepia(self):
        """Apply sepia filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_sepia(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Sepia")
    
    def apply_invert(self):
        """Apply invert colors filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_invert(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Invert Colors")
    
    def apply_emboss(self):
        """Apply emboss filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_emboss(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Emboss")
    
    def apply_sketch(self):
        """Apply pencil sketch filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_sketch(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Pencil Sketch")
    
    def apply_edge_detection(self):
        """Apply edge detection filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_edge_detection(
            self.model._committed, 50, 150
        )
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Edge Detection")
    
    def apply_boundary_extraction(self):
        """Apply boundary extraction filter"""
        if not self.model.has_image:
            return
        
        self.model._push_state()
        processed = self.effects.apply_boundary_extraction(self.model._committed)
        self.model._committed = processed
        self._refresh_views()
        self._update_status("Applied: Boundary Extraction")
    
    def apply_black_white(self):
        """Apply black and white threshold filter"""
        if not self.model.has_image:
            return
        
        threshold = simpledialog.askinteger(
            "Black & White",
            "Enter threshold (0-255):",
            initialvalue=127,
            minvalue=0,
            maxvalue=255
        )
        
        if threshold is None:
            return
        
        self.model._push_state()
        processed = self.effects.apply_black_white(
            self.model._committed, threshold
        )
        self.model._committed = processed
        self._refresh_views()
        self._update_status(f"Applied: Black & White (threshold={threshold})")
    
    # TRANSFORM OPERATIONS 
    def rotate_image(self, angle: int):
        """Rotate the image"""
        if not self.model.has_image:
            return
        
        self.model.rotate(angle)
        self._refresh_views()
        self._update_status(f"Rotated: {angle}°")
    
    def flip_image(self, mode: str):
        """Flip the image horizontally or vertically"""
        if not self.model.has_image:
            return
        
        self.model.flip(mode)
        self._refresh_views()
        self._update_status(f"Flipped: {mode}")
    
    def resize_dialog(self):
        """Open resize dialog"""
        if not self.model.has_image:
            messagebox.showwarning("No Image", "No image to resize.")
            return
        
        current_dims = self.model.image_dimensions
        if current_dims is None:
            return
        
        current_h, current_w = current_dims
        
        # Ask for new dimensions
        new_w = simpledialog.askinteger(
            "Resize",
            f"New width (current: {current_w}):",
            initialvalue=current_w,
            minvalue=1
        )
        
        if new_w is None:
            return
        
        new_h = simpledialog.askinteger(
            "Resize",
            f"New height (current: {current_h}):",
            initialvalue=current_h,
            minvalue=1
        )
        
        if new_h is None:
            return
        
        # Ask for confirmation if resizing to very small or large size
        if new_w < 50 or new_h < 50 or new_w > 5000 or new_h > 5000:
            if not messagebox.askyesno("Confirm Resize", 
                                      f"Resize to {new_w}×{new_h}? This may affect image quality."):
                return
        
        # Resize image
        self.model.resize(new_w, new_h)
        self._refresh_views()
        self._update_status(f"Resized to: {new_w}×{new_h}")
    
    # TOOL OPERATIONS 
    def set_tool(self, tool_name: str):
        """Set the current tool"""
        self.current_tool.set(tool_name)
        self._on_tool_changed()
    
    def pick_color(self):
        """Open color picker dialog"""
        color = colorchooser.askcolor(
            title="Pick Color",
            initialcolor=self.brush_color
        )[1]
        
        if color:
            self.brush_color = color
            self.color_preview.config(bg=color)
            self._update_status(f"Color selected: {color}")
    
    def apply_crop(self):
        """Apply crop selection"""
        if not self.model.has_image:
            return
        
        if self._crop_start is None or self._crop_end is None:
            messagebox.showinfo("Crop", "Please select an area first.")
            return
        
        x1, y1 = self._crop_start
        x2, y2 = self._crop_end
        
        # Ensure proper ordering
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        
        # Calculate dimensions
        width = x2 - x1
        height = y2 - y1
        
        if width < 10 or height < 10:
            messagebox.showwarning("Crop", "Selection is too small. Minimum 10x10 pixels required.")
            return
        
        if messagebox.askyesno("Confirm Crop", f"Crop to {width}×{height} pixels?"):
            self.model.crop(x1, y1, x2, y2)
            self.cancel_crop()
            self._refresh_views()
            self._update_status("Crop applied")
    
    def cancel_crop(self):
        """Cancel crop selection"""
        self._crop_start = None
        self._crop_end = None
        self.edited_view.clear_overlays()
        self._update_status("Crop cancelled")
    
    #  VIEW OPERATIONS 
    def fit_to_window(self):
        """Fit image to window"""
        if not self.model.has_image:
            return
        
        self.original_view.fit_to_window()
        self.edited_view.fit_to_window()
        
        # Update zoom slider and model
        zoom = self.edited_view.get_zoom()
        self.zoom_level.set(zoom)
        self.adjustment_values["zoom"].set(zoom * 100)
        self.model.current_zoom = zoom
        self._update_status("Fitted to window")
    
    # THEME OPERATIONS 
    def change_theme(self, theme_name: str):
        """Change application theme"""
        self.theme_manager.set_theme(theme_name)
        self._apply_theme()
        self._update_status(f"Theme: {theme_name}")
    
    def create_custom_theme(self):
        """Create a custom theme"""
        bg_color = colorchooser.askcolor(
            title="Select Background Color",
            initialcolor=self.theme_manager.theme["bg"]
        )[1]
        
        if not bg_color:
            return
        
        accent_color = colorchooser.askcolor(
            title="Select Accent Color",
            initialcolor=self.theme_manager.theme["accent"]
        )[1]
        
        if not accent_color:
            return
        
        custom_theme = self.theme_manager.create_custom_theme(bg_color, accent_color)
        self.theme_manager.theme = custom_theme
        self.theme_manager.current_theme = "Custom"
        self._apply_theme()
        self._update_status("Theme: Custom")
    
    def _apply_theme(self):
        """Apply current theme to all UI elements"""
        theme = self.theme_manager.theme
        
        # Apply theme recursively
        self._apply_theme_to_widget(self.root, theme)
        
        # Apply to specific views
        self.original_view.apply_theme(theme)
        self.edited_view.apply_theme(theme)
        
        # Update color preview
        self.color_preview.config(bg=self.brush_color)
        
        # Apply theme to paned window
        self.paned_window.config(bg=theme.get("bg", "#1f1f1f"))
    
    def _apply_theme_to_widget(self, widget: tk.Widget, theme: dict):
        """Recursively apply theme to widget and children"""
        self.theme_manager.apply_to_widget(widget, theme)
        
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, theme)
    
    # HELP OPERATIONS 
    def show_about(self):
        """Show about dialog"""
        about_text = """Photoshop Professional - Advanced Image Editor
        
A comprehensive image editing application built with:
• Python 3
• Tkinter (GUI Framework)
• OpenCV (Image Processing)
• Pillow (Image Display)
• NumPy (Numerical Computing)

Features:
• Multiple image formats support (PNG, JPG, BMP, etc.)
• Non-destructive editing with undo/redo
• Real-time adjustment previews
• Various filters and effects
• Drawing tools (Brush, Eraser)
• Text overlay
• Image transformations (Rotate, Flip, Resize, Crop)
• Resizable split view for comparison
• Custom themes and UI styling
• Keyboard shortcuts for productivity
        
"""
        
        messagebox.showinfo("About", about_text)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts = """KEYBOARD SHORTCUTS 

FILE OPERATIONS:
Ctrl+O - Open Image
Ctrl+S - Save Image

EDIT OPERATIONS:
Ctrl+Z - Undo
Ctrl+Y - Redo
Ctrl+R - Reset Image

VIEW OPERATIONS:
Ctrl+0 - Fit to Window

TOOLS:
B - Brush Tool
E - Eraser Tool
C - Crop Tool
T - Text Tool
V - Select Tool

FILTERS:
G - Grayscale
I - Invert Colors
S - Sepia Tone
P - Pencil Sketch
E - Edge Detection


        
SPLIT VIEW:
Drag center bar to resize views"""
        
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    # UTILITY METHODS 
    @staticmethod
    def _hex_to_bgr(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to BGR tuple for OpenCV.
        
        Args:
            hex_color: Color in hex format (#RRGGBB)
            
        Returns:
            Tuple[int, int, int]: BGR color tuple
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return (0, 0, 255)  # Default blue
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return (b, g, r)  # OpenCV uses BGR order
    
    def _refresh_views(self):
        """Refresh both image views and update status bar"""
        if self.model.has_image:
            original_img = self.model._original
            display_img = self.model.get_display_image()
            
            self.original_view.display_image(original_img)
            self.edited_view.display_image(display_img)
            
            # Update status with image info
            if display_img is not None:
                h, w = display_img.shape[:2]
                zoom_percent = int(self.adjustment_values["zoom"].get())
                
                # Get all slider values for status
                blur_val = self.adjustment_values["blur"].get()
                brightness_val = self.adjustment_values["brightness"].get()
                contrast_val = self.adjustment_values["contrast"].get()
                gamma_val = self.adjustment_values["gamma"].get()
                saturation_val = self.adjustment_values["saturation"].get()
                
                self._update_status(
                    f"{self.model.filename} | {w}×{h} pixels | "
                    f"Zoom: {zoom_percent}% | Tool: {self.current_tool.get()} | "
                    f"Blur: {blur_val} | Bright: {brightness_val} | Contrast: {contrast_val:.1f} | "
                    f"Gamma: {gamma_val:.1f} | Sat: {saturation_val}"
                )
        else:
            self.original_view.display_image(None)
            self.edited_view.display_image(None)
    
    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_var.set(f"Status: {message}")
    
    def quit_app(self):
        """Quit the application"""
        if self.model.is_dirty:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Save before quitting?"
            )
            
            if response is None:  # Cancel
                return
            elif response:  # Yes
                self.save_image()
        
        self.root.quit()
