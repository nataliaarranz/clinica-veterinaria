import sqlite3
import csv

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
#Cargar datos de dueños
with open("registroDuenos.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO Duenos(id_dueno, nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno)
            VALUES(?,?,?,?,?,?)
            """, (row[0], row[1], row[2], row[3], row[4], row[5]))

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
#Cargar datos de animales
with open("registroAnimales.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO Animales(id_animal, nombre_animal, chip_animal, especie_animal, nacimiento_animal, sexo_animal, id_dueno)
            VALUES(?,?,?,?,?,?,?)
            """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

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
    precio_con_iva REAL NOT NULL
);
""")
#Cargar datos de facturas
with open("registroFacturas.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO Facturas(id_factura, id_dueno, id_animal, tratamiento, fecha_factura, precio_sin_iva, precio_con_iva)
            VALUES(?,?,?,?,?,?,?)
            """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


#TRATAMIENTOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tratamientos(
    id_tratamiento INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tratamiento TEXT NOT NULL,
    precio_sin_iva REAL NOT NULL
);
""")
#Cargar datos de tratamientos
with open("registroTratamientos.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO Tratamientos(id_tratamiento, nombre_tratamiento, precio_sin_iva)
            VALUES(?,?,?)
            """, (row[0], row[1], row[2]))


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
# Insertar las citas en la tabla
citas_db = [{"id_cita", "id_animal", "id_dueno", "fecha_inicio", "fecha_fin", "tratamiento"}]
for cita in citas_db:
    cursor.execute("""
    INSERT INTO Citas (id_cita, id_animal, id_dueno, fecha_inicio, fecha_fin, tratamiento)
    VALUES (?,?,?,?,?,?)
    """, (cita["fecha"], cita["hora"], cita["id_dueno"], cita["descripcion"]))

conn.commit()
conn.close()  # Close the connection to the database