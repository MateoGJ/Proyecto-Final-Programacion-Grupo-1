import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHeaderView, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QMessageBox, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import pyqtSignal
import mysql.connector

# Constantes de conexión a la base de datos
DB_CONFIG = {
    'host': "localhost",
    'port': 3306,
    'user': "root",
    'password': 'maximiliano1o1o',
    'database': 'Green_Market_Inventory_DB'
}

class VentanaListadoProductos(QDialog):
    def __init__(self, productos):
        super().__init__()
        self.productos = productos
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Listado de Productos')
        self.setGeometry(200, 200, 600, 400)

        # Crear una tabla para mostrar el listado de productos
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)  # id, Nombre, Precio, Categoría
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Precio', 'Categoría'])

        self.cargar_datos()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)  # Agrega esta línea para incluir la tabla en el diseño

    def cargar_datos(self):
        # Cargar datos en la tabla
        self.table_widget.setRowCount(len(self.productos))

        for row, producto in enumerate(self.productos):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
            self.table_widget.setItem(row, 1, QTableWidgetItem(producto['nombre']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(producto['precio'])))
            self.table_widget.setItem(row, 3, QTableWidgetItem(producto['categoria']))

class VentanaEditarProducto(QDialog):
    producto_editado = pyqtSignal(dict)

    def __init__(self, producto, parent=None):
        super().__init__(parent)
        self.producto = producto
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Editar Producto')
        self.setGeometry(300, 300, 400, 200)

        # Widgets del formulario
        self.txt_nombre = QLineEdit(self)
        self.txt_precio = QLineEdit(self)
        self.cmb_categoria = QComboBox(self)  # <-- Cambié el nombre aquí
        self.load_categorias()

        # Botón para editar producto
        btn_editar = QPushButton('Editar', self)
        btn_editar.clicked.connect(self.editar_producto)

        # Configurar widgets con datos del producto seleccionado
        self.txt_nombre.setText(self.producto['nombre'])
        self.txt_precio.setText(str(self.producto['precio']))
        self.cmb_categoria.setCurrentText(self.producto['categoria'])  # <-- Cambié el nombre aquí

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Nombre:'))
        layout.addWidget(self.txt_nombre)
        layout.addWidget(QLabel('Precio:'))
        layout.addWidget(self.txt_precio)
        layout.addWidget(QLabel('Categoría:'))
        layout.addWidget(self.cmb_categoria)
        layout.addWidget(btn_editar)

        self.setLayout(layout)

    def load_categorias(self):
        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Consulta para obtener categorías
            consulta_categorias = "SELECT Nombre_categoria FROM Categorias"
            cursor.execute(consulta_categorias)
            categorias = cursor.fetchall()

            # Limpiar el combo box antes de agregar nuevos elementos
            self.cmb_categoria.clear()  # <-- Cambié el nombre aquí

            # Agregar la opción "Todas las Categorías" al inicio de la lista
            self.cmb_categoria.addItem('Todas las Categorías')  # <-- Cambié el nombre aquí

            # Agregar categorías al combo box
            for categoria in categorias:
                self.cmb_categoria.addItem(categoria[0])  # <-- Cambié el nombre aquí

            # Configurar el ComboBox para mostrar la opción "Todas las Categorías" inicialmente
            self.cmb_categoria.setCurrentIndex(0)

            print("Categorías cargadas exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en load_categorias: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def editar_producto(self):
        # Obtener datos del formulario
        nombre = self.txt_nombre.text()
        precio_texto = self.txt_precio.text()
        categoria = self.cmb_categoria.currentText()

        # Verificar que los campos de precio no estén vacíos
        if not precio_texto:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un valor para Precio.')
            return

        try:
            # Convertir a entero después de verificar que no está vacío
            precio = int(precio_texto)
        except ValueError:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un valor numérico válido para Precio.')
            return

        # Obtener id del producto
        id_producto = self.producto['id']

        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Obtener id de la categoría
            cursor.execute('SELECT id_categoria FROM categorias WHERE Nombre_categoria = %s', (categoria,))
            id_categoria = cursor.fetchone()[0]

            # Actualizar producto en la base de datos
            cursor.execute('UPDATE productos SET nombre = %s, precio = %s, id_categoria = %s WHERE id_producto = %s',
                           (nombre, precio, id_categoria, id_producto))

            conexion.commit()
            conexion.close()

            # Emitir señal con los datos actualizados
            self.producto_editado.emit({
                'id': id_producto,
                'nombre': nombre,
                'precio': precio,
                'categoria': categoria
            })

            QMessageBox.information(self, 'Éxito', 'Producto editado correctamente.')
            # Cerrar el cuadro de diálogo después de editar el producto
            self.accept()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en editar_producto: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

class VerduleriaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.productos = []  # Lista para almacenar productos (id, nombre, precio, id_categoria)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Verdulería App')

        # Crear una tabla para mostrar el listado de productos
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)  # id, Nombre, Precio, Categoría
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Precio', 'Categoría'])
        self.table_widget.setRowCount(0)  # Iniciar con la tabla vacía

        # Ajustar tamaño de la tabla
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Cargar datos en la tabla
        self.cargar_datos()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)

        # Botones para agregar, editar, eliminar productos
        self.btn_agregar = QPushButton('Agregar Producto', self)
        self.btn_eliminar = QPushButton('Eliminar Producto', self)

        # Conectar señales a funciones
        self.btn_agregar.clicked.connect(self.mostrar_formulario_agregar)
        self.btn_eliminar.clicked.connect(self.eliminar_producto)

        # ComboBox para filtrar productos por categoría
        self.cmb_categorias = QComboBox(self)
        self.load_categorias()  # Llama a la función load_categorias para cargar las categorías
        self.cmb_categorias.addItem('Todas las Categorías')  # Opción para mostrar todos los productos
        self.cmb_categorias.currentIndexChanged.connect(self.filtrar_por_categoria)

        # Botón para editar producto
        self.btn_editar = QPushButton('Editar Producto', self)
        self.btn_editar.clicked.connect(self.mostrar_ventana_editar)

        layout.addWidget(self.cmb_categorias)
        layout.addWidget(self.btn_agregar)
        layout.addWidget(self.btn_editar)
        layout.addWidget(self.btn_eliminar)

        self.setLayout(layout)
        self.show()

    def mostrar_ventana_editar(self):
        # Verificar si hay un producto seleccionado en la tabla
        if not self.table_widget.selectedIndexes():
            QMessageBox.warning(self, 'Advertencia', 'Por favor, seleccione un producto para editar.')
            return

        # Obtener datos del producto seleccionado
        index = self.table_widget.selectedIndexes()[0].row()
        producto_seleccionado = self.productos[index]

        # Crear una instancia de la ventana para editar productos
        self.ventana_editar = VentanaEditarProducto(producto_seleccionado, self)
        self.ventana_editar.producto_editado.connect(self.actualizar_producto)
        self.ventana_editar.exec_()  # Ejecutar la ventana como un cuadro de diálogo

    def actualizar_producto(self, producto_actualizado):
        # Actualizar el producto en la lista de productos
        for i, producto in enumerate(self.productos):
            if producto['id'] == producto_actualizado['id']:
                self.productos[i] = producto_actualizado

        # Recargar la tabla después de cerrar el cuadro de diálogo
        self.cargar_datos()

    def mostrar_formulario_agregar(self):
        # Crear una instancia de la ventana para agregar productos
        ventana_agregar = VentanaAgregarProducto(self)
        ventana_agregar.exec_()  # Ejecutar la ventana como un cuadro de diálogo

        # Recargar la tabla después de cerrar el cuadro de diálogo
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with mysql.connector.connect(**DB_CONFIG) as conexion:
                with conexion.cursor() as cursor:
                    # Consulta para obtener todos los productos con sus categorías
                    consulta_productos = "SELECT Productos.id_producto, Productos.nombre, Productos.precio, Categorias.Nombre_categoria " \
                                         "FROM Productos JOIN Categorias ON Productos.id_categoria = Categorias.id_categoria"
                    cursor.execute(consulta_productos)
                    productos = cursor.fetchall()

                    # Limpiar la tabla antes de agregar nuevos elementos
                    self.table_widget.setRowCount(0)

                    # Agregar productos a la tabla
                    for row, producto in enumerate(productos):
                        self.table_widget.insertRow(row)
                        self.table_widget.setItem(row, 0, QTableWidgetItem(str(producto[0])))  # Mostrar solo el ID del producto
                        self.table_widget.setItem(row, 1, QTableWidgetItem(producto[1]))  # Mostrar solo el nombre
                        self.table_widget.setItem(row, 2, QTableWidgetItem(str(producto[2])))
                        self.table_widget.setItem(row, 3, QTableWidgetItem(producto[3]))

                        # Agregar producto a la lista de productos
                        self.productos.append({
                            'id': producto[0],
                            'nombre': producto[1],
                            'precio': producto[2],
                            'categoria': producto[3]
                        })

            print("Datos cargados exitosamente.")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Error', f"Error de MySQL en cargar_datos: {err}")

    def agregar_producto(self):
        # Obtener datos del formulario
        nombre = self.txt_nombre.text()
        precio_texto = self.txt_precio.text()
        tiempo_texto = self.txt_tiempo.text()
        categoria = self.cmb_categoria.currentText()

        # Verificar que los campos de precio y tiempo no estén vacíos
        if not precio_texto or not tiempo_texto:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese un valor para Precio y Tiempo.')
            return

        try:
            # Convertir a entero después de verificar que no está vacío
            precio = int(precio_texto)
            tiempo = int(tiempo_texto)
        except ValueError:
            QMessageBox.warning(self, 'Advertencia', 'Por favor, ingrese valores numéricos válidos para Precio y Tiempo.')
            return

        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Obtener id de la categoría
            cursor.execute('SELECT id_categoria FROM categorias WHERE Nombre_categoria = %s', (categoria,))
            id_categoria = cursor.fetchone()[0]

            # Insertar producto en la base de datos
            cursor.execute('INSERT INTO productos (nombre, precio, tiempo_de_preparacion, id_categoria) VALUES (%s, %s, %s, %s)',
                        (nombre, precio, tiempo, id_categoria))

            conexion.commit()
            conexion.close()

            # Limpiar el formulario después de agregar el producto
            self.txt_nombre.clear()
            self.txt_precio.clear()
            self.txt_tiempo.clear()
            self.cmb_categoria.setCurrentIndex(0)

            QMessageBox.information(self, 'Éxito', 'Producto agregado correctamente.')
            # Recargar la tabla para reflejar el nuevo producto
            self.cargar_datos()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en agregar_producto: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()


    def editar_producto(self):
        # Obtener datos del formulario
        id_producto = int(self.table_widget.item(self.table_widget.currentRow(), 0).text())
        nombre = self.txt_nombre.text()
        precio = int(self.txt_precio.text())
        tiempo = int(self.txt_tiempo.text())
        categoria = self.cmb_categoria.currentText()

        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Obtener id de la categoría
            cursor.execute('SELECT id_categoria FROM categorias WHERE Nombre_categoria = %s', (categoria,))
            id_categoria = cursor.fetchone()[0]

            # Actualizar producto en la base de datos
            cursor.execute('UPDATE productos SET nombre = %s, precio = %s, tiempo_de_preparacion = %s, id_categoria = %s WHERE id_producto = %s',
                        (nombre, precio, tiempo, id_categoria, id_producto))

            conexion.commit()
            conexion.close()

            # Limpiar el formulario después de editar el producto
            self.txt_nombre.clear()
            self.txt_precio.clear()
            self.txt_tiempo.clear()
            self.cmb_categoria.setCurrentIndex(0)

            QMessageBox.information(self, 'Éxito', 'Producto editado correctamente.')
            # Recargar la tabla para reflejar los cambios
            self.cargar_datos()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en editar_producto: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def eliminar_producto(self):
        # Obtener el id del producto seleccionado en la tabla
        id_producto = int(self.table_widget.item(self.table_widget.currentRow(), 0).text())

        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Eliminar producto de la base de datos
            cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))

            conexion.commit()
            conexion.close()

            QMessageBox.information(self, 'Éxito', 'Producto eliminado correctamente.')
            # Recargar la tabla para reflejar los cambios
            self.cargar_datos()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en eliminar_producto: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def load_categorias(self):
        try:
            # Conexión a la base de datos (ajusta las credenciales según tu configuración)
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Consulta para obtener categorías
            consulta_categorias = "SELECT Nombre_categoria FROM Categorias"
            cursor.execute(consulta_categorias)
            categorias = cursor.fetchall()

            # Limpiar el combo box antes de agregar nuevos elementos
            self.cmb_categorias.clear()

            # Agregar la opción "Todas las Categorías" al inicio de la lista
            self.cmb_categorias.addItem('Todas las Categorías')

            # Agregar categorías al combo box
            for categoria in categorias:
                self.cmb_categorias.addItem(categoria[0])

            # Configurar el ComboBox para mostrar la opción "Todas las Categorías" inicialmente
            self.cmb_categorias.setCurrentIndex(0)

            print("Categorías cargadas exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en load_categorias: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def filtrar_por_categoria(self):
        try:
            # Conexión a la base de datos 
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Obtener la categoría seleccionada
            categoria_seleccionada = self.cmb_categorias.currentText()

            if categoria_seleccionada == 'Todas las Categorías':
                # Consulta para obtener todos los productos
                consulta_productos = "SELECT Productos.id_producto, Productos.nombre, Productos.precio, Categorias.Nombre_categoria " \
                                    "FROM Productos JOIN Categorias ON Productos.id_categoria = Categorias.id_categoria"
                cursor.execute(consulta_productos)
            else:
                # Consulta para obtener productos por categoría
                consulta_productos = "SELECT Productos.id_producto, Productos.nombre, Productos.precio, Categorias.Nombre_categoria " \
                                    "FROM Productos JOIN Categorias ON Productos.id_categoria = Categorias.id_categoria " \
                                    "WHERE Categorias.Nombre_categoria = %s"
                cursor.execute(consulta_productos, (categoria_seleccionada,))

            productos = cursor.fetchall()

            # Limpiar la tabla antes de agregar nuevos elementos
            self.table_widget.setRowCount(0)

            # Limpiar la lista de productos
            self.productos.clear()

            # Agregar productos a la tabla y a la lista
            for row, producto in enumerate(productos):
                self.table_widget.insertRow(row)
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(producto[0])))  # Mostrar solo el ID del producto
                self.table_widget.setItem(row, 1, QTableWidgetItem(producto[1]))  # Mostrar solo el nombre
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(producto[2])))
                self.table_widget.setItem(row, 3, QTableWidgetItem(producto[3]))

                # Agregar producto a la lista de productos
                self.productos.append({
                    'id': producto[0],
                    'nombre': producto[1],
                    'precio': producto[2],
                    'categoria': producto[3]
                })

            print("Productos filtrados por categoría.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en filtrar_por_categoria: {err}")
        finally:
            # Cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

