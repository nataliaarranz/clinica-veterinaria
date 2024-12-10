import streamlit as st
import requests
import re
import time

# Clase para representar a un dueno
class Dueno:
    def __init__(self, nombre, telefono, email, dni, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.dni = dni
        self.direccion = direccion

class Validador:
    @staticmethod
    def validar_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validar_dueno(dueno):
        if not all([dueno.nombre, dueno.telefono, dueno.email, dueno.dni, dueno.direccion]):
            return "Obligatorio rellenar todos los campos."
        if re.search(r'\d', dueno.nombre):
            return "El nombre del dueno no debe contener números."
        if not dueno.telefono.isdigit() or len(dueno.telefono) < 7:
            return "El teléfono del dueno debe contener solo números y tener al menos 7 dígitos."
        if not Validador.validar_email(dueno.email):
            return "El correo electrónico no tiene un formato válido."
        return None

class DuenoService:
    def __init__(self, url):
        self.url = url

    def guardar_datos(self, dueno):
        # Aquí podrías enviar los datos a un microservicio
        payload = {
            "nombre_dueno": dueno.nombre,
            "telefono_dueno": dueno.telefono,
            "email_dueno": dueno.email,
            "dni_dueno": dueno.dni,
            "direccion_dueno": dueno.direccion
        }
        return self.enviar_datos(payload)

    def enviar_datos(self, payload):
        try:
            response = requests.post(self.url, json=payload)
            return response  # Devuelve la respuesta
        except requests.exceptions.RequestException as e:
            return None  # Devuelve None en caso de error

def crear_formulario_duenos():
    st.title("Registro de Dueno🐾")
    url = "http://fastapi:8000/alta_duenos"  # Cambia esta URL según tu microservicio
    dueno_service = DuenoService(url)

    with st.form("registro_duenos"):
        st.subheader("Datos del dueno")
        nombre_dueno = st.text_input("Nombre del dueno: ", max_chars=50)
        telefono_dueno = st.text_input("Teléfono del dueno: ", max_chars=10)
        email_dueno = st.text_input("Correo del dueno: ")
        dni_dueno = st.text_input("DNI del dueno: ", max_chars=10)
        direccion_dueno = st.text_input("Domicilio: ")
        submit_button = st.form_submit_button(label="Dar de alta")

        if submit_button:
            dueno = Dueno(nombre_dueno, telefono_dueno, email_dueno, dni_dueno, direccion_dueno)
            error = Validador.validar_dueno(dueno)

            if error:
                st.error(error)
            else:
                # Crear un contenedor vacío para la animación
                with st.empty():
                    # Animación de carga
                    for i in range(5):
                        if i == 0:
                            st.write("👤 Registrando dueño...")
                        elif i == 1:
                            st.write("👤👤 Verificando datos...")
                        elif i == 2:
                            st.write("👤👤👤 Guardando en la base de datos...")
                        elif i == 3:
                            st.write("👤👤👤👤 Casi listo...")
                        else:
                            st.write("👤👤👤👤👤 ¡Completado!")
                        time.sleep(0.5)

                response = dueno_service.guardar_datos(dueno)
                if response is not None and response.status_code == 200:
                    # Animación de éxito
                    success_placeholder = st.empty()
                    for emoji in ["🎉", "🌟", "✨", "🎊", "🏆"]:
                        success_placeholder.markdown(f"### {emoji} ¡Dueño registrado con éxito! {emoji}")
                        time.sleep(0.3)
                    
                    # Mensaje final
                    st.success("¡Registro completado correctamente!")
                    st.json(response.json())
                else:
                    error_message = "Error de conexión" if response is None else response.json().get("detail", "Error desconocido")
                    st.error(f"Error al enviar los datos: {error_message}")

# Ejecutar la función para crear el formulario
if __name__ == "__main__":
    crear_formulario_duenos()