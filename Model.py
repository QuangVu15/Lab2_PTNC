import tkinter as tk
import psycopg2
from tkinter import messagebox
from psycopg2 import sql

class DatabaseModel:
    def __init__(self):
        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.cur = None
        self.conn = None
        self.data_display = None  # Widget to display data

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
            query = f"INSERT INTO \"{table}\" (hoten, diachi, massv) VALUES (%s, %s, %s)"
            self.cur.execute(query, (column1, column2, massv))
            self.conn.commit()
            messagebox.showinfo("Thành công", "Dữ liệu đã được chèn thành công!")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi chèn dữ liệu: {e}")

    def load_data(self, table_name):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            self.cur.execute(query)
            rows = self.cur.fetchall()

            # Clear old content before displaying new data
            if self.data_display:
                self.data_display.delete(1.0, tk.END)
            else:
                messagebox.showerror("Error", "Display widget not set.")
                return

            # Display new data
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def set_display_widget(self, display_widget):
        """Assign Text widget for displaying data"""
        self.data_display = display_widget
