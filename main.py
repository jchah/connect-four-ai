"""
main.py
Entry‑point script: starts the Connect‑Four GUI.

If you later add other front‑ends (CLI, AI vs. AI, network play, etc.),
you can expand this file into a simple menu that chooses which one to run.
"""

import tkinter as tk

# Importing the GUI module automatically pulls in the logic engine,
# because connect_four_gui.py does "from connect_four_logic import ConnectFour".
from connect_four_gui import ConnectFourGUI


def main() -> None:
    root = tk.Tk()
    ConnectFourGUI(root)  # build the window + widgets
    root.mainloop()       # hand control to Tkinter’s event loop


if __name__ == "__main__":
    main()
