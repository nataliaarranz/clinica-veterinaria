import requests
import streamlit as st

# URL del microservicio (ajusta según tu configuración)
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

# Función para buscar datos del dueño usando tu backend FastAPI
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
        return {"error": f"Error de conexión al buscar los datos: {e}"}

# Función para buscar datos del animal usando tu backend FastAPI
def buscar_animal(chip_animal):
    try:
        response = requests.get(f"{animales_backend}/{chip_animal}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "No existe animal con el chip introducido"}
        else:
            return {"error": f"Error al buscar los datos: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexión al buscar los datos: {e}"}

# Lógica para la interfaz de usuario en Streamlit
st.title("Buscar Dueños y Animales de Mascotas 🐾")

# Sidebar para selección
st.sidebar.title("Opciones de Búsqueda")
opcion_buscar = st.sidebar.radio("¿Qué desea buscar?", ["Buscar Dueño", "Buscar Animal"])

# Formulario para buscar dueño
if opcion_buscar == "Buscar Dueño":
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
elif opcion_buscar == "Buscar Animal":
    st.subheader("Buscar Animal por Chip")
    chip_animal = st.text_input("Chip del animal:", max_chars=15)
    if st.button("Buscar Animal"):
        resultado = buscar_animal(chip_animal)
        if "error" not in resultado:
            st.success("Animal encontrado:")
            st.json(resultado)
        else:
            st.error(resultado["error"])