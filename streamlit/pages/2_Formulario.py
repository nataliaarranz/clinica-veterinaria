import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import os

# URL del microservicio FastAPI
url = "http://fastapi:8000/alta_animal/"

# Archivo CSV donde se guardan los datos de los dueños y animales
registro_csv = "registro_dueños_animales.csv"

def crear_formulario():
    st.title("Registro de Dueños y Animales 🐾")

# Crear el formulario
    with st.form("registro_animales"):
        # Datos del dueño
        st.subheader("Datos del dueño")
        nombre_dueño = st.text_input("Nombre del dueño: ", max_chars = 50)
        telefono_dueño = st.text_input("Telefono del dueño: ", max_chars = 50)
        email_dueño = st.text_input("Correo del dueño: ")
        dni_dueño = st.text_input("DNI del dueño: ", max_chars = 10)
        direccion_dueño = st.text_input("Domicilio: ")

        # Datos del animal
        st.subheader("Datos del animal")
        nombre_animal = st.text_input("Nombre del animal: ")
        especie_animal = st.selectbox("Especie", ["Perro", "Gato"])
        fecha_nacimiento_animal = st.date_input("Fecha de nacimiento: ", datetime.today())
        sexo_animal = st.selectbox("Sexo", ["Macho", "Hembra"])

        # Envío del formulario
        submit_button = st.form_submit_button("Registrar Dueño y Animal")

# Procesar los datos del formulario
    if submit_button:
        procesar_formulario(nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño, nombre_animal, especie_animal, fecha_nacimiento_animal, sexo_animal)

def procesar_formulario(nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño, nombre_animal, especie_animal, fecha_nacimiento_animal, sexo_animal):
    payload = {
        "nombre_dueño": nombre_dueño,
        "telefono_dueño": telefono_dueño,
        "email_dueño": email_dueño,
        "dni_dueño": dni_dueño,
        "direccion_dueño": direccion_dueño,
        "nombre_animal": nombre_animal,
        "especie_animal": especie_animal,
        "fecha_nacimiento_animal": fecha_nacimiento_animal.strftime("%Y-%m-%d"),
        "sexo_animal": sexo_animal
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        st.success("Dueño y Animal registrados correctamente")
        guardar_datos_csv(payload)
    except requests.exceptions.RequestException as e:
        st.error(f"No se pudo dar de alta, error: {e}")

def guardar_datos_csv(payload):
    if os.path.exists(registro_csv):
        registro_df = pd.read_csv(registro_csv)
    else:
        registro_df = pd.DataFrame(columns=["nombre_dueño", "telefono_dueño", "email_dueño", "dni_dueño", "direccion_dueño", "nombre_animal", "especie_animal", "fecha_nacimiento_animal", "sexo_animal"])

    nuevo_registro = pd.DataFrame([payload])
    registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
    registro_df.to_csv(registro_csv, index=False)

def buscar_registros():
    st.header("Buscar Registros por DNI del Dueño")
    nombre_dueño_buscar = st.text_input("Ingrese el nombre del dueño para buscar", key="buscar_dueño")
    
    if st.button("Buscar", key="boton_buscar_dueño"):
        if nombre_dueño_buscar:
            if os.path.exists(registro_csv):
                df_merged = pd.read_csv(registro_csv)
                df_resultados = df_merged[df_merged['nombre_dueño'].str.contains(nombre_dueño_buscar, case=False, na=False)]
                if not df_resultados.empty:
                    st.write("Resultados de la Búsqueda: ")
                    st.dataframe(df_resultados)
                else:
                    st.error("No se encontraron registros para ese dueño.")
            else:
                st.warning("El archivo de registro no existe. Registre al menos un dueño y animal primero.")
        else:
            st.warning("Por favor, ingrese un nombre para buscar")

# Ejecutar funciones
crear_formulario()
buscar_registros()
   
        
# --- SECCIÓN DE BÚSQUEDA DE DUEÑOS ---
st.header("Buscar Registros por DNI del Dueño")
nombre_dueño_buscar = st.text_input("Ingrese el nombre del dueño para buscar", key = "buscar_dueño")
if st.button("Buscar", key = "boton_buscar_dueño"):
    if nombre_dueño_buscar:
        if os.path.exists(registro_csv):
            # Cargamos los datos del CSV
            df_merged = pd.read_csv(registro_csv)
            # Filtrar el DataFrame para encontrar registros que coincidan con el nombre del dueño
            df_resultados = df_merged[df_merged['nombre_dueño']. str. contains(nombre_dueño_buscar, case = False, na = False)]
            # Mostrar los resultados
            if not df_resultados.empty:
                st.write("Resultados de la Búsqueda: ")
                st.dataframe(df_resultados)
            else: 
                st.error("No se encontraron registros para ese dueño.")
        else:
            st.warning("El archivo de registro no existe. Registre al menos un dueño y animal primero.")
    else: 
        st.warning("Por favor, ingrese un nombre para buscar")
