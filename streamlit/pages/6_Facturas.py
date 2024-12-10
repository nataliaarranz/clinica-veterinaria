import streamlit as st
import requests
from datetime import datetime
import os
import pandas as pd
import time




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
        self.iva = 0.21
        self.fecha = datetime.now()
        self.numero_factura = self._generar_numero_factura()

    def _generar_numero_factura(self):
        return f"F{self.fecha.strftime('%Y%m%d%H%M%S')}"

    def precio_con_iva(self):
        return self.precio_sin_iva * (1 + self.iva)

    def mostrar_factura(self):
        # Primero, mostramos el título de la página
        st.markdown("""
            <div style='background: linear-gradient(120deg, #2B4162 0%, #12100E 100%); 
                        padding: 2rem; 
                        border-radius: 10px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                <h1 style='color: white; 
                           font-size: 2.2rem; 
                           margin-bottom: 0.5rem; 
                           text-align: center;
                           font-weight: 600;'>
                    🧾 Factura Clínica Veterinaria 🧾
                </h1>
            </div>
        """, unsafe_allow_html=True)

        # Luego, creamos un contenedor para la factura
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                # Datos de la clínica
                st.markdown("""
                    <div style='text-align: center; margin-bottom: 2rem;'>
                        <h2 style='color: #2B4162; font-size: 1.8rem;'>Clínica Veterinaria Cuatro Patas</h2>
                        <p style='color: #666;'>
                            Paseo de la Castellana, 14 • Madrid<br>
                            Tel: 912457890 • CIF: B12345678
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                # Datos del cliente y factura
                st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; margin-bottom: 2rem;'>
                        <div>
                            <h3 style='color: #2B4162;'>📋 Datos del Cliente</h3>
                            <p><strong>Cliente:</strong> {self.nombre_dueno}</p>
                            <p><strong>Paciente:</strong> {self.nombre_animal}</p>
                        </div>
                        <div style='text-align: right;'>
                            <h3 style='color: #2B4162;'>🧾 Factura</h3>
                            <p><strong>Nº:</strong> {self.numero_factura}</p>
                            <p><strong>Fecha:</strong> {self.fecha.strftime('%d/%m/%Y %H:%M')}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Tabla de conceptos
                st.markdown("<h3 style='color: #2B4162; margin-bottom: 1rem;'>Detalles de la factura</h3>", unsafe_allow_html=True)
                
                df = pd.DataFrame({
                    'Concepto': [self.tratamiento, 'IVA (21%)', 'Total'],
                    'Importe': [
                        f"{self.precio_sin_iva:.2f}€",
                        f"{(self.precio_sin_iva * self.iva):.2f}€",
                        f"{self.precio_con_iva():.2f}€"
                    ]
                })
                
                st.dataframe(
                    df,
                    hide_index=True,
                    column_config={
                        "Concepto": st.column_config.TextColumn("Concepto", width="medium"),
                        "Importe": st.column_config.TextColumn("Importe", width="small")
                    }
                )

                # Mensaje final
                st.markdown("""
                    <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 10px;'>
                        <small style='color: #666;'>
                            Esta factura sirve como justificante de pago
                        </small>
                    </div>
                """, unsafe_allow_html=True)

    def guardar_factura(self, repository):
        with st.spinner("Guardando factura..."):
            time.sleep(0.5)
            factura_data = {
                "numero_factura": self.numero_factura,
                "nombre_dueno": self.nombre_dueno,
                "nombre_animal": self.nombre_animal,
                "tratamiento": self.tratamiento,
                "importe_sin_iva": self.precio_sin_iva,
                "importe_con_iva": self.precio_con_iva(),
                "fecha": self.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            response = requests.post("http://fastapi:8000/alta_factura/", json=factura_data)
            
            if response.status_code == 200:
                repository.add(factura_data)
            else:
                st.error(f"❌ Error al guardar la factura: {response.text}")

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
        # Título con estilo mejorado
        st.markdown("""
            <div style='background: linear-gradient(120deg, #2B4162 0%, #12100E 100%); 
                        padding: 2rem; 
                        border-radius: 10px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                <h1 style='color: white; 
                           font-size: 2.2rem; 
                           margin-bottom: 0.5rem; 
                           text-align: center;
                           font-weight: 600;'>
                    💉 Registro de Consulta Veterinaria
                </h1>
            </div>
        """, unsafe_allow_html=True)

        # Contenedor principal
        with st.container():
            # Obtener los datos
            duenos = self.dueno_service.obtener_duenos()
            animales = self.animal_service.obtener_animales()

            if not duenos or not animales:
                st.error("❌ No se han podido obtener los datos necesarios.")
                return

            # Crear columnas para mejor organización
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
                        <h3 style='color: #2B4162; margin-bottom: 1rem;'>👤 Información del Cliente</h3>
                    </div>
                """, unsafe_allow_html=True)
                nombre_dueno = st.selectbox(
                    "Selecciona el dueño:",
                    [dueno["nombre_dueno"] for dueno in duenos],
                    key="dueno_select"
                )
                nombre_animal = st.selectbox(
                    "Selecciona el animal:",
                    [animal["nombre_animal"] for animal in animales],
                    key="animal_select"
                )

            with col2:
                st.markdown("""
                    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
                        <h3 style='color: #2B4162; margin-bottom: 1rem;'>💊 Detalles del Tratamiento</h3>
                    </div>
                """, unsafe_allow_html=True)
                tratamiento_seleccionado = st.selectbox(
                    "Selecciona el tipo de tratamiento:",
                    list(self.tratamientos.keys()),
                    key="tratamiento_select"
                )
                precio_sin_iva = self.tratamientos[tratamiento_seleccionado]
                
                # Mostrar precio
                st.markdown(f"""
                    <div style='background: #e9ecef; 
                               padding: 1rem; 
                               border-radius: 8px; 
                               margin-top: 1rem;
                               text-align: center;'>
                        <p style='color: #2B4162; 
                                 font-size: 1.1rem; 
                                 margin: 0;'>
                            Precio sin IVA: <strong>{precio_sin_iva:.2f}€</strong>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # Botón centrado con estilo
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(
                    "Generar Factura",
                    type="primary",
                    use_container_width=True,
                ):
                    if nombre_dueno and nombre_animal and tratamiento_seleccionado:
                        with st.spinner("Generando factura..."):
                            factura = Factura(nombre_dueno, nombre_animal, tratamiento_seleccionado, precio_sin_iva)
                            factura.mostrar_factura()
                            factura.guardar_factura(self.factura_repository)
                    else:
                        st.error("❌ Por favor, completa todos los campos.")

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