from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import sys
import mysql.connector  

class StockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Actual de Productos")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Alerta"])

        self.load_stock_data()   

        layout.addWidget(self.table)

        alert_button = QPushButton("Notificar Bajo Inventario")
        alert_button.clicked.connect(self.alert_low_stock)
        layout.addWidget(alert_button)

        self.setLayout(layout)

    def load_stock_data(self):
  
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='violeta',
            password='usain1087',
            database='Green_Market_Inventory_DB'
        )
        cursor = conn.cursor()

      
        cursor.execute("SELECT id_producto, nombre, cantidad FROM Productos")

        stock_data = cursor.fetchall()


        self.table.setRowCount(len(stock_data))

        for row_num, row_data in enumerate(stock_data):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_num, col_num, item)

                
                if col_num == 2 and int(data) < 30:
                    alert_item = QTableWidgetItem("¡Bajo Inventario!")
                    alert_item.setForeground ('Qtred')  

        conn.close()

    def alert_low_stock(self):
        
        low_stock_count = 0

        for row in range(self.table.rowCount()):
            quantity_item = self.table.item(row, 2)
            if quantity_item and int(quantity_item.text()) < 50:
                low_stock_count += 1

        if low_stock_count > 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Hay {low_stock_count} productos con bajo inventario.")
            msg.setWindowTitle("Alerta de Bajo Inventario")
            msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)