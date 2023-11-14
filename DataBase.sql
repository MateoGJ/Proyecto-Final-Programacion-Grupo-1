CREATE DATABASE Green_Market_Inventory_DB;
USE Green_Market_Inventory_DB;

CREATE TABLE Productos (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  precio INT NOT NULL,
  id_categoria INT
);

CREATE TABLE Categorias (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  Nombre_categoria VARCHAR(255)
);

CREATE TABLE Clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(255),
  Dirección VARCHAR(255),
  Numero_Contacto VARCHAR(255)
);

CREATE TABLE Remitos (
  id_remito INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT,
  Fecha_Entrega DATE
);

CREATE TABLE stock_entries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  producto_id INT,
  cantidad INT DEFAULT 0,
  fecha DATE DEFAULT NULL, -- Fecha de salida
  tipo_operacion VARCHAR(255) DEFAULT NULL,
  remito_id INT -- Hace referencia al remito al que pertenece la entrada
);

ALTER TABLE stock_entries
ADD CONSTRAINT fk_id_producto
FOREIGN KEY (producto_id)
REFERENCES Productos (id_producto);

ALTER TABLE Productos
ADD FOREIGN KEY (id_categoria) REFERENCES Categorias (id_categoria);

ALTER TABLE Remitos
ADD FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente);

ALTER TABLE stock_entries
ADD CONSTRAINT fk_remito_id
FOREIGN KEY (remito_id)
REFERENCES Remitos (id_remito);
