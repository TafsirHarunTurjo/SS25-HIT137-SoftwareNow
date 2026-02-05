# issue(not working perfectly): blur after doing contrast or brightness.
#  can't get back to original blur

# ================== IMPORTS ==================
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import os
import numpy as np


# ================== IMAGE PROCESSOR ==================
class ImageProcessor:
    def __init__(self):
        self._original_image = None
        self._image = None
        self._base_image = None
        self._preview_image = None  # For temporary preview during sliding
        self.filename = None
        self.undo_stack = []
        self.redo_stack = []
        self.slider_changes = {}  # Track slider changes for undo/redo
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}  # Current slider values
        self._preview_base = None  # Base image for previews

    def load_image(self, path):
        self.filename = os.path.basename(path)
        self._original_image = cv2.imread(path)
        self._image = self._original_image.copy()
        self._base_image = self._original_image.copy()  # Base should always be original or committed state
        self._preview_base = self._original_image.copy()
        self._preview_image = None
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.slider_changes.clear()
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}

    def push_undo(self):
        self.undo_stack.append({
            'image': self._image.copy(),
            'sliders': self.current_slider_values.copy()  # Save current slider states
        })
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append({
                'image': self._image.copy(),
                'sliders': self.current_slider_values.copy()
            })
            state = self.undo_stack.pop()
            self._image = state['image']
            self._base_image = self._image.copy()
            self._preview_base = self._image.copy()
            self.current_slider_values = state.get('sliders', {'blur': 0, 'brightness': 0, 'contrast': 1.0})
            # Reset preview image
            self._preview_image = None

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append({
                'image': self._image.copy(),
                'sliders': self.current_slider_values.copy()
            })
            state = self.redo_stack.pop()
            self._image = state['image']
            self._base_image = self._image.copy()
            self._preview_base = self._image.copy()
            self.current_slider_values = state.get('sliders', {'blur': 0, 'brightness': 0, 'contrast': 1.0})
            # Reset preview image
            self._preview_image = None

    def reset_image(self):
        if self._original_image is not None:
            self._image = self._original_image.copy()
            self._base_image = self._original_image.copy()
            self._preview_base = self._original_image.copy()
            self._preview_image = None
            self.undo_stack.clear()
            self.redo_stack.clear()
            self.slider_changes.clear()
            self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}

    def get_image(self):
        if self._preview_image is not None:
            return self._preview_image
        return self._image

    def commit_base(self):
        if self._preview_image is not None:
            self.push_undo()
            self._image = self._preview_image.copy()
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        # Update slider changes with current values
        self.slider_changes = self.current_slider_values.copy()

    def update_slider_state(self, slider_name, value):
        """Track slider changes"""
        self.current_slider_values[slider_name] = value

    def get_slider_state(self):
        """Get current slider states"""
        return self.current_slider_values.copy()

    def reset_slider_preview(self):
        """Reset preview image to base image"""
        self._preview_image = None

    # ---- BUTTON EFFECTS ----
    def to_grayscale(self):
        self.push_undo()
        img = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self._image = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True

    def detect_edges(self):
        self.push_undo()
        gray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self._image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True

    def rotate(self, angle):
        self.push_undo()
        if angle == 90:
            self._image = cv2.rotate(self._image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self._image = cv2.rotate(self._image, cv2.ROTATE_180)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True

    def flip(self, mode):
        self.push_undo()
        if mode == "horizontal":
            self._image = cv2.flip(self._image, 1)
        elif mode == "vertical":
            self._image = cv2.flip(self._image, 0)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True

    # ---- SLIDER PREVIEW ----
    def preview_blur(self, k):
        if self._image is None:
            return
            
        k = int(k)
        self.update_slider_state('blur', k)
        
        # Start from preview base (which is the committed image state)
        img = self._preview_base.copy()
        
        # Apply all three effects in proper order
        # 1. Blur first (affects all pixels equally)
        if k > 0:
            if k % 2 == 0: 
                k += 1
            img = cv2.GaussianBlur(img, (k, k), 0)
        
        # 2. Brightness and contrast
        brightness_val = int(self.current_slider_values['brightness'] * 2.55)
        contrast_val = float(self.current_slider_values['contrast'])
        
        # Apply both brightness and contrast together
        if brightness_val != 0 or contrast_val != 1.0:
            img = cv2.convertScaleAbs(img, alpha=contrast_val, beta=brightness_val)
            
        self._preview_image = img
        return True

    def preview_brightness(self, v):
        if self._image is None:
            return
            
        v = int(v)
        self.update_slider_state('brightness', v)
        
        # Start from preview base
        img = self._preview_base.copy()
        
        # Apply all three effects in proper order
        # 1. Blur first
        blur_val = self.current_slider_values['blur']
        if blur_val > 0:
            k = blur_val if blur_val % 2 == 1 else blur_val + 1
            img = cv2.GaussianBlur(img, (k, k), 0)
        
        # 2. Brightness and contrast
        brightness_val = int(v * 2.55)
        contrast_val = float(self.current_slider_values['contrast'])
        
        # Apply both brightness and contrast together
        if brightness_val != 0 or contrast_val != 1.0:
            img = cv2.convertScaleAbs(img, alpha=contrast_val, beta=brightness_val)
            
        self._preview_image = img
        return True

    def preview_contrast(self, v):
        if self._image is None:
            return
            
        v = float(v)
        self.update_slider_state('contrast', v)
        
        # Start from preview base
        img = self._preview_base.copy()
        
        # Apply all three effects in proper order
        # 1. Blur first
        blur_val = self.current_slider_values['blur']
        if blur_val > 0:
            k = blur_val if blur_val % 2 == 1 else blur_val + 1
            img = cv2.GaussianBlur(img, (k, k), 0)
        
        # 2. Brightness and contrast
        brightness_val = int(self.current_slider_values['brightness'] * 2.55)
        contrast_val = v
        
        # Apply both brightness and contrast together
        if brightness_val != 0 or contrast_val != 1.0:
            img = cv2.convertScaleAbs(img, alpha=contrast_val, beta=brightness_val)
            
        self._preview_image = img
        return True

    # ---- PRESETS ----
    def preset_bw(self):
        return self.to_grayscale()

    def preset_soft_blur(self):
        self.push_undo()
        self._image = cv2.GaussianBlur(self._image, (9, 9), 0)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True

    def preset_high_contrast(self):
        self.push_undo()
        self._image = cv2.convertScaleAbs(self._image, alpha=1.8, beta=0)
        self._base_image = self._image.copy()
        self._preview_base = self._image.copy()
        self._preview_image = None
        self.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        return True


# ================== IMAGE VIEWER ==================
class ImageViewer:
    def __init__(self, parent, title):
        self.frame = tk.Frame(parent)
        tk.Label(self.frame, text=title, font=("Arial", 11, "bold")).pack()
        self.label = tk.Label(self.frame, bg="#222")
        self.label.pack(expand=True, fill=tk.BOTH)
        self.tk_img = None

    def show_image(self, image, zoom=1.0):
        if image is None: 
            return
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        w, h = pil.size
        pil = pil.resize((int(w * zoom), int(h * zoom)), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(pil)
        self.label.config(image=self.tk_img)


# ================== MAIN APP ==================
class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Editor – Tkinter + OpenCV")
        self.root.geometry("1300x780")

        self.zoom_level = 1.0
        self.dark_mode = False
        self.processor = ImageProcessor()
        self.is_sliding = False  # Track if slider is being dragged

        self.create_menu()
        self.create_toolbar()
        self.create_layout()
        self.create_status_bar()
        self.bind_shortcuts()
        self.apply_dark_mode()  # Initialize with default mode

    # ---- MENU ----
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save As", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_command(label="Reset Image", command=self.reset_image, accelerator="Ctrl+R")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode, accelerator="Ctrl+D")
        
        # Preset menu
        preset_menu = tk.Menu(menubar, tearoff=0)
        preset_menu.add_command(label="Black & White", command=self.apply_preset_bw)
        preset_menu.add_command(label="Soft Blur", command=self.apply_preset_soft_blur)
        preset_menu.add_command(label="High Contrast", command=self.apply_preset_high_contrast)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="View", menu=view_menu)
        menubar.add_cascade(label="Presets", menu=preset_menu)
        self.root.config(menu=menubar)

    # ---- TOOLBAR ----
    def create_toolbar(self):
        bar = tk.Frame(self.root)
        bar.pack(fill=tk.X)
        
        # Create a toolbar frame with buttons
        toolbar_buttons = [
            ("📂 Open", self.load_image),
            ("💾 Save", self.save_image),
            ("↶ Undo", self.undo),
            ("↷ Redo", self.redo),
            ("🔄 Reset", self.reset_image),
            ("⊕ Zoom In", self.zoom_in),
            ("⊖ Zoom Out", self.zoom_out),
            ("🌙 Dark Mode", self.toggle_dark_mode),
            ("⚫ B&W", self.apply_preset_bw),
            ("🔍 Soft Blur", self.apply_preset_soft_blur),
            ("🔆 High Contrast", self.apply_preset_high_contrast)
        ]
        
        for text, cmd in toolbar_buttons:
            tk.Button(bar, text=text, command=cmd).pack(side=tk.LEFT, padx=2, pady=2)

    # ---- LAYOUT ----
    def create_layout(self):
        self.main = tk.Frame(self.root)
        self.main.pack(fill=tk.BOTH, expand=True)

        ctrl = tk.Frame(self.main, width=240)
        ctrl.pack(side=tk.LEFT, fill=tk.Y)

        # Image manipulation buttons
        tk.Button(ctrl, text="Grayscale", command=self.grayscale).pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Edges", command=self.edges).pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Rotate 90°", command=lambda: self.rotate(90)).pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Rotate 180°", command=lambda: self.rotate(180)).pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Flip Horizontal", command=lambda: self.flip("horizontal")).pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Flip Vertical", command=lambda: self.flip("vertical")).pack(fill=tk.X, pady=2)
        
        # Preset buttons in the control panel
        tk.Label(ctrl, text="Presets", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=(10, 2))
        tk.Button(ctrl, text="Black & White", command=self.apply_preset_bw, bg="#e0e0e0").pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="Soft Blur", command=self.apply_preset_soft_blur, bg="#e0e0e0").pack(fill=tk.X, pady=2)
        tk.Button(ctrl, text="High Contrast", command=self.apply_preset_high_contrast, bg="#e0e0e0").pack(fill=tk.X, pady=2)
        
        tk.Button(ctrl, text="Reset Image", command=self.reset_image, bg="#ffcccc").pack(fill=tk.X, pady=5)

        # Sliders for effects
        self.blur = tk.Scale(ctrl, from_=0, to=21, label="Blur", orient=tk.HORIZONTAL,
                              command=self.preview_blur)
        self.blur.pack(fill=tk.X, pady=5)
        self.blur.bind("<ButtonPress-1>", self.on_slider_start)
        self.blur.bind("<ButtonRelease-1>", self.on_slider_end)

        self.brightness = tk.Scale(ctrl, from_=-100, to=100, label="Brightness",
                                    orient=tk.HORIZONTAL, command=self.preview_brightness)
        self.brightness.set(0)
        self.brightness.pack(fill=tk.X, pady=5)
        self.brightness.bind("<ButtonPress-1>", self.on_slider_start)
        self.brightness.bind("<ButtonRelease-1>", self.on_slider_end)

        self.contrast = tk.Scale(ctrl, from_=0.0, to=3.0, resolution=0.1, label="Contrast",
                                  orient=tk.HORIZONTAL, command=self.preview_contrast)
        self.contrast.set(1.0)
        self.contrast.pack(fill=tk.X, pady=5)
        self.contrast.bind("<ButtonPress-1>", self.on_slider_start)
        self.contrast.bind("<ButtonRelease-1>", self.on_slider_end)

        self.zoom_slider = tk.Scale(ctrl, from_=25, to=300, label="Zoom %",
                                     orient=tk.HORIZONTAL, command=self.set_zoom)
        self.zoom_slider.set(100)
        self.zoom_slider.pack(fill=tk.X, pady=5)

        self.paned = tk.PanedWindow(self.main, sashwidth=6)
        self.paned.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.viewer_original = ImageViewer(self.paned, "Original")
        self.viewer_edited = ImageViewer(self.paned, "Edited")

        self.paned.add(self.viewer_original.frame)
        self.paned.add(self.viewer_edited.frame)

    # ---- STATUS ----
    def create_status_bar(self):
        self.status = tk.StringVar(value="No image loaded. Use 'File > Open' or toolbar buttons")
        tk.Label(self.root, textvariable=self.status, bd=1,
                 relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    # ---- SHORTCUTS ----
    def bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-r>", lambda e: self.reset_image())
        self.root.bind("<Control-d>", lambda e: self.toggle_dark_mode())
        # Zoom shortcuts
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-equal>", lambda e: self.zoom_in())  # Some keyboards use = for +
        # Preset shortcuts
        self.root.bind("<Control-b>", lambda e: self.apply_preset_bw())
        self.root.bind("<Control-l>", lambda e: self.apply_preset_soft_blur())
        self.root.bind("<Control-h>", lambda e: self.apply_preset_high_contrast())

    # ---- VIEW ----
    def update_view(self):
        img = self.processor.get_image()
        if img is not None:
            self.viewer_original.show_image(self.processor._original_image, self.zoom_level)
            self.viewer_edited.show_image(img, self.zoom_level)
            h, w = img.shape[:2]
            blur_val = self.processor.current_slider_values['blur']
            bright_val = self.processor.current_slider_values['brightness']
            contrast_val = self.processor.current_slider_values['contrast']
            self.status.set(f"{self.processor.filename} | {w}x{h}px | Zoom {int(self.zoom_level*100)}% | Blur:{blur_val} Bright:{bright_val} Contrast:{contrast_val:.1f}")

    # ---- FILE ----
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp")])
        if path:
            self.processor.load_image(path)
            self.zoom_level = 1.0
            self.zoom_slider.set(100)
            self.reset_sliders()
            self.update_view()

    def save_image(self):
        if self.processor.get_image() is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")])
        if path:
            cv2.imwrite(path, self.processor.get_image())
            messagebox.showinfo("Saved", "Image saved successfully!")

    # ---- EDIT ----
    def undo(self):
        self.processor.undo()
        self.restore_slider_states()
        self.update_view()

    def redo(self):
        self.processor.redo()
        self.restore_slider_states()
        self.update_view()

    def reset_image(self):
        self.processor.reset_image()
        self.reset_sliders()
        self.update_view()

    def grayscale(self):
        if self.processor.to_grayscale():
            self.reset_sliders()  # Reset sliders after button operation
            self.update_view()

    def edges(self):
        if self.processor.detect_edges():
            self.reset_sliders()  # Reset sliders after button operation
            self.update_view()

    def rotate(self, angle):
        if self.processor.rotate(angle):
            self.update_view()

    def flip(self, mode):
        if self.processor.flip(mode):
            self.update_view()

    # ---- SLIDER HANDLING ----
    def on_slider_start(self, event):
        """Called when slider drag starts"""
        self.is_sliding = True
        # Store the current base image before starting to slide
        self.processor._preview_base = self.processor._image.copy()

    def on_slider_end(self, event):
        """Called when slider drag ends"""
        self.is_sliding = False
        # Commit the changes
        self.processor.commit_base()
        self.update_view()

    def preview_blur(self, v):
        if self.processor.get_image() is None: 
            return
        if self.processor.preview_blur(v):
            self.update_view()

    def preview_brightness(self, v):
        if self.processor.get_image() is None: 
            return
        if self.processor.preview_brightness(v):
            self.update_view()

    def preview_contrast(self, v):
        if self.processor.get_image() is None: 
            return
        if self.processor.preview_contrast(v):
            self.update_view()

    def reset_sliders(self):
        """Reset all sliders to default values"""
        self.blur.set(0)
        self.brightness.set(0)
        self.contrast.set(1.0)
        self.processor.current_slider_values = {'blur': 0, 'brightness': 0, 'contrast': 1.0}
        self.processor.reset_slider_preview()

    def restore_slider_states(self):
        """Restore slider states from processor's current_slider_values"""
        slider_states = self.processor.get_slider_state()
        
        # Temporarily unbind to avoid triggering preview
        self.blur.unbind("<ButtonPress-1>")
        self.blur.unbind("<ButtonRelease-1>")
        self.brightness.unbind("<ButtonPress-1>")
        self.brightness.unbind("<ButtonRelease-1>")
        self.contrast.unbind("<ButtonPress-1>")
        self.contrast.unbind("<ButtonRelease-1>")
        
        # Restore values
        self.blur.set(slider_states.get('blur', 0))
        self.brightness.set(slider_states.get('brightness', 0))
        self.contrast.set(slider_states.get('contrast', 1.0))
        
        # Update preview base
        self.processor._preview_base = self.processor._image.copy()
        
        # Rebind events
        self.blur.bind("<ButtonPress-1>", self.on_slider_start)
        self.blur.bind("<ButtonRelease-1>", self.on_slider_end)
        self.brightness.bind("<ButtonPress-1>", self.on_slider_start)
        self.brightness.bind("<ButtonRelease-1>", self.on_slider_end)
        self.contrast.bind("<ButtonPress-1>", self.on_slider_start)
        self.contrast.bind("<ButtonRelease-1>", self.on_slider_end)

    # ---- PRESETS ----
    def apply_preset_bw(self):
        if self.processor._image is None:
            messagebox.showinfo("No Image", "Please load an image first!")
            return
        if self.processor.preset_bw():
            self.reset_sliders()
            self.update_view()

    def apply_preset_soft_blur(self):
        if self.processor._image is None:
            messagebox.showinfo("No Image", "Please load an image first!")
            return
        if self.processor.preset_soft_blur():
            self.reset_sliders()
            self.update_view()

    def apply_preset_high_contrast(self):
        if self.processor._image is None:
            messagebox.showinfo("No Image", "Please load an image first!")
            return
        if self.processor.preset_high_contrast():
            self.reset_sliders()
            self.update_view()

    # ---- ZOOM ----
    def zoom_in(self):
        if self.zoom_level < 3.0:  # Limit maximum zoom
            self.zoom_level *= 1.1
            self.zoom_slider.set(int(self.zoom_level * 100))
            self.update_view()

    def zoom_out(self):
        if self.zoom_level > 0.25:  # Limit minimum zoom
            self.zoom_level /= 1.1
            self.zoom_slider.set(int(self.zoom_level * 100))
            self.update_view()

    def set_zoom(self, v):
        self.zoom_level = float(v) / 100
        self.update_view()

    # ---- DARK MODE ----
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_dark_mode()

    def apply_dark_mode(self):
        if self.dark_mode:
            # Dark theme colors
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            widget_bg = "#3c3c3c"
            widget_fg = "#ffffff"
        else:
            # Light theme colors
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            widget_bg = "#ffffff"
            widget_fg = "#000000"

        # Apply colors to root and all widgets
        self.root.configure(bg=bg_color)
        
        # Update all child widgets
        self.update_widget_colors(self.root, bg_color, fg_color, widget_bg, widget_fg)
        
        # Update specific widgets
        self.viewer_original.label.config(bg="#222" if self.dark_mode else "#ddd")
        self.viewer_edited.label.config(bg="#222" if self.dark_mode else "#ddd")
        
        # Update status bar
        self.status.set(f"{'Dark Mode' if self.dark_mode else 'Light Mode'} | Sliders now work together properly")

    def update_widget_colors(self, widget, bg_color, fg_color, widget_bg, widget_fg):
        """Recursively update widget colors"""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.PanedWindow)):
                widget.config(bg=bg_color)
            elif isinstance(widget, tk.Label):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=widget_bg, fg=widget_fg, 
                             activebackground=fg_color, activeforeground=bg_color)
            elif isinstance(widget, tk.Scale):
                widget.config(bg=bg_color, fg=fg_color, 
                             troughcolor=widget_bg, highlightbackground=bg_color)
            elif isinstance(widget, tk.Menu):
                widget.config(bg=widget_bg, fg=widget_fg)
        except:
            pass
        
        # Update child widgets
        for child in widget.winfo_children():
            self.update_widget_colors(child, bg_color, fg_color, widget_bg, widget_fg)


# ================== RUN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()