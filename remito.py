import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QSpinBox, QCheckBox, QComboBox, 
    QSplitter, QListWidget, QVBoxLayout, QDialog, QPushButton, QListWidgetItem,
    QMessageBox, QLabel, QLineEdit  # Asegúrate de incluir QLineEdit aquí
)
from PyQt5.QtCore import Qt
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

        self.cargar_clientes()

    def cargar_clientes(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='xxx',
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
                password='xxx',
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
                nombre_cliente = "Cliente no cargado"
            else:
                id_cliente = self.cmb_clientes.currentData()
                nombre_cliente = self.cmb_clientes.currentText()

            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='xxx',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_insertar_remito = "INSERT INTO remitos (id_cliente) VALUES (%s)"
            cursor.execute(consulta_insertar_remito, (id_cliente,))
            conexion.commit()

            nuevo_id = cursor.lastrowid

            remito_nombre = f"Remito {nuevo_id}"
            remito_item = QListWidgetItem(remito_nombre)
            remito_item.setData(Qt.UserRole, nuevo_id)
            self.parent().lista_remitos.addItem(remito_item)
            self.accept()

            print("Remito guardado exitosamente.")

            detalles_remito = VentanaDetallesRemito(remito_id=nuevo_id, nombre_cliente=nombre_cliente, productos=self.productos_remito)
            detalles_remito.exec_()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en guardar_remito: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

class VentanaDetallesRemito(QDialog):
    def __init__(self, remito_id, nombre_cliente, productos):
        super().__init__()
        self.remito_id = remito_id
        self.nombre_cliente = nombre_cliente
        self.productos = productos
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Detalles del Remito {self.remito_id}")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        label_cliente = QLabel(f"Cliente: {self.nombre_cliente}")
        label_productos = QLabel("Productos:")

        for producto_id, cantidad in self.productos:
            nombre_producto = self.obtener_nombre_producto(producto_id)
            label_producto = QLabel(f"{nombre_producto} x {cantidad}")
            layout.addWidget(label_producto)

        btn_editar = QPushButton("Editar Remito")
        btn_eliminar = QPushButton("Eliminar Remito")

        btn_editar.clicked.connect(self.editar_remito)
        btn_eliminar.clicked.connect(self.eliminar_remito)

        layout.addWidget(label_cliente)
        layout.addWidget(label_productos)
        layout.addWidget(btn_editar)
        layout.addWidget(btn_eliminar)

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

    def editar_remito(self):
        editar_dialog = VentanaEditarRemito(remito_id=self.remito_id, nombre_cliente=self.nombre_cliente, productos=self.productos)
        editar_dialog.exec_()

    def eliminar_remito(self):
        confirmacion = QMessageBox.question(self, "Eliminar Remito", "¿Está seguro de que desea eliminar este remito?",
                                           QMessageBox.Yes | QMessageBox.No)

        if confirmacion == QMessageBox.Yes:
            print(f"Remito {self.remito_id} eliminado.")
            self.accept()

class VentanaEditarRemito(QDialog):
    def __init__(self, remito_id, nombre_cliente, productos):
        super().__init__()
        self.remito_id = remito_id
        self.nombre_cliente = nombre_cliente
        self.productos = productos
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Editar Remito {self.remito_id}")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        # Agrega controles para editar los detalles del remito
        # Puedes usar QLineEdit, QSpinBox, etc., según sea necesario
        self.edit_nombre_cliente = QLineEdit(self.nombre_cliente)
        self.edit_productos = QLineEdit(", ".join([f"{self.obtener_nombre_producto(producto_id)} x {cantidad}" for producto_id, cantidad in self.productos]))

        btn_guardar = QPushButton("Guardar Cambios")
        btn_cancelar = QPushButton("Cancelar")

        btn_guardar.clicked.connect(self.guardar_cambios)
        btn_cancelar.clicked.connect(self.close)

        layout.addWidget(QLabel("Nombre del Cliente:"))
        layout.addWidget(self.edit_nombre_cliente)
        layout.addWidget(QLabel("Productos:"))
        layout.addWidget(self.edit_productos)
        layout.addWidget(btn_guardar)
        layout.addWidget(btn_cancelar)

    def guardar_cambios(self):
        # Implementa la lógica para guardar los cambios en la base de datos
        nuevo_nombre_cliente = self.edit_nombre_cliente.text()
        nuevos_productos = self.edit_productos.text()

        # Puedes actualizar la base de datos con la nueva información
        # ...

        print(f"Cambios guardados para el Remito {self.remito_id}.")
        self.accept()

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

            consulta_remitos = "SELECT id_remito, columna_correcta FROM remitos ORDER BY fecha_creacion DESC"
            cursor.execute(consulta_remitos)
            remitos = cursor.fetchall()

            self.lista_remitos.clear()

            for id_remito, nombre in remitos:
                remito_item = QListWidgetItem(nombre)
                remito_item.setData(Qt.UserRole, id_remito)
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

    def mostrar_detalles_remito(self, item):
        remito_id = item.data(Qt.UserRole)
        detalles_remito = VentanaDetallesRemito(remito_id=remito_id, nombre_cliente="", productos=[])
        detalles_remito.exec_()

if __name__ == '__main__':
    app = QApplication([])
    remito_app = RemitoApp()
    remito_app.lista_remitos.itemClicked.connect(remito_app.mostrar_detalles_remito)
    remito_app.show()
    sys.exit(app.exec_())
