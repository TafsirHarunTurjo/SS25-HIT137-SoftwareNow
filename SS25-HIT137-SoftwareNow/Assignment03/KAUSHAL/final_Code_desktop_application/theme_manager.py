"""
Theme Manager Module

Handles theme management and UI styling for the Photoshop application.
Demonstrates OOP concepts: Encapsulation, Singleton pattern.
"""

import tkinter as tk
from typing import Dict, List


class ThemeManager:
    """
    Manages application themes with predefined and custom options.
    Demonstrates Singleton-like pattern.
    """
    
    # Class variable for shared instance
    _instance = None
    
    # Predefined themes - demonstrates class variables
    THEMES = {
        "Dark": {
            "bg": "#1f1f1f",
            "fg": "#ffffff",
            "panel_bg": "#2a2a2a",
            "button_bg": "#333333",
            "button_fg": "#ffffff",
            "accent": "#4aa3ff",
            "canvas_bg": "#101010",
            "hover": "#3a3a3a",
            "slider_bg": "#2a2a2a",
            "entry_bg": "#333333",
            "entry_fg": "#ffffff",
        },
        "Light": {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "panel_bg": "#f7f7f7",
            "button_bg": "#ffffff",
            "button_fg": "#000000",
            "accent": "#2a6fff",
            "canvas_bg": "#dddddd",
            "hover": "#e0e0e0",
            "slider_bg": "#f7f7f7",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
        },
        "Ocean": {
            "bg": "#0b1f2a",
            "fg": "#eaf6ff",
            "panel_bg": "#102c3b",
            "button_bg": "#163748",
            "button_fg": "#eaf6ff",
            "accent": "#3cc7ff",
            "canvas_bg": "#07151c",
            "hover": "#1a3a4d",
            "slider_bg": "#102c3b",
            "entry_bg": "#163748",
            "entry_fg": "#eaf6ff",
        },
        "Nord": {
            "bg": "#2e3440",
            "fg": "#eceff4",
            "panel_bg": "#3b4252",
            "button_bg": "#434c5e",
            "button_fg": "#eceff4",
            "accent": "#88c0d0",
            "canvas_bg": "#1f232b",
            "hover": "#4c566a",
            "slider_bg": "#3b4252",
            "entry_bg": "#434c5e",
            "entry_fg": "#eceff4",
        },
    }
    
    def __new__(cls):
        """Create singleton instance - demonstrates __new__ method"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager - demonstrates constructor"""
        if not hasattr(self, 'initialized'):
            self.current_theme = "Dark"
            self.theme = self.THEMES["Dark"].copy()
            self.initialized = True
    
    @staticmethod
    def _is_dark(hex_color: str) -> bool:
        """
        Determine if a color is dark based on luminance.
        
        Args:
            hex_color: Color in hex format (#RRGGBB)
            
        Returns:
            bool: True if color is dark
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return False
        
        # Parse RGB components
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Calculate luminance
        luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return luminance < 128
    
    def create_custom_theme(self, bg_color: str, accent_color: str) -> Dict[str, str]:
        """
        Create a custom theme based on background and accent colors.
        
        Args:
            bg_color: Background color in hex
            accent_color: Accent color in hex
            
        Returns:
            dict: Complete theme dictionary
        """
        is_dark = self._is_dark(bg_color)
        
        # Create complementary colors
        panel_bg = self._adjust_color(bg_color, -20 if is_dark else 20)
        button_bg = accent_color
        button_fg = "#000000" if not self._is_dark(accent_color) else "#ffffff"
        canvas_bg = self._adjust_color(bg_color, -30 if is_dark else 30)
        
        return {
            "bg": bg_color,
            "fg": "#ffffff" if is_dark else "#000000",
            "panel_bg": panel_bg,
            "button_bg": button_bg,
            "button_fg": button_fg,
            "accent": accent_color,
            "canvas_bg": canvas_bg,
            "hover": self._adjust_color(accent_color, 30),
            "slider_bg": panel_bg,
            "entry_bg": button_bg,
            "entry_fg": button_fg,
        }
    
    @staticmethod
    def _adjust_color(hex_color: str, amount: int) -> str:
        """
        Adjust color brightness by a given amount.
        
        Args:
            hex_color: Color in hex format
            amount: Amount to adjust (-255 to 255)
            
 Returns:
            str: Adjusted color in hex format
        """
        hex_color = hex_color.lstrip("#")
        
        # Parse RGB components
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Adjust brightness
        r = max(0, min(255, r + amount))
        g = max(0, min(255, g + amount))
        b = max(0, min(255, b + amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def set_theme(self, theme_name: str):
        """
        Set the current theme by name.
        
        Args:
            theme_name: Name of the theme to set
        """
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.theme = self.THEMES[theme_name].copy()
            print(f"Theme set to: {theme_name}")
        else:
            # Handle custom themes
            self.current_theme = "Custom"
            print(f"Custom theme set")
    
    def get_theme_names(self) -> List[str]:
        """
        Get list of available theme names.
        
        Returns:
            list: List of theme names
        """
        return list(self.THEMES.keys())
    
    def apply_to_widget(self, widget: tk.Widget, theme: Dict[str, str] = None):
        """
        Apply theme colors to a specific widget.
        
        Args:
            widget: Tkinter widget to style
            theme: Theme dictionary (uses current theme if None)
        """
        if theme is None:
            theme = self.theme
        
        widget_type = widget.winfo_class()
        
        try:
            # Apply theme based on widget type
            if widget_type in ("TFrame", "Frame", "Labelframe", "LabelFrame", "Panedwindow", "TPanedwindow"):
                widget.config(bg=theme.get("bg", "#1f1f1f"))
            elif widget_type == "Label":
                widget.config(
                    bg=theme.get("bg", "#1f1f1f"),
                    fg=theme.get("fg", "#ffffff")
                )
            elif widget_type == "Button":
                widget.config(
                    bg=theme.get("button_bg", "#333333"),
                    fg=theme.get("button_fg", "#ffffff"),
                    activebackground=theme.get("hover", "#3a3a3a"),
                    activeforeground=theme.get("button_fg", "#ffffff"),
                    relief=tk.RAISED,
                    bd=2,
                    padx=10,
                    pady=5
                )
            elif widget_type == "Scale":
                widget.config(
                    bg=theme.get("bg", "#1f1f1f"),
                    fg=theme.get("fg", "#ffffff"),
                    troughcolor=theme.get("slider_bg", "#2a2a2a"),
                    highlightbackground=theme.get("bg", "#1f1f1f"),
                    activebackground=theme.get("accent", "#4aa3ff")
                )
            elif widget_type == "Entry":
                widget.config(
                    bg=theme.get("entry_bg", "#333333"),
                    fg=theme.get("entry_fg", "#ffffff"),
                    insertbackground=theme.get("entry_fg", "#ffffff"),
                    relief=tk.SUNKEN,
                    bd=2
                )
            elif widget_type == "Canvas":
                widget.config(
                    bg=theme.get("canvas_bg", "#101010"),
                    highlightthickness=0
                )
            elif widget_type == "Checkbutton":
                widget.config(
                    bg=theme.get("bg", "#1f1f1f"),
                    fg=theme.get("fg", "#ffffff"),
                    selectcolor=theme.get("accent", "#4aa3ff"),
                    activebackground=theme.get("bg", "#1f1f1f"),
                    activeforeground=theme.get("fg", "#ffffff")
                )
            elif widget_type == "Radiobutton":
                widget.config(
                    bg=theme.get("bg", "#1f1f1f"),
                    fg=theme.get("fg", "#ffffff"),
                    selectcolor=theme.get("accent", "#4aa3ff"),
                    activebackground=theme.get("bg", "#1f1f1f"),
                    activeforeground=theme.get("fg", "#ffffff")
                )
            elif widget_type == "Scrollbar":
                widget.config(
                    bg=theme.get("panel_bg", "#2a2a2a"),
                    troughcolor=theme.get("bg", "#1f1f1f"),
                    activebackground=theme.get("accent", "#4aa3ff")
                )
        except Exception as e:
            # Silently handle widgets that don't support certain configurations
            pass