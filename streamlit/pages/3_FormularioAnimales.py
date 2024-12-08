import streamlit as st
import requests
import re
from datetime import datetime

# URL del microservicio FastAPI
url = "http://fastapi:8000/alta_animal"

# Clase para representar a un animal
class Animal:
    def __init__(self, nombre, chip, especie, nacimiento, sexo, dni_dueno):
        self.nombre = nombre
        self.chip = chip
        self.especie = especie
        self.nacimiento = nacimiento
        self.sexo = sexo
        self.dni_dueno = dni_dueno

# Clase para validar los datos del animal
class ValidadorAnimal:
    @staticmethod
    def validar_chip(chip):
        return chip.isdigit() and len(chip) == 15

    @staticmethod
    def validar_animal(animal):
        if not all([animal.nombre, animal.chip, animal.especie, animal.nacimiento, animal.sexo]):
            return "Obligatorio rellenar todos los campos."
        if not ValidadorAnimal.validar_chip(animal.chip):
            return "El chip debe ser un número de 15 dígitos."
        if re.search(r'\d', animal.nombre):
            return "El nombre del animal no debe contener números."
        if re.search(r'\d', animal.especie):
            return "La especie del animal no debe contener números."
        return None

# Clase para manejar el servicio de envío de datos
class AnimalService:
    def __init__(self, url):
        self.url = url

    def guardar_datos(self, animal):
        payload = {
            "nombre_animal": animal.nombre,
            "chip_animal": animal.chip,
            "especie_animal": animal.especie,
            "nacimiento_animal": animal.nacimiento,
            "sexo": animal.sexo,
            "dni_dueno": animal.dni_dueno
        }
        try:
            response = requests.post(self.url, json=payload)
            return response
        except requests.exceptions.RequestException as e:
            return None, str(e)


# Clase para manejar la interfaz de usuario
class FormularioAnimales:
    def __init__(self):
        self.animal_service = AnimalService(url)

    def crear_formulario(self):
        st.title("Registro de Animales🐾")
        # Cargar datos de dueños
        duenos_data = ('http://fastapi:8000/duenos/')
        
        #Obtener la lista de dueños
        response = requests.get(duenos_data)
        if response.status_code == 200:
            duenos = response.json()
            #Crear un diccionario con todos los dueños
            duenos_dict = {dueno['dni_dueno']: dueno['nombre_dueno'] 
                       for dueno in duenos
                       if 'dni_dueno' in dueno and 'nombre_dueno' in dueno}
        
        else:
            st.error("Error al obtener los dueños.")
            duenos_dict={}

        
        with st.form("registro_animales"):
            st.subheader("Datos del animal")
            nombre_animal = st.text_input("Nombre del animal: ", max_chars=50)
            chip_animal = st.text_input("Número de chip de animal: ", max_chars=15).strip()
            especie_animal = st.text_input("Especie del animal: ")
            nacimiento_animal = st.date_input("Fecha de nacimiento del animal: ")
            sexo_animal = st.selectbox("Sexo del animal: ", ["Macho", "Hembra"])
            dueno_seleccionado = st.selectbox("Selecciona el dueño:", options = list(duenos_dict.values()))
            
        
            #Botón dar de alta
            submit_button = st.form_submit_button(label="Dar de alta animal")
            
            if submit_button:
                #Obtener el ID del dueño seleccionado
                dni_dueno = next((key for key, value in duenos_dict.items() if value == dueno_seleccionado), None)
                if dni_dueno is None:
                    st.error("No se ha seleccionado un dueño.")
                else:
                    #Procesar formulario
                    self.procesar_formulario(nombre_animal, chip_animal, especie_animal, nacimiento_animal.strftime("%Y-%m-%d"), sexo_animal, dni_dueno)

    def procesar_formulario(self, nombre, chip, especie, nacimiento, sexo, dni_dueno):
        animal = Animal(nombre, chip, especie, nacimiento, sexo, dni_dueno)
        error = ValidadorAnimal.validar_animal(animal)

        if error:
            st.error(error)
        else:
            response = self.animal_service.guardar_datos(animal)
            if response is not None and response.status_code == 200:
                st.success("Datos enviados correctamente")
                st.json(response.json())  # Mostrar la respuesta del microservicio
            else:
                error_message = "Error de conexión" if response is None else response.text
                st.error(f"Error al enviar los datos: {error_message}")

# Ejecutar el formulario
if __name__ == "__main__":
    formulario = FormularioAnimales()
    formulario.crear_formulario()