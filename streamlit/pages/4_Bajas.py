import streamlit as st
import requests

st.title("Gestión de baja Dueños o Animales 🖥️🖥")
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

def dar_baja_dueno(dni_dueno):
    try:
        response = requests.delete(f"{duenos_backend}/{dni_dueno}")
        if response.status_code == 200:
            st.success("Se ha dado de baja al dueño correctamente")
            st.json(response.json())
        elif response.status_code == 404:
            st.error("No existe un dueño con el DNI introducido.")
        else:
            st.error(f"Error al dar de baja: {response.status_code}")
            st.error(f"Detalle: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")

def crear_formulario_baja_duenos():
    st.title("Baja de Dueños 🐾")
    with st.form("dar_baja_dueno"):
        dni_dueno = st.text_input("DNI del dueño a dar de baja", max_chars=10)
        submit_button = st.form_submit_button(label="Dar de baja")
        if submit_button:
            if not dni_dueno.strip():
                st.error("El campo DNI no puede estar vacío")
            else:
                dar_baja_dueno(dni_dueno)

def dar_baja_animal(chip_animal):
    try:
        response = requests.delete(f"{animales_backend}/{chip_animal}")
        if response.status_code == 200:
            st.success("Se ha dado de baja al animal correctamente")
            st.json(response.json())
        elif response.status_code == 404:
            st.error("No existe un animal con el número de chip introducido.")
        else:
            st.error(f"Error al dar de baja: {response.status_code}")
            st.error(f"Detalle: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")

def crear_formulario_baja_animal():
    st.title("Baja de Animales 🐾")
    with st.form("dar_baja_animal"):
        chip_animal = st.text_input("Chip del animal a dar de baja", max_chars=15)
        submit_button = st.form_submit_button(label="Dar de baja")
        if submit_button:
            if not chip_animal.strip():
                st.error("El campo chip no puede estar vacío")
            else:
                dar_baja_animal(chip_animal)

st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("¿Desea dar de baja a un dueño o un animal?", ["Dueño", "Animal"])
if opcion == "Dueño":
    crear_formulario_baja_duenos()
elif opcion == "Animal":
    crear_formulario_baja_animal()
