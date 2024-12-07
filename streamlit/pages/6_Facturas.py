import streamlit as st
import requests
from datetime import datetime
import os
import pandas as pd




class FacturaRepository:
    def __init__(self, filename: str):
        self.filename = filename

    def get_all(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df.to_dict(orient="records")
        return []

    def add(self, factura):
        nuevo_registro = pd.DataFrame([factura])
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = pd.concat([df, nuevo_registro], ignore_index=True)
        else:
            df = nuevo_registro
        df.to_csv(self.filename, index=False)

# Clase para manejar la lógica de los dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def obtener_duenos(self):
        try:
            response = requests.get(self.backend_url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener dueños: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            st.error(f"Error al obtener dueños: {e}")
            return []

# Clase para manejar la lógica de los animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def obtener_animales(self):
        try:
            response = requests.get(self.backend_url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener animales: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            st.error(f"Error al obtener animales: {e}")
            return []

# Clase para manejar la lógica de la factura
class Factura:
    def __init__(self, nombre_dueno, nombre_animal, tratamiento, precio_sin_iva):
        self.nombre_dueno = nombre_dueno
        self.nombre_animal = nombre_animal
        self.tratamiento = tratamiento
        self.precio_sin_iva = precio_sin_iva
        self.iva = 0.21  # IVA del 21%
        self.fecha = datetime.now()  # Agregar la fecha aquí

    def precio_con_iva(self):
        return self.precio_sin_iva * (1 + self.iva)

    def mostrar_factura(self):
        st.subheader("Factura de Consulta Veterinaria")
        st.write(f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Nombre del Dueño: {self.nombre_dueno}")
        st.write(f"Nombre del Animal: {self.nombre_animal}")
        st.write("Tratamiento realizado:")
        st.write(f"- {self.tratamiento} - {self.precio_sin_iva:.2f}€ (sin IVA)")
        st.write(f"- {self.tratamiento} - {self.precio_con_iva():.2f}€ (con IVA)")
        st.write(f"**Total a Pagar: {self.precio_con_iva():.2f}€**")
        st.write(f"**Información del Centro**")
        st.write("Clinica Veterinaria Cuatro Patas")
        st.write("Ubicación: Paseo de la Castellana, 14")
        st.write("Teléfono: 912457890")

    # En el método guardar_factura
    def guardar_factura(self, repository):
        # Crear un diccionario con los datos de la factura
        factura_data = {
            "nombre_dueno": self.nombre_dueno,
            "nombre_animal": self.nombre_animal,
            "tratamiento": self.tratamiento,
            "importe_con_iva": self.precio_con_iva(),  # Aquí se llama al método
            "fecha": self.fecha.strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha
        }
        
        # Hacer una solicitud POST al servidor para guardar la factura
        response = requests.post("http://fastapi:8000/alta_factura/", json=factura_data)
        
        if response.status_code == 200:
            st.success("Factura guardada exitosamente.")
        else:
            st.error(f"Error al guardar la factura: {response.text}")

class Consulta:
    def __init__(self, dueno_service, animal_service, factura_repository):
        self.dueno_service = dueno_service
        self.animal_service = animal_service
        self.factura_repository = factura_repository  # Agregar el repositorio de facturas
        self.tratamientos = {
            "Análisis": 15,
            "Vacunación": 15,
            "Desparasitación": 25,
            "Revisión general": 30,
            "Revisión cardiología": 55,
            "Revisión cutánea": 45,
            "Revisión broncología": 35,
            "Ecografías": 50,
            "Limpieza bucal": 50,
            "Extracción de piezas dentales": 70,
            "Cirugía": 250
        }

    def registrar_consulta(self):
        st.title("Registro de Consulta Veterinaria")

        # Obtener los datos de dueños y animales
        duenos = self.dueno_service.obtener_duenos()
        animales = self.animal_service.obtener_animales()

        if not duenos or not animales:
            st.error("No se han podido obtener los datos necesarios.")
            return

        # Selección de dueño y animal
        nombre_dueno = st.selectbox("Selecciona el dueño:", [dueno["nombre_dueno"] for dueno in duenos])
        nombre_animal = st.selectbox("Selecciona el animal:", [animal["nombre_animal"] for animal in animales])

        # Selección del tratamiento
        tratamiento_seleccionado = st.selectbox("Selecciona el tipo de tratamiento:", list(self.tratamientos.keys()))
        precio_sin_iva = self.tratamientos[tratamiento_seleccionado]

        if st.button("Generar Factura"):
            if nombre_dueno and nombre_animal and tratamiento_seleccionado:
                factura = Factura(nombre_dueno, nombre_animal, tratamiento_seleccionado, precio_sin_iva)
                factura.mostrar_factura()
                
                # Guardar la factura en el repositorio
                factura.guardar_factura(self.factura_repository)
                st.success("Factura guardada exitosamente.")
            else:
                st.error("Por favor, completa todos los campos.")
def main():
    # URL del microservicio FastAPI
    animales_backend = "http://fastapi:8000/animales"
    duenos_backend = "http://fastapi:8000/duenos"

    # Crear instancias de los servicios
    dueno_service = DuenoService(duenos_backend)
    animal_service = AnimalService(animales_backend)

    # Crear instancia del repositorio de facturas
    factura_repository = FacturaRepository("registroFacturas.csv")

    # Crear instancia de la clase Consulta
    consulta = Consulta(dueno_service, animal_service, factura_repository)

    # Llamar a la función para registrar la consulta y generar la factura
    consulta.registrar_consulta()

if __name__ == "__main__":
    main()