class VentanaAgregarProducto(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Agregar Producto')
        self.setGeometry(300, 300, 400, 200)

        # Widgets del formulario
        self.txt_nombre = QLineEdit(self)
        self.txt_precio = QLineEdit(self)
        self.cmb_categoria = QComboBox(self)
        self.load_categorias()

        # Botón para agregar producto
        btn_agregar = QPushButton('Agregar', self)
        btn_agregar.clicked.connect(self.agregar_producto)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Nombre:'))
        layout.addWidget(self.txt_nombre)
        layout.addWidget(QLabel('Precio:'))
        layout.addWidget(self.txt_precio)
        layout.addWidget(QLabel('Categoría:'))
        layout.addWidget(self.cmb_categoria)
        layout.addWidget(btn_agregar)

        self.setLayout(layout)

    def load_categorias(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Consulta para obtener categorías
            consulta_categorias = "SELECT Nombre_categoria FROM Categorias"
            cursor.execute(consulta_categorias)
            categorias = cursor.fetchall()

            # Agregar categorías al combo box
            for categoria in categorias:
                self.cmb_categoria.addItem(categoria[0])

            print("Categorías cargadas exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error de MySQL en load_categorias: {err}")
        finally:
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_producto(self):
        # Obtener datos del formulario
        nombre = self.txt_nombre.text()
        precio = self.txt_precio.text()
        categoria = self.cmb_categoria.currentText()

        # Validar que se haya seleccionado una categoría
        if not categoria:
            QMessageBox.warning(self, 'Error', 'Por favor, seleccione una categoría.')
            return

        # Implementar la lógica para agregar productos
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password='maximiliano1o1o',
                database='Green_Market_Inventory_DB'
            )

            cursor = conexion.cursor()

            # Obtener id de la categoría
            cursor.execute('SELECT id_categoria FROM categorias WHERE Nombre_categoria = %s', (categoria,))
            id_categoria = cursor.fetchone()[0]

            # Insertar producto en la base de datos
            cursor.execute('INSERT INTO productos (nombre, precio, id_categoria) VALUES (%s, %s, %s)',
                           (nombre, precio, id_categoria))

            conexion.commit()
            conexion.close()

            # Cerrar el cuadro de diálogo después de agregar el producto
            self.accept()

        except mysql.connector.Error as err:
            print(f"Error de MySQL en agregar_producto: {err}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals() and conexion.is_connected():
                cursor.close()
                conexion.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VerduleriaApp()
    sys.exit(app.exec_())
