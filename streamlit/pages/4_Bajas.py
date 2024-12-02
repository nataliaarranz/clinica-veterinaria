import streamlit as st
import requests

# Clase para manejar la lógica de la baja de dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def dar_baja(self, dni_dueno):
        try:
            response = requests.delete(f"{self.backend_url}/{dni_dueno}")
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, "No existe un dueño con el DNI introducido."
            else:
                return False, f"Error al dar de baja: {response.status_code}, Detalle: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {e}"

# Clase para manejar la lógica de la baja de animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def dar_baja(self, chip_animal):
        try:
            response = requests.delete(f"{self.backend_url}/{chip_animal}")
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, "No existe un animal con el número de chip introducido."
            else:
                return False, f"Error al dar de baja: {response.status_code}, Detalle: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {e}"

# Clase para manejar la interfaz de usuario
class BajaInterface:
    def __init__(self, dueno_service, animal_service):
        self.dueno_service = dueno_service
        self.animal_service = animal_service

    def crear_formulario_baja_duenos(self):
        st.title("Baja de Dueños 🐾")
        with st.form("dar_baja_dueno"):
            dni_dueno = st.text_input("DNI del dueño a dar de baja", max_chars=10)
            submit_button = st.form_submit_button(label="Dar de baja")
            if submit_button:
                if not dni_dueno.strip():
                    st.error("El campo DNI no puede estar vacío")
                else:
                    success, message = self.dueno_service.dar_baja(dni_dueno)
                    if success:
                        st.success("Se ha dado de baja al dueño correctamente")
                        st.json(message)
                    else:
                        st.error(message)

    def crear_formulario_baja_animal(self):
        st.title("Baja de Animales 🐾")
        with st.form("dar_baja_animal"):
            chip_animal = st.text_input("Chip del animal a dar de baja", max_chars=15)
            submit_button = st.form_submit_button(label="Dar de baja")
            if submit_button:
                if not chip_animal.strip():
                    st.error("El campo chip no puede estar vacío")
                else:
                    success, message = self.animal_service.dar_baja(chip_animal)
                    if success:
                        st.success("Se ha dado de baja al animal correctamente")
                        st.json(message)
                    else:
                        st.error(message)

# Inicialización de servicios y la interfaz
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
baja_interface = BajaInterface(dueno_service, animal_service)

# Interfaz de usuario principal
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("¿Desea dar de baja a un dueño o un animal?", ["Dueño", "Animal"])
if opcion == "Dueño":
    baja_interface.crear_formulario_baja_duenos()
elif opcion == "Animal":
    baja_interface.crear_formulario_baja_animal()