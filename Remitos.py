import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QWidget,
    QHeaderView,
    QSplitter,
    QVBoxLayout,
    QPushButton,
    QFormLayout,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QListWidget,
    QDialog,
    QTableWidgetItem,
    QTableWidget,
)
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime

class VentanaNuevoRemito(QDialog):
    def __init__(self, parent, lista_remitos, lista_productos):
        super().__init__(parent)
        self.lista_remitos = lista_remitos
        self.productos_remito = lista_productos
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Nuevo Remito')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout(self)

        # Controles para cliente
        form_cliente = QFormLayout()
        self.cmb_clientes = QComboBox()
        form_cliente.addRow('Cliente:', self.cmb_clientes)

        # Agregar los clientes a la lista desplegable
        self.cargar_clientes()

        self.chk_cliente_no_cargado = QCheckBox("Cliente no cargado")
        form_cliente.addRow('', self.chk_cliente_no_cargado)

        # Conectar evento de cambio de cliente no cargado
        self.chk_cliente_no_cargado.clicked.connect(self.seleccionar_cliente_anonimo)

        # Conectar evento de cambio de cliente para cargar productos
        self.cmb_clientes.currentIndexChanged.connect(self.cargar_productos)

        # Controles para productos
        form_productos = QFormLayout()
        self.cmb_productos = QComboBox()
        self.spn_cantidad = QSpinBox()
        self.spn_cantidad.setRange(0, 99999)  # Sin límite superior
        self.btn_agregar_producto = QPushButton('Agregar Producto', self)
        self.btn_agregar_producto.clicked.connect(self.agregar_producto)
        self.lista_productos = QListWidget()

        form_productos.addRow('Producto:', self.cmb_productos)
        form_productos.addRow('Cantidad:', self.spn_cantidad)
        form_productos.addRow(self.btn_agregar_producto)
        form_productos.addRow('Productos:', self.lista_productos)

        # Botón para agregar nuevo remito
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
                password='maximiliano1o1o',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            # Obtener clientes
            consulta_clientes = "SELECT id_cliente, Nombre FROM clientes WHERE id_cliente <> 999"
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

    def seleccionar_cliente_anonimo(self):
        if self.chk_cliente_no_cargado.isChecked():
            # Deshabilitar la selección del cliente
            self.cmb_clientes.setEnabled(False)
            
            # Marcar como cliente anónimo
            index_anonimo = self.cmb_clientes.findData(999)
            if index_anonimo != -1:
                self.cmb_clientes.setCurrentIndex(index_anonimo)

    def cargar_productos(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
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

    def agregar_producto(self):
        producto_id = self.cmb_productos.currentData()
        cantidad = self.spn_cantidad.value()

        if producto_id and cantidad > 0:
            nombre_producto = self.obtener_nombre_producto(producto_id)

            self.productos_remito.append((producto_id, cantidad))
            item_text = f"{cantidad} x {nombre_producto}"
            self.lista_productos.addItem(item_text)

    def obtener_nombre_producto(self, producto_id):
    # Obtener el nombre del producto usando el ID
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            # Obtener el nombre del producto
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

    def guardar_remito(self):
        try:
            id_cliente = None 

            # Si no está marcada la casilla de cliente anónimo, obtener el ID del cliente seleccionado
            if not self.chk_cliente_no_cargado.isChecked():
                id_cliente = self.cmb_clientes.currentData()
            else:
                # Si está marcada la casilla de cliente anónimo, usar el ID del cliente anónimo
                id_cliente = 999  # ID del cliente anónimo "999"

            # Insertar el remito en la tabla Remitos
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_remito_query = "INSERT INTO Remitos (id_cliente, Fecha_Entrega) VALUES (%s, %s)"
            remito_data = (id_cliente, fecha_actual)

            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()
            cursor.execute(insert_remito_query, remito_data)
            conexion.commit()  

            # Obtener el ID del remito recién insertado
            remito_id = cursor.lastrowid

            if self.chk_cliente_no_cargado.isChecked():
                # Cliente no cargado, usar cliente ficticio
                id_cliente = 999  # ID de cliente ficticio
                cliente_nombre = "Anónimo"
            else:
                # Cliente seleccionado de la lista desplegable
                id_cliente = self.cmb_clientes.currentData()
                cliente_nombre = self.cmb_clientes.currentText()  # Obtener el nombre del cliente

            # Insertar los productos en la tabla stock_entries
            for producto_id, cantidad in self.productos_remito:
                insert_stock_query = "INSERT INTO stock_entries (producto_id, cantidad, fecha, tipo_operacion, remito_id) VALUES (%s, %s, %s, %s, %s)"
                stock_data = (producto_id, cantidad, fecha_actual, 'Salida', remito_id)
                cursor.execute(insert_stock_query, stock_data)
                conexion.commit()  

            # Actualizar la tabla de remitos en la interfaz
            row_count = self.lista_remitos.rowCount()
            self.lista_remitos.insertRow(row_count)
            self.lista_remitos.setItem(row_count, 0, QTableWidgetItem(str(remito_id)))  # ID del remito
            self.lista_remitos.setItem(row_count, 1, QTableWidgetItem(self.cmb_clientes.currentText()))  # Nombre del cliente
            productos_str = ", ".join([f"{cantidad} x {self.obtener_nombre_producto(producto_id)}" for (producto_id, cantidad) in self.productos_remito])
            self.lista_remitos.setItem(row_count, 2, QTableWidgetItem(productos_str))  # Productos
            self.lista_remitos.setItem(row_count, 3, QTableWidgetItem(fecha_actual))  # Fecha del remito

            conexion.close()

            self.accept()  # Cerrar la ventana de nuevo remito

        except mysql.connector.Error as err:
            print(f"Error de MySQL en guardar_remito: {err}")


class RemitoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.productos_remito = []  # Lista de productos del remito
        self.init_ui()
        self.cargar_remitos()  # Llamada a la función para cargar remitos al iniciar la ventana

    def init_ui(self):
        self.setWindowTitle('Sistema de Remitos')
        self.setGeometry(100, 100, 800, 600)

        self.btn_agregar_remito = QPushButton('Agregar Nuevo Remito', self)
        self.btn_agregar_remito.clicked.connect(self.mostrar_ventana_nuevo_remito)

        self.btn_eliminar_remito = QPushButton('Eliminar Remito', self)
        self.btn_eliminar_remito.clicked.connect(self.ejecutar_eliminar_remito) 

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)  

        # Crear la tabla para mostrar los remitos
        self.lista_remitos = QTableWidget(self)
        self.lista_remitos.setColumnCount(4)  # ID, Cliente, Productos, Fecha
        self.lista_remitos.setHorizontalHeaderLabels(["ID", "Cliente", "Productos", "Fecha"])
        self.lista_remitos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Expande las columnas
        self.lista_remitos.setEditTriggers(QTableWidget.NoEditTriggers)  # Deshabilita la edición
        self.lista_remitos.setSelectionBehavior(QTableWidget.SelectRows)  # Selecciona la fila completa

        layout = QVBoxLayout(self)
        layout.addWidget(self.btn_agregar_remito)
        layout.addWidget(self.btn_eliminar_remito)
        layout.addWidget(self.lista_remitos)

    def ejecutar_eliminar_remito(self):
        try:
            self.eliminar_remito()
            print("Remito eliminado exitosamente.")

        except mysql.connector.Error as err:
            print(f"Error de MySQL al eliminar el remito: {err}")

    def eliminar_remito(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            # Obtener el ID del remito seleccionado en la tabla
            row = self.lista_remitos.currentRow()
            remito_id = int(self.lista_remitos.item(row, 0).text())

            opcion = QMessageBox.question(
                self, 'Eliminar Remito', '¿Estás seguro que deseas eliminar este remito?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if opcion == QMessageBox.Yes:
                # Eliminar las entradas relacionadas en stock_entries
                delete_stock_query = "DELETE FROM stock_entries WHERE remito_id = %s"
                cursor.execute(delete_stock_query, (remito_id,))
                conexion.commit()

                # Eliminar el remito de la tabla Remitos
                delete_remito_query = "DELETE FROM Remitos WHERE id_remito = %s"
                cursor.execute(delete_remito_query, (remito_id,))
                conexion.commit()

                conexion.close()

                # Actualizar la lista de remitos en la interfaz después de eliminar
                self.cargar_remitos()
                print("Remito eliminado exitosamente.")

        except mysql.connector.Error as err:
            print(f"Error de MySQL al eliminar el remito: {err}")
    
    
    def cargar_remitos(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='green_market_inventory_db'
            )

            cursor = conexion.cursor()

            consulta_remitos = "SELECT id_remito, id_cliente, Fecha_Entrega FROM Remitos"
            cursor.execute(consulta_remitos)
            remitos = cursor.fetchall()

            self.lista_remitos.setRowCount(len(remitos))

            for index, remito in enumerate(remitos):
                remito_id, id_cliente, fecha = remito

                # Obtener el nombre del cliente o establecer como "Anónimo" si el ID es ficticio
                if id_cliente == 999:
                    nombre_cliente = "Anónimo"
                else:
                    consulta_cliente = "SELECT Nombre FROM Clientes WHERE id_cliente = %s"
                    cursor.execute(consulta_cliente, (id_cliente,))
                    nombre_cliente = cursor.fetchone()[0]

                # Obtener los productos asociados a este remito
                consulta_productos = "SELECT cantidad, nombre FROM stock_entries JOIN Productos ON stock_entries.producto_id = Productos.id_producto WHERE remito_id = %s"
                cursor.execute(consulta_productos, (remito_id,))
                productos = cursor.fetchall()

                productos_text = ", ".join([f"{cantidad} x {nombre}" for cantidad, nombre in productos])

                self.lista_remitos.setItem(index, 0, QTableWidgetItem(str(remito_id)))
                self.lista_remitos.setItem(index, 1, QTableWidgetItem(nombre_cliente))  # Nombre del cliente
                self.lista_remitos.setItem(index, 2, QTableWidgetItem(productos_text))  # Productos
                self.lista_remitos.setItem(index, 3, QTableWidgetItem(str(fecha)))  # Fecha del remito

            conexion.close()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en cargar_remitos: {err}")

    def mostrar_ventana_nuevo_remito(self):
        ventana_nuevo_remito = VentanaNuevoRemito(
            parent=self, lista_remitos=self.lista_remitos, lista_productos=self.productos_remito
        )
        ventana_nuevo_remito.exec_()

if __name__ == '__main__':
    app = QApplication([])
    remito_app = RemitoApp()
    remito_app.show()
    sys.exit(app.exec_())
