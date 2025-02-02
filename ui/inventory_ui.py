import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal

SERVER_URL = "http://127.0.0.1:5000"

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Table to display inventory
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Quantity"])
        layout.addWidget(self.table)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh Inventory")
        self.refresh_button.clicked.connect(self.refresh_inventory)
        layout.addWidget(self.refresh_button)

        # Add Item Section
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        layout.addWidget(self.name_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        layout.addWidget(self.quantity_input)

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_button)

        # Remove Item Section
        self.remove_name_input = QLineEdit()
        self.remove_name_input.setPlaceholderText("Item Name to Remove")
        layout.addWidget(self.remove_name_input)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.clicked.connect(self.remove_item)
        layout.addWidget(self.remove_button)

        # Update Quantity Section
        self.update_name_input = QLineEdit()
        self.update_name_input.setPlaceholderText("Item Name to Update")
        layout.addWidget(self.update_name_input)

        self.update_quantity_input = QLineEdit()
        self.update_quantity_input.setPlaceholderText("New Quantity")
        layout.addWidget(self.update_quantity_input)

        self.update_button = QPushButton("Update Quantity")
        self.update_button.clicked.connect(self.update_quantity)
        layout.addWidget(self.update_button)

        self.setLayout(layout)
        self.refresh_inventory()

    def refresh_inventory(self):
        self.worker = Worker(self.fetch_inventory)
        self.worker.result_signal.connect(self.update_table)
        self.worker.start()

    def fetch_inventory(self):
        try:
            response = requests.get(f"{SERVER_URL}/inventory")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching inventory: {e}")
        return []

    def update_table(self, data):
        self.table.setRowCount(0)
        for item in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["quantity"])))

    def add_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()
        if name and quantity:
            self.worker = Worker(self.send_add_item, name, int(quantity))
            self.worker.start()

    def send_add_item(self, name, quantity):
        try:
            response = requests.post(f"{SERVER_URL}/add-item", json={"name": name, "quantity": quantity})
            if response.status_code == 200:
                self.refresh_inventory()
        except Exception as e:
            print(f"Error adding item: {e}")

    def remove_item(self):
        name = self.remove_name_input.text()
        if name:
            self.worker = Worker(self.send_remove_item, name)
            self.worker.start()

    def send_remove_item(self, name):
        try:
            response = requests.post(f"{SERVER_URL}/remove-item", json={"name": name})
            if response.status_code == 200:
                self.refresh_inventory()
        except Exception as e:
            print(f"Error removing item: {e}")

    def update_quantity(self):
        name = self.update_name_input.text()
        quantity = self.update_quantity_input.text()
        if name and quantity:
            self.worker = Worker(self.send_update_quantity, name, int(quantity))
            self.worker.start()

    def send_update_quantity(self, name, quantity):
        try:
            response = requests.post(f"{SERVER_URL}/update-quantity", json={"name": name, "quantity": quantity})
            if response.status_code == 200:
                self.refresh_inventory()
        except Exception as e:
            print(f"Error updating quantity: {e}")

class Worker(QThread):
    result_signal = pyqtSignal(list)

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        result = self.func(*self.args)
        self.result_signal.emit(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())