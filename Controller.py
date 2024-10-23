class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Assign Text widget from view to model
        self.model.set_display_widget(self.view.data_display)

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
