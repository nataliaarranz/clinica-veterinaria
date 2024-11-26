import streamlit as st
import requests

st.title("Formulario para dar de alta duenos 🖥️🖥")
url = "http://fastapi:8000/alta_duenos"

# Guardar datos del dueno
def guardar_datos_dueno(nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno):
    payload = {
        "nombre_dueno": nombre_dueno,
        "telefono_dueno": telefono_dueno,
        "email_dueno": email_dueno,
        "dni_dueno": dni_dueno,
        "direccion_dueno": direccion_dueno
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
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexion al enviar los datos: {e}")

# Procesar formulario
def procesar_formulario_duenos(nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno):
    # Validar campos completos
    if not all([nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno]):
        st.error("Obligatorio rellenar todos los campos.")
        return
    # Guardar datos en CSV
    guardar_datos_dueno(nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno)

# Crear formulario
def crear_formulario_duenos():
    st.title("Registro de Dueños🐾")

    with st.form("registro_duenos"):
        # Datos del dueno
        st.subheader("Datos del dueño")
        nombre_dueno = st.text_input("Nombre del dueño: ", max_chars=50)
        telefono_dueno = st.text_input("Telefono del dueño: ", max_chars=50)
        email_dueno = st.text_input("Correo del dueño: ")
        dni_dueno = st.text_input("DNI del dueño: ", max_chars=10)
        direccion_dueno = st.text_input("Domicilio: ")
        submit_button = st.form_submit_button(label="Dar de alta")

        if submit_button:
            procesar_formulario_duenos(nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno)

# Llamar función crear formulario
crear_formulario_duenos()