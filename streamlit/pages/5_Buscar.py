import streamlit as st 
import requests 

# Título de la aplicación 
st.title("Buscar Dueños de Mascotas 🐾") 

 # URL del microservicio (ajusta según tu configuración) 
backend = "http://fastapi:8000/buscar_dueño"
dueños_backend = "http://fastapi:8000/dueños"
animales_backend = "http://fastapi:8000/animales"

# Función para buscar datos del dueño 
def buscar_dueño(dni_dueño): 
    try: 
        response = requests.get(dueños_backend) 
        # Mostrar el resultado de la solicitud 
        if response.status_code == 200: 
            return response.json() # Retornar los datos del dueño 
        elif response.status_code == 404: 
            st.error("No existe dueño con el DNI introducido") 
            return None 
        else: 
            st.error(f"Error al buscar los datos: {response.status_code}") 
            st.error(f"Detalle: {response.text}") 
            return None 
    except requests.exceptions.RequestException as e: 
        st.error(f"Error de conexión al buscar los datos: {e}") 
        return None 

# Procesar el formulario 
def procesar_formulario_busqueda_dueño(dni_dueño): 
    if not dni_dueño: 
        st.error("Obligatorio ingresar un DNI.") 
        return 
    # Buscar datos del dueño 
    datos_dueño = buscar_dueño(dni_dueño) 
    if datos_dueño: 
        st.success("Dueño encontrado:") 
        st.json(datos_dueño) # Mostrar los datos del dueño 

# Crear el formulario 
def crear_formulario_busqueda_dueño(): 
    st.subheader("Buscar Dueño") # Esta línea no debe tener ':' después 
    with st.form("buscar_dueños"): 
        dni_dueño = st.text_input("DNI del dueño: ", max_chars=10) 
        submit_button = st.form_submit_button(label="Buscar") 
        if submit_button: 
            procesar_formulario_busqueda_dueño(dni_dueño) 


# Función para buscar datos del animal 
def buscar_animal(chip_animal): 
    try: 
        response = requests.get(animales_backend) 
        # Mostrar el resultado de la solicitud 
        if response.status_code == 200: 
            return response.json() # Retornar los datos del animal 
        elif response.status_code == 404: 
            st.error("No existe animal con el chip introducido") 
            return None 
        else: 
            st.error(f"Error al buscar los datos: {response.status_code}") 
            st.error(f"Detalle: {response.text}") 
            return None 
    except requests.exceptions.RequestException as e: 
        st.error(f"Error de conexión al buscar los datos: {e}") 
        return None 

# Procesar el formulario 
def procesar_formulario_busqueda_animal(chip_animal): 
    if not chip_animal: 
        st.error("Obligatorio ingresar un chip.") 
        return 
    # Buscar datos del animal 
    datos_animal = buscar_animal(chip_animal) 
    if datos_animal: 
        st.success("Animal encontrado:") 
        st.json(datos_animal) # Mostrar los datos del animal 

# Crear el formulario 
def crear_formulario_busqueda_animal(): 
    st.subheader("Buscar Animal") # Esta línea no debe tener ':' después 
    with st.form("buscar_animales"): 
        chip_animal = st.text_input("Chip del animal: ", max_chars=10) 
        submit_button = st.form_submit_button(label="Buscar") 
        if submit_button: 
            procesar_formulario_busqueda_animal(chip_animal) 

# Llamar a la función para crear el formulario
#Mostrar formularios
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("¿Desea dar de baja a un dueño o un animal?", ["Dueño", "Animal"])
if opcion == "Dueño":
    crear_formulario_busqueda_dueño() 
elif opcion == "Animal":
    crear_formulario_busqueda_animal()
