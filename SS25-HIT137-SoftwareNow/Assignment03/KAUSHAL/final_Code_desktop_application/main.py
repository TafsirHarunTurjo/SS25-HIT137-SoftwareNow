"""
Main Entry Point for Photoshop Mini Application
Demonstrates application startup and main loop.
"""

import tkinter as tk
from image_controller import ImageController


def main():
    """
    Main function to start the application.
    Demonstrates application initialization.
    """
    try:
        print("Starting Photoshop Mini Application...")
        
        # Create main window
        root = tk.Tk()
        
        # Create application controller
        app = ImageController(root)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'+{x}+{y}')
        
        # Start main loop
        print("Application started successfully!")
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()