import tkinter as tk
from Model import DatabaseModel
from View import LoginView
from Controller import LoginController

if __name__ == "__main__":
    root = tk.Tk()

    # Initialize Model, View, and Controller
    model = DatabaseModel()
    view = LoginView(root, None)
    controller = LoginController(model, view)

    # Connect controller to view
    view.controller = controller

    # Start the application
    root.mainloop()
