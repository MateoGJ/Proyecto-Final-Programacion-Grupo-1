from PyQt5.QtWidgets import QApplication, QSizePolicy, QHeaderView, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog, QGridLayout, QLabel, QComboBox
import sys
import mysql.connector  
from PyQt5.QtGui import QColor

class StockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Actual de Productos")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Stock Total"])

        self.load_stock_data()

        # Permitir que la tabla se expanda horizontalmente y verticalmente
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        entries_button = QPushButton("Mostrar Entradas y Salidas")
        entries_button.clicked.connect(self.show_entries)
        layout.addWidget(entries_button)

        self.setLayout(layout)

        # Ajustar el tamaño inicial de la ventana
        self.resize(600, 400)

    def load_stock_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password='maximiliano1o1o',
            database='Green_Market_Inventory_DB'
        )
        cursor = conn.cursor()

        # Realizar una consulta para obtener el stock total
        cursor.execute("SELECT P.id_producto, P.nombre, "
                       "SUM(IF(SE.tipo_operacion = 'salida', SE.cantidad * -1, SE.cantidad)) AS stock "
                       "FROM Productos P LEFT JOIN stock_entries SE ON P.id_producto = SE.producto_id "
                       "GROUP BY P.id_producto, P.nombre")

        stock_data = cursor.fetchall()

        self.table.setRowCount(len(stock_data))
        self.table.setColumnCount(3)  

        column_headers = ["ID", "Nombre", "Stock"]
        self.table.setHorizontalHeaderLabels(column_headers)

        for row_num, row_data in enumerate(stock_data):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_num, col_num, item)

                # Cambiar el fondo de las filas con bajo inventario a rojo
                if col_num == 2 and data is not None and int(data) < 30:
                    for i in range(3):  
                        self.table.item(row_num, i).setBackground(QColor(255, 0, 0))

        conn.close()

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        # Ajustar el tamaño de la ventana para adaptarse al contenido
        self.resize(self.table.horizontalHeader().length() + 70, self.table.verticalHeader().length() + 40)

        # Ajustar el tamaño de la ventana
        self.resize(800, 600)  

        # Mostrar la ventana
        self.show()

    def show_entries(self):
        entries_dialog = EntriesDialog(self)
        entries_dialog.exec_()

class EntriesDialog(QDialog):
    def __init__(self, parent=None):
        super(EntriesDialog, self).__init__(parent)
        self.setWindowTitle("Entradas y Salidas")

        layout = QVBoxLayout()  

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Producto", "Cantidad", "Fecha", "Tipo de Operación", "Remito ID"])

        # Permitir que la tabla se expanda en el ancho disponible
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_entries_data()

        layout.addWidget(self.table)

        filter_label = QLabel("Filtrar por Producto:")
        layout.addWidget(filter_label)

        self.filter_combobox = QComboBox()
        self.load_product_names()
        layout.addWidget(self.filter_combobox)

        filter_button = QPushButton("Filtrar")
        filter_button.clicked.connect(self.filter_entries)
        layout.addWidget(filter_button)

        self.setLayout(layout)

        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

        # Configurar una política de tamaño para que la ventana se expanda
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)

    def load_entries_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password='maximiliano1o1o',
            database='Green_Market_Inventory_DB'
        )
        cursor = conn.cursor()

        # Realizar una consulta para obtener las entradas y salidas
        cursor.execute("SELECT P.nombre, SE.cantidad, SE.fecha, SE.tipo_operacion, SE.remito_id "
                    "FROM stock_entries SE JOIN Productos P ON SE.producto_id = P.id_producto")

        entries_data = cursor.fetchall()

        self.table.setRowCount(len(entries_data))

        for row_num, row_data in enumerate(entries_data):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_num, col_num, item)

        conn.close()

    def load_product_names(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password='maximiliano1o1o',
            database='Green_Market_Inventory_DB'
        )
        cursor = conn.cursor()

        # Obtener los nombres de los productos
        cursor.execute("SELECT nombre FROM Productos")

        product_names = cursor.fetchall()

        for name in product_names:
            self.filter_combobox.addItem(name[0])

        conn.close()

    def filter_entries(self):
        selected_product = self.filter_combobox.currentText()

        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password='maximiliano1o1o',
            database='Green_Market_Inventory_DB'
        )
        cursor = conn.cursor()

        # Filtrar las entradas y salidas por el producto seleccionado
        cursor.execute("SELECT P.nombre, SE.cantidad, SE.fecha, SE.tipo_operacion, SE.remito_id "
                    "FROM stock_entries SE JOIN Productos P ON SE.producto_id = P.id_producto "
                    "WHERE P.nombre = %s", (selected_product,))

        filtered_data = cursor.fetchall()

        self.table.setRowCount(len(filtered_data))

        for row_num, row_data in enumerate(filtered_data):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_num, col_num, item)

        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stock_window = StockWindow()
    stock_window.show()
    sys.exit(app.exec_())
