import streamlit as st
import requests

st.title("Gestión de baja Dueños o Animales 🖥️🖥")
url = "http://fastapi:8000/baja"


#Dar de baja DUEÑO
def dar_baja_dueño(dni_dueño):
    try:
        response = requests.delete(f"{url}/{dni_dueño}")
        if response.status_code == 200:
            st.success("Se ha dado de baja al dueño correctamente")
            #Respuesta de microservicio
            st.json(response.json())
        elif response.status_code == 404:
            st.error("No existe un dueño con el DNI introducido.")
        else:
            st.error(f"Error al dar de baja: {response.status_code}")
            st.error(f"Detalle: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")

#Formulario para dar de baja dueño
def crear_formulario_baja_dueños():
    st.title("Baja de Dueños 🐾")
    
    with st.form("dar_baja_dueño"):
        st.subheader("Ingrese el DNI del dueño que desea dar de baja")
        dni_dueño = st.text_input("DNI del dueño", max_chars= 10)
        submit_button = st.form_submit_button(label="Dar de baja")
        
        if submit_button:
            dar_baja_dueño(dni_dueño)


#Dar de baja ANIMAL
def dar_baja_animal(chip_animal):
    try:
        response = requests.delete(f"{url}/{chip_animal}")
        if response.status_code == 200:
            st.success("Se ha dado de baja al animal correctamente")
            #Respuesta de microservicio
            st.json(response.json())
        elif response.status_code == 404:
            st.error("No existe un animal con el número de chip introducido.")
        else:
            st.error(f"Error al dar de baja: {response.status_code}")
            st.error(f"Detalle: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
#Formulario para dar de baja animal
def crear_formulario_baja_animal():
    st.title("Baja de Animales 🐾")
    with st.form("dar_baja_animal"):
        st.subheader("Ingrese el chip del animal que desea dar de baja")
        chip_animal = st.text_input("Chip del animal", max_chars= 10)
        submit_button = st.form_submit_button(label="Dar de baja")
        
        if submit_button:
            dar_baja_animal(chip_animal)


#Mostrar formularios
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("¿Desea dar de baja a un dueño o un animal?", ["Dueño", "Animal"])
if opcion == "Dueño":
    crear_formulario_baja_dueños()
elif opcion == "Animal":
    crear_formulario_baja_animal()