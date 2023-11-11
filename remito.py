import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QSpinBox, QCheckBox, QComboBox, QSplitter, QListWidget, QVBoxLayout, QDialog, QPushButton, QListWidgetItem
import mysql.connector

class VentanaNuevoRemito(QDialog):
    def __init__(self, parent, lista_productos):
        super().__init__(parent)
        self.productos_remito = lista_productos
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Nuevo Remito')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        form_cliente = QFormLayout()
        self.cmb_clientes = QComboBox()
        self.chk_cliente_no_cargado = QCheckBox("Cliente no cargado")
        form_cliente.addRow('Cliente:', self.cmb_clientes)
        form_cliente.addRow('', self.chk_cliente_no_cargado)

        self.cmb_clientes.currentIndexChanged.connect(self.cargar_productos)

        form_productos = QFormLayout()
        self.cmb_productos = QComboBox()
        self.spn_cantidad = QSpinBox()
        self.spn_cantidad.setRange(0, 99999)
        self.btn_agregar_producto = QPushButton('Agregar Producto', self)
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        self.lista_productos = QListWidget()

        form_productos.addRow('Producto:', self.cmb_productos)
        form_productos.addRow('Cantidad:', self.spn_cantidad)
        form_productos.addRow(self.btn_agregar_producto)
        form_productos.addRow('Productos:', self.lista_productos)

        btn_guardar_remito = QPushButton('Guardar Remito', self)
        btn_guardar_remito.clicked.connect(self.guardar_remito)

        layout.addLayout(form_cliente)
        layout.addLayout(form_productos)
        layout.addWidget(btn_guardar_remito)

        self.productos_remito = []

        self.cargar_clientes()

    def cargar_clientes(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='Pacha#2324',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_clientes = "SELECT id_cliente, Nombre FROM clientes"
            cursor.execute(consulta_clientes)
            clientes = cursor.fetchall()

            self.cmb_clientes.clear()

            for id_cliente, nombre in clientes:
                self.cmb_clientes.addItem(nombre, id_cliente)

            print("Clientes cargados exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en cargar_clientes: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_producto(self):
        producto_id = self.cmb_productos.currentData()
        cantidad = self.spn_cantidad.value()

        if producto_id and cantidad > 0:
            nombre_producto = self.obtener_nombre_producto(producto_id)

            self.productos_remito.append((producto_id, cantidad))
            item_text = f"{cantidad} x {nombre_producto}"
            self.lista_productos.addItem(item_text)

    def obtener_nombre_producto(self, producto_id):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='Pacha#2324',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_nombre_producto = "SELECT nombre FROM productos WHERE id_producto = %s"
            cursor.execute(consulta_nombre_producto, (producto_id,))
            resultado = cursor.fetchone()

            if resultado:
                nombre_producto = resultado[0]
                return nombre_producto
            else:
                return "Nombre no encontrado"
        except mysql.connector.Error as err:
            print(f"Error de MySQL en obtener_nombre_producto: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_productos(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='Pacha#2324',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_productos = "SELECT id_producto, nombre FROM productos"
            cursor.execute(consulta_productos)
            productos = cursor.fetchall()

            self.cmb_productos.clear()

            for id_producto, nombre in productos:
                self.cmb_productos.addItem(nombre, id_producto)

            print("Productos cargados exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en cargar_productos: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def guardar_remito(self):
        try:
            if self.chk_cliente_no_cargado.isChecked():
                id_cliente = 999
            else:
                id_cliente = self.cmb_clientes.currentData()

            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='Pacha#2324',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_insertar_remito = "INSERT INTO remitos (id_cliente) VALUES (%s)"
            cursor.execute(consulta_insertar_remito, (id_cliente,))
            conexion.commit()

            nuevo_id = cursor.lastrowid

            remito_nombre = f"Remito {nuevo_id}"
            remito_item = QListWidgetItem(remito_nombre)
            self.parent().lista_remitos.addItem(remito_item)
            self.accept()

            print("Remito guardado exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en guardar_remito: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

class RemitoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.productos_remito = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sistema de Remitos')
        self.setGeometry(100, 100, 800, 600)

        self.btn_agregar_remito = QPushButton('Agregar Nuevo Remito', self)
        self.btn_agregar_remito.clicked.connect(self.mostrar_ventana_nuevo_remito)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(0x1)

        self.lista_remitos = QListWidget(self)
        self.splitter.addWidget(self.lista_remitos)

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn_agregar_remito)
        layout.addWidget(self.splitter)

        self.cargar_remitos()

    def cargar_remitos(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='Pacha#2324',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_remitos = "SELECT id_remito, nombre FROM remitos ORDER BY fecha_creacion DESC"
            cursor.execute(consulta_remitos)
            remitos = cursor.fetchall()

            self.lista_remitos.clear()

            for id_remito, nombre in remitos:
                remito_item = QListWidgetItem(nombre)
                self.lista_remitos.addItem(remito_item)

            print("Remitos cargados exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en cargar_remitos: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def mostrar_ventana_nuevo_remito(self):
        ventana_nuevo_remito = VentanaNuevoRemito(parent=self, lista_productos=self.productos_remito)
        ventana_nuevo_remito.exec_()

if __name__ == '__main__':
    app = QApplication([])
    remito_app = RemitoApp()
    remito_app.show()
    sys.exit(app.exec_())

# Añade el siguiente método a la clase RemitoApp
class RemitoApp(QWidget):
    # ... (otros métodos)

    def mostrar_detalles_remito(self, item):
        remito_id = self.lista_remitos.row(item) + 1  # Obtén el ID del remito seleccionado

        # A continuación, puedes cargar los detalles del remito desde la base de datos
        # y mostrarlos en una nueva ventana o de la manera que prefieras.

        # Ejemplo: Mostrar un cuadro de mensaje con los detalles del remito
        QMessageBox.information(self, "Detalles del Remito", f"Detalles del Remito {remito_id}")

# Modifica la parte donde conectas el evento para llamar al nuevo método
if __name__ == '__main__':
    app = QApplication([])
    remito_app = RemitoApp()

    # Conecta el evento itemClicked a la función mostrar_detalles_remito
    remito_app.lista_remitos.itemClicked.connect(remito_app.mostrar_detalles_remito)

    remito_app.show()
    sys.exit(app.exec_())
