import sqlite3

#Crear la base de datos y las tablas
conn = sqlite3.connect('clinica_veterinaria.db')
cursor = conn.cursor()

#Crear las tablas
#DUEÑOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS Duenos(
    id_dueno INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_dueno TEXT NOT NULL,
    telefono_dueno INTEGER NOT NULL,
    email_dueno TEXT NOT NULL,
    dni_dueno TEXT NOT NULL,
    direccion_dueno TEXT NOT NULL
);
""")

#ANIMALES
cursor.execute("""
CREATE TABLE IF NOT EXISTS Animales(
    id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_animal TEXT NOT NULL,
    chip_animal INTEGER NOT NULL,
    especie_animal TEXT NOT NULL,
    nacimiento_animal TEXT NOT NULL,
    sexo_animal TEXT NOT NULL,
    id_dueno INTEGER NOT NULL,
    FOREIGN KEY(id_dueno) REFERENCES Duenos(id_dueno)
);
""")

#FACTURAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS Facturas(
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dueno INTEGER NOT NULL,
    FOREIGN KEY(id_dueno) REFERENCES Duenos(id_dueno),
    id_animal INTEGER NOT NULL,
    FOREIGN KEY(id_animal) REFERENCES Animales(id_animal),
    tratamiento TEXT NOT NULL,
    fecha_factura TEXT NOT NULL,
    precio_sin_iva REAL NOT NULL,
    precio_con_iva REAL NOT NULL,
);
""")

#TRATAMIENTOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tratamientos(
    id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tratamiento TEXT NOT NULL,
    precio_sin_iva REAL NOT NULL
);
""")

#CITAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS Citas(
    id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal INTEGER NOT NULL,
    FOREIGN KEY(id_animal) REFERENCES Animales(id_animal),
    id_dueno INTEGER NOT NULL,
    FOREIGN KEY(id_dueno) REFERENCES Duenos(id_dueno),
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    tratamiento TEXT NOT NULL
);
""")

conn.commit()
conn.close()  # Close the connection to the database