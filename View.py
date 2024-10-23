import tkinter as tk
from tkinter import messagebox

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Login to PostgreSQL")

        # Auto-fill credentials
        default_credentials = {
            "username": "postgres",
            "password": "123456",
            "host": "localhost",
            "database": "dbtest"
        }

        # User Interface Elements
        tk.Label(root, text="Username:").grid(row=0, column=0)
        self.entry_user = tk.Entry(root)
        self.entry_user.insert(0, default_credentials["username"])  # Auto-fill
        self.entry_user.grid(row=0, column=1)

        tk.Label(root, text="Password:").grid(row=1, column=0)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.insert(0, default_credentials["password"])  # Auto-fill
        self.entry_pass.grid(row=1, column=1)

        tk.Label(root, text="Host:").grid(row=2, column=0)
        self.entry_host = tk.Entry(root)
        self.entry_host.insert(0, default_credentials["host"])  # Auto-fill
        self.entry_host.grid(row=2, column=1)

        tk.Label(root, text="Database:").grid(row=3, column=0)
        self.entry_db = tk.Entry(root)
        self.entry_db.insert(0, default_credentials["database"])  # Auto-fill
        self.entry_db.grid(row=3, column=1)

        # Login Button
        tk.Button(root, text="Login", command=self.login).grid(row=4, column=1)

        # Add fields for Ho Tên, Địa chỉ, and Mã số sinh viên
        tk.Label(root, text="Họ Tên:").grid(row=5, column=0)
        self.entry_ho_ten = tk.Entry(root)
        self.entry_ho_ten.grid(row=5, column=1)

        tk.Label(root, text="Địa chỉ:").grid(row=6, column=0)
        self.entry_dia_chi = tk.Entry(root)
        self.entry_dia_chi.grid(row=6, column=1)

        tk.Label(root, text="Mã số sinh viên:").grid(row=7, column=0)
        self.entry_massv = tk.Entry(root)
        self.entry_massv.grid(row=7, column=1)

        # Add and Load Data Buttons
        tk.Button(root, text="Thêm", command=self.insert_data).grid(row=8, column=1)
        tk.Button(root, text="Load Data", command=self.load_data).grid(row=9, column=1)

        # Data Display Section
        self.data_display = tk.Text(root, height=10, width=50)
        self.data_display.grid(row=10, column=0, columnspan=2)

    def login(self):
        user = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        host = self.entry_host.get().strip()
        db_name = self.entry_db.get().strip()

        if not all([user, password, host, db_name]):
            messagebox.showwarning("Warning", "Vui lòng điền đầy đủ thông tin!")
            return
        
        self.controller.login(user, password, host, db_name)

    def insert_data(self):
        column1 = self.entry_ho_ten.get()
        column2 = self.entry_dia_chi.get()
        massv = self.entry_massv.get()
        table = "SinhVien"
        self.controller.insert_data(table, column1, column2, massv)

    def load_data(self):
        table_name = "SinhVien"
        self.controller.load_data(table_name)
