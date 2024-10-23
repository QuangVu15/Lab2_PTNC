import tkinter as tk
from GUI_Login_ver2 import DatabaseModel, LoginController, LoginView

# Main: Run the application
if __name__ == "__main__":
    root = tk.Tk()

    # Create the model and controller
    model = DatabaseModel()
    view = LoginView(root, None)  
    controller = LoginController(model, view)

    # Pass the controller to the view
    view.controller = controller
    root.mainloop()
