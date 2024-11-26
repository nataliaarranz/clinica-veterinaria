import requests

# URL del microservicio (ajusta segun tu configuracion)
duenos_backend = "https://fastapi:8000/duenos"
animales_backend = "https://fastapi:8000/animales"

# Funcion para buscar datos del dueno usando tu backend FastAPI
def buscar_dueno(dni_dueno):
    try:
        response = requests.get(f"{duenos_backend}/{dni_dueno}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "No existe dueño con el DNI introducido"}
        else:
            return {"error": f"Error al buscar los datos: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexion al buscar los datos: {e}"}

# Funcion para buscar datos del animal usando tu backend FastAPI
def buscar_animal(chip):
    try:
        response = requests.get(f"{animales_backend}/{chip}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "No existe animal con el chip introducido"}
        else:
            return {"error": f"Error al buscar los datos: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexion al buscar los datos: {e}"}

import streamlit as st

# Titulo de la aplicacion
st.title("Buscar Duños y Animales de Mascotas 🐾")

# Sidebar para seleccion
st.sidebar.title("Opciones de Busqueda")
opcion_buscar = st.sidebar.radio("¿Que desea buscar?", ["Buscar Dueño", "Buscar Animal"])

# Formulario para buscar dueno
def crear_formulario_busqueda_dueno():
    st.subheader("Buscar Dueño")
    dni_dueno = st.text_input("DNI del dueño:", max_chars=10)
    if st.button("Buscar Dueño"):
        resultado = buscar_dueno(dni_dueno)
        if "error" not in resultado:
            st.success("Dueño encontrado:")
            st.json(resultado)
        else:
            st.error(resultado["error"])

# Formulario para buscar animal
def crear_formulario_busqueda_animal():
    st.subheader("Buscar Animal por Chip")
    chip_animal = st.text_input("Chip del animal:", max_chars=15)
    if st.button("Buscar Animal"):
        resultado = buscar_animal(chip_animal)
        if "error" not in resultado:
            st.success("Animal encontrado:")
            st.json(resultado)
        else:
            st.error(resultado["error"])

# Logica para mostrar formularios basada en la seleccion del sidebar
if opcion_buscar == "Buscar Dueño":
    crear_formulario_busqueda_dueno()
elif opcion_buscar == "Buscar Animal":
    crear_formulario_busqueda_animal()