import requests
import streamlit as st

# Clase para manejar la lógica de búsqueda de dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def buscar(self, dni_dueno):
        try:
            response = requests.get(f"{self.backend_url}/{dni_dueno}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "No existe dueño con el DNI introducido"}
            else:
                return {"error": f"Error al buscar los datos: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error de conexión al buscar los datos: {e}"}

# Clase para manejar la lógica de búsqueda de animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def buscar(self, chip_animal):
        try:
            response = requests.get(f"{self.backend_url}/{chip_animal}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "No existe animal con el chip introducido"}
            else:
                return {"error": f"Error al buscar los datos: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error de conexión al buscar los datos: {e}"}

# Clase para manejar la interfaz de usuario
class SearchInterface:
    def __init__(self, dueno_service, animal_service):
        self.dueno_service = dueno_service
        self.animal_service = animal_service

    def buscar_dueno(self):
        st.subheader("Buscar Dueño")
        dni_dueno = st.text_input("DNI del dueño:", max_chars=10)
        if st.button("Buscar Dueño"):
            resultado = self.dueno_service.buscar(dni_dueno)
            if "error" not in resultado:
                st.success("Dueño encontrado:")
                st.json(resultado)
            else:
                st.error(resultado["error"])

    def buscar_animal(self):
        st.subheader("Buscar Animal por Chip")
        chip_animal = st.text_input("Chip del animal:", max_chars=15)
        if st.button("Buscar Animal"):
            resultado = self.animal_service.buscar(chip_animal)
            if "error" not in resultado:
                st.success("Animal encontrado:")
                st.json(resultado)
            else:
                st.error(resultado["error"])

# Inicialización de servicios y la interfaz
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
search_interface = SearchInterface(dueno_service, animal_service)

# Lógica de la interfaz de usuario principal
st.title("Buscar Dueños y Animales de Mascotas 🐾")

# Sidebar para selección
st.sidebar.title("Opciones de Búsqueda")
opcion_buscar = st.sidebar.radio("¿Qué desea buscar?", ["Buscar Dueño", "Buscar Animal"])

# Mostrar el formulario correspondiente según la opción seleccionada
if opcion_buscar == "Buscar Dueño":
    search_interface.buscar_dueno()
elif opcion_buscar == "Buscar Animal":
    search_interface.buscar_animal()