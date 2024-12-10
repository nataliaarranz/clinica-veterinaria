import requests
import streamlit as st
from streamlit_calendar import calendar
import time

# Clase para manejar la lógica de las citas
class CitaService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def send(self, data, method="POST", cita_id=None):
        try:
            url = self.backend_url if cita_id is None else f"{self.backend_url}/{cita_id}"
            if method == "POST":
                response = requests.post(url, json=data)
            elif method == "PUT":
                response = requests.put(url, json=data)
            elif method == "DELETE":
                response = requests.delete(url)
            if response.status_code == 200:
                return response.json() if method == "POST" else '200'
            else:
                return str(response.status_code)
        except Exception as e:
            return str(e)

# Clase para manejar la lógica de los dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def get_duenos(self):
        try:
            response = requests.get(self.backend_url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener dueños: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            st.error(f"Excepción al obtener dueños: {e}")
            return []

# Clase para manejar la lógica de los animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def get_animales(self):
        try:
            response = requests.get(self.backend_url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener animales: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            st.error(f"Excepción al obtener animales: {e}")
            return []

# Clase para manejar la interfaz de usuario
class CitaInterface:
    def __init__(self, cita_service, dueno_service, animal_service):
        self.cita_service = cita_service
        self.dueno_service = dueno_service
        self.animal_service = animal_service

    def registrar_cita(self):
        st.write('Fecha de la cita:')
         
        with st.container():
            # Usar columnas para centrar el contenido
            col1, col2, col3 = st.columns([1, 2, 1])  # Ajusta los pesos según sea necesario

            with col2:  # Columna central
                with st.form("form_nueva_cita"):
                    animales = self.animal_service.get_animales()
                    animales_nombre = [animal["nombre_animal"] for animal in animales] if animales else ["No hay animales registrados."]
                    nombre_animal = st.selectbox("Nombre animal: ", animales_nombre)
                    
                    duenos = self.dueno_service.get_duenos()
                    duenos_nombre = [dueno["nombre_dueno"] for dueno in duenos] if duenos else ["No hay dueños registrados."]
                    nombre_dueno = st.selectbox("Nombre dueño: ", duenos_nombre)
                    
                    # Menú desplegable para seleccionar el tratamiento
                    tratamientos = [
                        "Analisis",
                        "Vacunacion",
                        "Desparasitacion",
                        "Revision general",
                        "Revision cardiologia",
                        "Revision cutanea",
                        "Revision broncologia",
                        "Ecografias",
                        "Limpieza bucal",
                        "Extraccion de piezas dentales",
                        "Cirugia"
                    ]
                    tratamiento = st.selectbox("Tipo de cita:", tratamientos)
                    
                    submitted = st.form_submit_button("Registrar cita")

        if submitted:
            self._procesar_registro_cita(nombre_animal, nombre_dueno, tratamiento)
    
    def obtener_color_tratamiento(self, tratamiento):
        tratamientos_colores = {
            "Analisis": "#FF4B4B",
            "Vacunacion": "#FF4B4B",
            "Desparasitacion": "#FF4B4B",
            "Revision general": "#FF4B4B",
        }
        return tratamientos_colores.get(tratamiento, "#FF4B4B")  # Color por defecto si no se encuentra

    def _procesar_registro_cita(self, nombre_animal, nombre_dueno, tratamiento):
        if "time_inicial" in st.session_state:
            if nombre_animal == "No hay animales registrados." or nombre_dueno == "No hay dueños registrados.":
                st.error("Por favor, asegúrate de que hay animales y dueños registrados.")
            elif not tratamiento:
                st.error("El campo 'Tipo de cita' es obligatorio.")
            else:
                # Validar si el rango de fechas ya está ocupado
                conflict = any(
                    event["start"] <= st.session_state["time_inicial"] < event["end"] or
                    event["start"] < st.session_state["time_final"] <= event["end"]
                    for event in st.session_state["events"]
                )
                if conflict:
                    st.error("El rango de fechas ya está ocupado. Selecciona otra hora.")
                else:
                    data = {
                        "nombre_animal": nombre_animal,
                        "nombre_dueno": nombre_dueno,
                        "tratamiento": tratamiento,
                        "fecha_inicio": st.session_state["time_inicial"],
                        "fecha_fin": st.session_state["time_final"],
                        "backgroundColor": self.obtener_color_tratamiento(tratamiento),  # Color dinámico
                        "borderColor": self.obtener_color_tratamiento(tratamiento)      # Color dinámico
                    }
                    response = self.cita_service.send(data)
                    if isinstance(response, dict) and "id" in response:
                        st.session_state["events"].append({
                            "id": response["id"],
                            "title": tratamiento,
                            "start": st.session_state["time_inicial"],
                            "end": st.session_state["time_final"],
                            "backgroundColor": "#FF4B4B",  # Color de fondo del evento
                            "borderColor": "#FF4B4B"       # Color del borde del evento
                        })
                        st.success("Registrado con éxito, puede cerrar!")
                    else:
                        st.error("No se registró, status_code: {}".format(response))
        else:
            st.error("No se ha seleccionado una fecha.")

    def mostrar_calendario(self):
        mode = st.selectbox(
            "Calendar Mode: ",
            (
                "daygrid",
                "timegrid",
                "timeline",
                "resource-daygrid",
                "resource-timegrid",
                "resource-timeline",
                "list",
                "multimonth",
            ),
        )

        events = st.session_state.get("events", [])

        calendar_resources = [
            {"id": "a", "building": "Clinica 1", "title": "Consulta A"},
            {"id": "c", "building": "Clinica 1", "title": "Consulta B"},
        ]

        calendar_options = {
            "editable": True,
            "navLinks": True,
            "resources": calendar_resources,
            "selectable": True,
            "initialDate": "2024-11-01",
            "initialView": "resourceTimeGridDay",
            "resourceGroupField": "building",
            "slotMinTime": "8:00:00",
            "slotMaxTime": "18:00:00",
        }

        state = calendar(
            events=events,
            options=calendar_options,
            key='timegrid',
        )

        # Actualizar los eventos en el estado de Streamlit
        if state.get("eventsSet") is not None:
            st.session_state["events"] = state["eventsSet"]

        if state.get('select') is not None:
            st.session_state["time_inicial"] = state["select"]["start"]
            st.session_state["time_final"] = state["select"]["end"]
            self.registrar_cita()

        # Modificar cita
        if state.get('eventChange') is not None:
            data = state.get('eventChange').get('event')
            modified_data = {
                "id": data["id"],
                "start": data["start"],
                "end": data["end"]
            }
            envio = self.cita_service.send(modified_data, method="PUT")
            if envio == '200':
                st.success('Cita modificada con éxito')
            else:
                st.error(f"No se pudo modificar la cita, status_code: {envio}")

        # Cancelar cita
        if state.get('eventClick') is not None:
            data = state['eventClick']['event']
            if st.button(f"Cancelar cita {data['title']}"):
                envio = self.cita_service.send({"id": data["id"]}, method="DELETE")
                if envio == "200":
                    st.session_state["events"] = [
                        event for event in st.session_state["events"] if event["id"] != data["id"]
                    ]
                    st.success("Cita cancelada.")
                else:
                    st.error(f"No se pudo cancelar la cita, status_code: {envio}")

# Inicialización de servicios y la interfaz
citas_backend = "http://fastapi:8000/citas"
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

cita_service = CitaService(citas_backend)
dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
cita_interface = CitaInterface(cita_service, dueno_service, animal_service)

# Inicializar `st.session_state["events"]` como lista si no existe
if "events" not in st.session_state or not isinstance(st.session_state["events"], list):
    st.session_state["events"] = []

# Título de la aplicación
st.title("Calendario de citas veterinarias 📆")

# Mostrar el calendario y manejar la lógica de citas
cita_interface.mostrar_calendario()