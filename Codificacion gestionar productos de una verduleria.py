pip install PyQt5
python.exe -m pip install --upgrade pip
pip install PyQt5
pip install mysql-connector-python

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
import mysql.connector
class VerduleriaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Verdulería App')
        self.lbl_nombre = QLabel('Nombre:')
        self.txt_nombre = QLineEdit()
        self.lbl_precio = QLabel('Precio:')
        self.txt_precio = QLineEdit()
        self.lbl_tiempo = QLabel('Tiempo de Preparación:')
        self.txt_tiempo = QLineEdit()
        self.lbl_categoria = QLabel('Categoría:')
        self.cmb_categoria = QComboBox()
        self.load_categorias ()
        self.btn_agregar = QPushButton('Agregar Producto')
        self.btn_editar = QPushButton('Editar Producto')
        self.btn_eliminar = QPushButton('Eliminar Producto')
        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_editar.clicked.connect(self.editar_producto)
        self.btn_eliminar.clicked.connect (self.eliminar_producto)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_nombre)
        vbox.addWidget(self.txt_nombre)
        vbox.addWidget(self.lbl_precio)
        vbox.addWidget(self.txt_precio)
        vbox.addWidget(self.lbl_tiempo)
        vbox.addWidget(self.txt_tiempo)
        vbox.addWidget(self.lbl_categoria)
        vbox.addWidget(self.cmb_categoria)
        vbox.addWidget(self.btn_agregar)
        vbox.addWidget(self.btn_editar)
        vbox.addWidget(self.btn_eliminar)

        self.setLayout(vbox)
        self.show()

    def load_categorias(self):
        # Conectar a la base de datos MySQL y cargar categorías en el ComboBox
        connection = mysql.connector.connect(
            host='tu_host',
            user='tu_usuario',
            password='tu_contraseña',
            database='tu_base_de_datos'
        )
        cursor = connection.cursor()
        cursor.execute('SELECT Nombre_categoria FROM Categorias')
        categorias = cursor.fetchall()
        connection.close()

        for categoria in categorias:
            self.cmb_categoria.addItem(categoria[0])

    def agregar_producto(self):
        nombre = self.txt_nombre.text()
        precio = int(self.txt_precio.text())
        tiempo = int(self.txt_tiempo.text())
        categoria = self.cmb_categoria.currentText()

        connection = mysql.connector.connect(
            host='tu_host',
            user='tu_usuario',
            password='tu_contraseña',
            database='tu_base_de_datos'
        )
        cursor = connection.cursor()

        # Obtener id de la categoría
        cursor.execute('SELECT id_categoria FROM Categorias WHERE Nombre_categoria = %s', (categoria,))
        id_categoria = cursor.fetchone()[0]

        # Insertar producto en la base de datos
        cursor.execute('INSERT INTO Productos (nombre, precio, tiempo_de_preparacion, id_categoria) VALUES (%s, %s, %s, %s)',
                       (nombre, precio, tiempo, id_categoria))

        connection.commit()
        connection.close()

        QMessageBox.information(self, 'Éxito', 'Producto agregado correctamente.')

    def editar_producto(self):
        # Implementa la lógica para editar productos en la base de datos
        pass

    def eliminar_producto(self):
        # Implementa la lógica para eliminar productos de la base de datos
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VerduleriaApp()
    sys.exit(app.exec_())






