INSERT INTO Categorias (Nombre_categoria) VALUES
  ('Frutas'),
  ('Verduras'),
  ('Legumbres'),
  ('Cereales'),
  ('Hortalizas'),
  ('Frutos secos');

-- Carga de datos en la tabla Clientes
INSERT INTO Clientes (Nombre, Dirección, Numero_Contacto) VALUES
  ('Juan Pérez', 'Calle 123, Ciudad A', '555-1234'),
  ('María González', 'Avenida X, Ciudad B', '555-5678'),
  ('Luis Rodríguez', 'Calle Z, Ciudad C', '555-9876'),
  ('Ana López', 'Ruta 456, Ciudad D', '555-5432'),
  ('Carlos Sánchez', 'Avenida Y, Ciudad E', '555-6789');

-- Carga de datos en la tabla Remitos
INSERT INTO Remitos (id_cliente, Fecha_Entrega) VALUES
  (1, '2023-10-15'),
  (2, '2023-10-16'),
  (3, '2023-10-17'),
  (4, '2023-10-18'),
  (5, '2023-10-19');

-- Carga de datos en la tabla Productos
INSERT INTO Productos (nombre, precio, id_categoria) VALUES
  ('Manzanas', 2.5, 1),
  ('Zanahorias', 1.0, 2),
  ('Peras', 2.0, 1),
  ('Tomates', 1.5, 2),
  ('Arroz', 3.0, 3);

-- Estos registros hacen referencia a los productos entregados en los remitos anteriores
INSERT INTO stock_entries (producto_id, cantidad, fecha, tipo_operacion, remito_id) VALUES
  (1, 300, '2023-10-15', 'entrada', 1),
  (2, 350, '2023-10-15', 'entrada', 1),
  (3, 275, '2023-10-16', 'entrada', 2),
  (4, 160, '2023-10-17', 'entrada', 3),
  (5, 180, '2023-10-18', 'entrada', 4),
  (1, 100, '2023-10-15', 'salida', 1),
  (2, 50, '2023-10-15', 'salida', 1),
  (3, 75, '2023-10-16', 'salida', 2),
  (4, 60, '2023-10-17', 'salida', 3),
  (5, 80, '2023-10-18', 'salida', 4);
