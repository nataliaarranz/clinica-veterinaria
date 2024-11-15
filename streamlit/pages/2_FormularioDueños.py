import streamlit as st
import requests

st.title("Formulario para dar de alta dueños 🖥️🖥")
url = "http://fastapi:8000/alta_dueños"


# Guardar datos del dueño
def guardar_datos_dueño(nombre_dueño, dni_dueño, telefono_dueño, direccion_dueño, email_dueño):
    payload = {
        "nombre_dueño": nombre_dueño,
        "dni_dueño": dni_dueño,
        "telefono_dueño": telefono_dueño,
        "direccion_dueño": direccion_dueño,
        "email_dueño": email_dueño
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
        st.error(f"Error de conexión al enviar los datos: {e}")


# Procesar formulario
def procesar_formulario_dueños(nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño):
    # Validar campos completos
    if not all([nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño]):
        st.error("Obligatorio rellenar todos los campos.")
        return
    # Guardar datos en CSV
    guardar_datos_dueño(nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño)


# Crear formulario
def crear_formulario_dueños():
    st.title("Registro de Dueños🐾")

    with st.form("registro_dueños"):
        # Datos del dueño
        st.subheader("Datos del dueño")
        nombre_dueño = st.text_input("Nombre del dueño: ", max_chars=50)
        telefono_dueño = st.text_input("Telefono del dueño: ", max_chars=50)
        email_dueño = st.text_input("Correo del dueño: ")
        dni_dueño = st.text_input("DNI del dueño: ", max_chars=10)
        direccion_dueño = st.text_input("Domicilio: ")
        submit_button = st.form_submit_button(label="Dar de alta")

        if submit_button:
            procesar_formulario_dueños(nombre_dueño, telefono_dueño, email_dueño, dni_dueño, direccion_dueño)


# Llamar función crear formulario
crear_formulario_dueños()
