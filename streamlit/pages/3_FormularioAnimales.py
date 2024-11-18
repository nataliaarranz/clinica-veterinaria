##CÓDIGO ORIGINAL RAÚL
import streamlit as st
import requests
from datetime import datetime

# URL del microservicio FastAPI
url = "http://fastapi:8000/alta_animal"

#ALTA DE ANIMALES
st.title("Formulario para dar de alta animales 🖥️🖥")

#Guardar datos del dueño
def guardar_datos_animales(nombre_animal, numero_chip_animal, especie_animal, fecha_nacimiento_animal, sexo_animal):
    payload = {
        "nombre_animal": nombre_animal,
        "chip_animal": numero_chip_animal,
        "especie_animal": especie_animal,
        "fecha_nacimiento_animal": fecha_nacimiento_animal,
        "sexo": sexo_animal
    }
    # Enviar los datos al microservicio
    try:
        response = requests.post(url, json=payload)
        # Mostrar el resultado de la solicitud
        if response.status_code == 200:
            st.success("Datos enviados correctamente")
            st.json(response.json())  # Mostrar la respuesta del microservicio
        else:
            st.error(f"Error al enviar los datos: {response.status_code}")
            st.error(f"Detalle: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al enviar los datos: {e}")

#Procesar formulario
def procesar_formulario_animales(nombre_animal, numero_chip_animal, especie_animal, fecha_nacimiento_animal, sexo_animal):
    #Validar campos completos
    if not all([nombre_animal, numero_chip_animal, especie_animal, fecha_nacimiento_animal, sexo_animal]):
        st.error("Obligatorio rellenar todos los campos.")
        return
    #Guardar datos en CSV
    guardar_datos_animales(nombre_animal, numero_chip_animal, especie_animal, fecha_nacimiento_animal, sexo_animal)

#Crear formulario
def crear_formulario_animales():
    st.title("Registro de Animales🐾")
    with st.form("registro_animales"):
        # Datos del animales
        st.subheader("Datos del animal")
        nombre_animal = st.text_input("Nombre del animal: ", max_chars = 50)
        numero_chip_animal = st.text_input("Número de chip de animal: ", max_chars = 50)
        especie_animal = st.text_input("Especie del animal: ")
        fecha_nacimiento_animal = st.date_input("Fecha de nacimiento del animal: ")
        sexo_animal = st.selectbox("Sexo del animal: ", ["Macho", "Hembra"])
        submit_button = st.form_submit_button(label="Dar de alta animal")
        
        if submit_button:
            procesar_formulario_animales(nombre_animal, numero_chip_animal, especie_animal, fecha_nacimiento_animal.strftime("%Y-%m-%d"), sexo_animal)
#Llamar función crear formulario
crear_formulario_animales()

