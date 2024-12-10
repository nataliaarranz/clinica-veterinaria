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
                    # Determinar la consulta (A o B) basado en la disponibilidad
                    consulta = "A"  # Por defecto asignar a consulta A
                    hora_inicio = st.session_state["time_inicial"]
                    hora_fin = st.session_state["time_final"]
                    
                    # Verificar si la consulta A está ocupada en ese horario específico
                    for event in st.session_state["events"]:
                        if (event["resourceId"] == "A" and 
                            ((event["start"] <= hora_inicio < event["end"]) or 
                             (event["start"] < hora_fin <= event["end"]))):
                            consulta = "B"
                            break

                    # Asignar color según la consulta
                    color = "#4CAF50" if consulta == "A" else "#2196F3"
                    
                    data = {
                        "nombre_animal": nombre_animal,
                        "nombre_dueno": nombre_dueno,
                        "tratamiento": tratamiento,
                        "fecha_inicio": hora_inicio,
                        "fecha_fin": hora_fin,
                        "consulta": consulta,
                        "backgroundColor": color,
                        "borderColor": color
                    }
                    
                    response = self.cita_service.send(data)
                    if isinstance(response, dict) and "id" in response:
                        nuevo_evento = {
                            "id": response["id"],
                            "title": tratamiento,
                            "start": hora_inicio,
                            "end": hora_fin,
                            "backgroundColor": color,
                            "borderColor": color,
                            "resourceId": consulta,
                            "className": f"consultation-{consulta.lower()}"
                        }
                        st.session_state["events"].append(nuevo_evento)
                        st.success("Cita registrada con éxito!")
                        
                        # Forzar recarga de la página para mostrar la nueva cita
                        st.rerun()
                    else:
                        st.error("Error al registrar la cita")
        else:
            st.error("No se ha seleccionado una fecha.")

    def mostrar_calendario(self):
        # Estilos CSS personalizados para el calendario
        st.markdown("""
            <style>
            .calendar-container {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                margin: 2rem 0;
            }
            .fc {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                font-family: 'Arial', sans-serif;
            }
            .fc-toolbar-title {
                color: #2B4162 !important;
                font-size: 1.5rem !important;
                font-weight: 600 !important;
                text-transform: capitalize !important;
            }
            .fc-button {
                background-color: #2B4162 !important;
                border-color: #2B4162 !important;
                box-shadow: none !important;
                padding: 0.5rem 1rem !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
            }
            .fc-button:hover {
                background-color: #1a2a3f !important;
                border-color: #1a2a3f !important;
                transform: translateY(-1px) !important;
            }
            .fc-event {
                border-radius: 4px !important;
                padding: 3px 5px !important;
                font-size: 0.85rem !important;
                border: none !important;
                transition: transform 0.2s ease !important;
            }
            .fc-event:hover {
                transform: scale(1.02) !important;
            }
            .fc-event-title {
                font-weight: 500 !important;
                padding: 2px 4px !important;
            }
            .fc-timegrid-slot, .fc-timegrid-axis {
                height: 3rem !important;
            }
            .fc-col-header-cell {
                background-color: #f8f9fa !important;
                padding: 1rem 0 !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                font-size: 0.9rem !important;
            }
            .fc-timegrid-axis {
                background-color: #f8f9fa !important;
                font-weight: 500 !important;
            }
            .fc-timegrid-slot-label {
                font-weight: 500 !important;
                color: #666 !important;
            }
            .fc-today {
                background-color: rgba(43, 65, 98, 0.05) !important;
            }
            .fc-event.consultation-a {
                background-color: #4CAF50 !important;
                border-left: 3px solid #388E3C !important;
            }
            .fc-event.consultation-b {
                background-color: #2196F3 !important;
                border-left: 3px solid #1976D2 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Título y descripción mejorados
        st.markdown("""
            <div style='background: linear-gradient(120deg, #2B4162 0%, #12100E 100%); 
                        padding: 2rem; 
                        border-radius: 10px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                <h1 style='color: white; 
                           font-size: 2.2rem; 
                           margin-bottom: 0.5rem; 
                           text-align: center;
                           font-weight: 600;'>
                    Sistema de Gestión de Citas
                </h1>

        """, unsafe_allow_html=True)

        # Configuración del calendario
        calendar_options = {
            "editable": True,
            "navLinks": True,
            "selectable": True,
            "selectMirror": True,
            "initialView": "resourceTimeGridDay",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "18:00:00",
            "allDaySlot": False,
            "slotDuration": "00:30:00",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "resourceTimeGridDay,resourceTimeGridWeek,dayGridMonth"
            },
            "resources": [
                {"id": "A", "title": "Consulta A", "eventColor": "#4CAF50"},
                {"id": "B", "title": "Consulta B", "eventColor": "#2196F3"},
            ],
            "businessHours": {
                "daysOfWeek": [1, 2, 3, 4, 5],
                "startTime": "08:00",
                "endTime": "18:00",
            },
            "slotLabelFormat": {
                "hour": "2-digit",
                "minute": "2-digit",
                "hour12": False
            },
            "eventTimeFormat": {
                "hour": "2-digit",
                "minute": "2-digit",
                "hour12": False
            },
            "nowIndicator": True,
            "scrollTime": "08:00:00",
            "height": "auto",
            "expandRows": True
        }

        # Contenedor del calendario con estilo
        with st.container():
            st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
            state = calendar(
                events=st.session_state.get("events", []),
                options=calendar_options,
                key="calendar"
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # Procesar eventos del calendario
        if state.get("select"):
            st.session_state["time_inicial"] = state["select"]["start"]
            st.session_state["time_final"] = state["select"]["end"]
            self.registrar_cita()

        # Mostrar detalles de la cita al hacer clic
        if state.get("eventClick"):
            event_data = state["eventClick"]["event"]
            with st.container():
                st.markdown(f"""
                    <div style='background: white; 
                               padding: 1.5rem; 
                               border-radius: 8px; 
                               box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
                               margin: 1rem 0;
                               border-left: 4px solid #2B4162;'>
                        <h3 style='color: #2B4162; 
                                 margin-bottom: 1rem;
                                 font-size: 1.3rem;'>
                            Detalles de la Cita
                        </h3>
                        <p style='margin-bottom: 0.5rem;'>
                            <strong>Tratamiento:</strong> {event_data['title']}
                        </p>
                        <p style='margin-bottom: 0.5rem;'>
                            <strong>Inicio:</strong> {event_data['start']}
                        </p>
                        <p style='margin-bottom: 1rem;'>
                            <strong>Fin:</strong> {event_data['end']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de cancelar con estilo
                col1, col2, col3 = st.columns([1,1,1])
                with col2:
                    if st.button("🗑️ Cancelar Cita", 
                                key="cancel_button",
                                help="Eliminar esta cita del calendario"):
                        self.cancelar_cita(event_data["id"])

    def cargar_citas_existentes(self):
        try:
            response = requests.get(self.cita_service.backend_url)
            if response.status_code == 200:
                citas = response.json()
                st.session_state["events"] = [{
                    "id": cita["id"],
                    "title": cita["tratamiento"],
                    "start": cita["fecha_inicio"],
                    "end": cita["fecha_fin"],
                    "backgroundColor": "#4CAF50" if cita["consulta"] == "A" else "#2196F3",
                    "borderColor": "#4CAF50" if cita["consulta"] == "A" else "#2196F3",
                    "resourceId": cita["consulta"],
                    "className": f"consultation-{cita['consulta'].lower()}"
                } for cita in citas]
        except Exception as e:
            st.error(f"Error al cargar citas: {e}")

# Inicialización de servicios y la interfaz
citas_backend = "http://fastapi:8000/citas"
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

cita_service = CitaService(citas_backend)
dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
cita_interface = CitaInterface(cita_service, dueno_service, animal_service)

# Inicializar st.session_state["events"] como lista si no existe
if "events" not in st.session_state or not isinstance(st.session_state["events"], list):
    st.session_state["events"] = []

# Cargar las citas existentes al inicio
def cargar_citas_existentes():
    try:
        response = requests.get(citas_backend)
        if response.status_code == 200:
            citas = response.json()
            st.session_state["events"] = [{
                "id": cita["id"],
                "title": cita["tratamiento"],
                "start": cita["fecha_inicio"],
                "end": cita["fecha_fin"],
                "backgroundColor": "#4CAF50" if cita["consulta"] == "A" else "#2196F3",
                "borderColor": "#4CAF50" if cita["consulta"] == "A" else "#2196F3",
                "resourceId": cita["consulta"],
                "className": f"consultation-{cita['consulta'].lower()}"
            } for cita in citas]
    except Exception as e:
        st.error(f"Error al cargar citas: {e}")

# Cargar citas al inicio
cargar_citas_existentes()

# Mostrar el calendario y manejar la lógica de citas
cita_interface.mostrar_calendario()