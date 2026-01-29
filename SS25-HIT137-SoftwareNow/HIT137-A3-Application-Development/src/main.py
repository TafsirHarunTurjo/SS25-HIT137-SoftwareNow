"""HIT137 Assignment 3 - Application Development.

Entry point for the Image Editor application.
"""

import tkinter as tk
from src.app.gui import ImageEditorGUI


def main() -> None:
    root = tk.Tk()
    ImageEditorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
