from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from Stock import StockWindow
from Productos import VerduleriaApp
from Remitos import RemitoApp

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de...")
        layout = QVBoxLayout()

        # Crear instancias de las ventanas
        self.stock_window = StockWindow()
        self.productos_window = VerduleriaApp()
        self.remitos_window = RemitoApp()

        # Crear QStackedWidget y agregar las ventanas
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.stock_window)
        self.stacked_widget.addWidget(self.productos_window)
        self.stacked_widget.addWidget(self.remitos_window)

        # Botones para cambiar entre ventanas
        btn_stock = QPushButton("Stock")
        btn_stock.clicked.connect(self.show_stock)

        btn_productos = QPushButton("Productos")
        btn_productos.clicked.connect(self.show_productos)

        btn_remitos = QPushButton("Remitos")
        btn_remitos.clicked.connect(self.show_remitos)

        # Agregar botones al diseño
        layout.addWidget(btn_stock)
        layout.addWidget(btn_productos)
        layout.addWidget(btn_remitos)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

    def show_stock(self):
        self.stacked_widget.setCurrentWidget(self.stock_window)

    def show_productos(self):
        self.stacked_widget.setCurrentWidget(self.productos_window)

    def show_remitos(self):
        self.stacked_widget.setCurrentWidget(self.remitos_window)

if __name__ == '__main__':
    app = QApplication([])
    main_page = MainPage()
    main_page.show()
    app.exec_()
