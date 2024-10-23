import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql


# View: User Interface
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

        # Login and Insert Data Buttons
        tk.Button(root, text="Login", command=self.login).grid(row=4, column=1)

        # Add fields for Ho Tên, Địa chỉ, and Massv
        tk.Label(root, text="Họ Tên:").grid(row=5, column=0)
        self.entry_ho_ten = tk.Entry(root)
        self.entry_ho_ten.grid(row=5, column=1)

        tk.Label(root, text="Địa chỉ:").grid(row=6, column=0)
        self.entry_dia_chi = tk.Entry(root)
        self.entry_dia_chi.grid(row=6, column=1)

        tk.Label(root, text="Mã số sinh viên:").grid(row=7, column=0)  # New label for massv
        self.entry_massv = tk.Entry(root)  # New entry for massv
        self.entry_massv.grid(row=7, column=1)

        tk.Button(root, text="Thêm", command=self.insert_data).grid(row=8, column=1)

        # Data Display Section
        self.data_display = tk.Text(root, height=10, width=50)
        self.data_display.grid(row=10, column=0, columnspan=2)

        tk.Button(root, text="Load Data", command=lambda: self.load_data()).grid(row=9, column=1)

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
        massv = self.entry_massv.get()  # Get value from massv entry
        table = "SinhVien"  # Using a fixed table name for simplicity
        self.controller.insert_data(table, column1, column2, massv)

    def load_data(self):
        table_name = "SinhVien"  # Using a fixed table name for simplicity
        self.controller.load_data(table_name)


# Controller: Handles the logic between View and Model
class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def login(self, user, password, host, db_name):
        self.model.user.set(user)
        self.model.password.set(password)
        self.model.host.set(host)
        self.model.db_name.set(db_name)
        self.model.connect_db()

    def insert_data(self, table, column1, column2, massv):
        self.model.insert_data(table, column1, column2, massv)

    def load_data(self, table_name):
        self.model.load_data(table_name)


# Model: Data handling and database connection
class DatabaseModel:
    def __init__(self):
        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.cur = None  # Initialize cur to None
        self.conn = None  # Initialize conn to None

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Kết nối database thành công!")
        except Exception as e:
            messagebox.showerror("Error", f"Kết nối database thất bại: {e}")

    def insert_data(self, table, column1, column2, massv):
        try:
            query = f"INSERT INTO \"{table}\" (hoten, diachi, massv) VALUES (%s, %s, %s)"  # Include massv in the query
            self.cur.execute(query, (column1, column2, massv))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được chèn thành công!")
        except Exception as e:
            self.conn.rollback()  # Hoàn tác giao dịch
            messagebox.showerror("Lỗi", f"Lỗi khi chèn dữ liệu: {e}")

    def load_data(self, table_name):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Clear old content before displaying new data
            self.data_display.delete(1.0, tk.END)

            # Display new data
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")  
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def set_display_widget(self, display_widget):
        """Assign Text widget for displaying data"""
        self.data_display = display_widget


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

