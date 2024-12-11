import requests
import streamlit as st
from streamlit_calendar import calendar
import time
from datetime import datetime

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

    def mostrar_calendario(self):
        # Estilos del calendario
        st.markdown("""
            <style>
            .calendar-container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .fc-event {
                padding: 5px;
                border-radius: 3px;
                margin: 2px 0;
            }
            .consultation-a { 
                background-color: #FF4444 !important; 
                border-color: #FF4444 !important;
            }
            .consultation-b { 
                background-color: #FFA500 !important; 
                border-color: #FFA500 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Configuración del calendario
        calendar_options = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "resourceTimeGridDay,resourceTimeGridWeek"
            },
            "initialView": "resourceTimeGridDay",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "18:00:00",
            "slotDuration": "00:30:00",
            "selectable": True,
            "selectMirror": True,
            "editable": False,
            "height": "650px",
            "businessHours": {
                "daysOfWeek": [1, 2, 3, 4, 5],
                "startTime": "08:00",
                "endTime": "18:00"
            },
            "selectConstraint": "businessHours",
            "selectOverlap": False,
            "resources": [
                {"id": "A", "title": "Consulta A"},
                {"id": "B", "title": "Consulta B"}
            ]
        }

        # Renderizar calendario
        with st.container():
            st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
            state = calendar(events=st.session_state.get("events", []), options=calendar_options)
            st.markdown('</div>', unsafe_allow_html=True)

            # Procesar selección de horario
            if state.get("select"):
                st.session_state["time_inicial"] = state["select"].get("start")
                st.session_state["time_final"] = state["select"].get("end")
                self.registrar_cita()

            # Mostrar detalles de cita al hacer clic
            if state.get("eventClick"):
                self.mostrar_detalles_cita(state["eventClick"]["event"])

    def registrar_cita(self):
        with st.form("form_cita", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nombre_animal = st.selectbox("Animal", self.get_animales_nombres())
            with col2:
                nombre_dueno = st.selectbox("Dueño", self.get_duenos_nombres())
            
            tratamiento = st.selectbox("Tipo de cita", self.get_tratamientos())
            submitted = st.form_submit_button("Registrar cita")

            if submitted:
                self._procesar_registro_cita(nombre_animal, nombre_dueno, tratamiento)

    def _procesar_registro_cita(self, nombre_animal, nombre_dueno, tratamiento):
        if not all([nombre_animal, nombre_dueno, tratamiento]):
            st.error("Todos los campos son obligatorios")
            return

        hora_inicio = st.session_state.get("time_inicial")
        hora_fin = st.session_state.get("time_final")
        if not hora_inicio or not hora_fin:
            st.error("Selecciona un horario en el calendario")
            return

        # Verificar disponibilidad
        consulta = self.verificar_disponibilidad(hora_inicio, hora_fin)
        if not consulta:
            return

        # Registrar cita
        self.crear_cita(nombre_animal, nombre_dueno, tratamiento, hora_inicio, hora_fin, consulta)

    def get_animales_nombres(self):
        animales = self.animal_service.get_animales()
        if not animales:
            return ["No hay animales registrados."]
        return [animal["nombre_animal"] for animal in animales]

    def get_duenos_nombres(self):
        duenos = self.dueno_service.get_duenos()
        if not duenos:
            return ["No hay dueños registrados."]
        return [dueno["nombre_dueno"] for dueno in duenos]

    def get_tratamientos(self):
        return [
            "Consulta general",
            "Vacunación",
            "Cirugía",
            "Control",
            "Urgencia"
        ]

    def verificar_disponibilidad(self, hora_inicio, hora_fin):
        consulta_a_ocupada = False
        consulta_b_ocupada = False
        
        for event in st.session_state["events"]:
            tiempo_conflicto = (
                event["start"] <= hora_inicio < event["end"] or
                event["start"] < hora_fin <= event["end"]
            )
            if tiempo_conflicto:
                if event["resourceId"] == "A":
                    consulta_a_ocupada = True
                elif event["resourceId"] == "B":
                    consulta_b_ocupada = True

        if consulta_a_ocupada and consulta_b_ocupada:
            st.error("❌ Ambas consultas están ocupadas en este horario")
            return None
        
        return "B" if consulta_a_ocupada else "A"

    def crear_cita(self, nombre_animal, nombre_dueno, tratamiento, hora_inicio, hora_fin, consulta):
        data = {
            "nombre_animal": nombre_animal,
            "nombre_dueno": nombre_dueno,
            "tratamiento": tratamiento,
            "fecha_inicio": hora_inicio,
            "fecha_fin": hora_fin,
            "consulta": consulta
        }
        
        response = self.cita_service.send(data)
        if isinstance(response, dict) and "id" in response:
            color = "#FFA500" if consulta == "B" else "#FF4444"  # Naranja para B, Rojo para A
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
            st.success("✅ Cita registrada con éxito!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Error al registrar la cita")

    def mostrar_detalles_cita(self, event_data):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>
                    📅 Detalles de la Cita
                </h3>
                <p style='margin-bottom: 0.5rem;'>
                    <strong>Tratamiento:</strong> {event_data.get('title', 'N/A')}
                </p>
                <p style='margin-bottom: 0.5rem;'>
                    <strong>Consulta:</strong> {event_data.get('resourceId', 'N/A')}
                </p>
                <p style='margin-bottom: 0.5rem;'>
                    <strong>Inicio:</strong> {event_data.get('start', 'N/A')}
                </p>
                <p style='margin-bottom: 1rem;'>
                    <strong>Fin:</strong> {event_data.get('end', 'N/A')}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Botones de acción
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Editar Cita", 
                        key=f"edit_button_{event_data.get('id')}",
                        type="secondary",
                        use_container_width=True):
                self.mostrar_formulario_edicion(event_data)
        
        with col2:
            if st.button("❌ Cancelar Cita", 
                        key=f"cancel_button_{event_data.get('id')}",
                        type="primary",
                        use_container_width=True):
                self.cancelar_cita(int(event_data.get('id')))

    def mostrar_formulario_edicion(self, event_data):
        with st.form(key=f"edit_form_{event_data.get('id')}"):
            st.markdown("### ✏️ Editar Cita")
            
            col1, col2 = st.columns(2)
            with col1:
                animales = self.get_animales_nombres()
                nombre_animal = st.selectbox(
                    "Animal", 
                    animales,
                    index=0  # Valor por defecto: primer animal
                )
            with col2:
                duenos = self.get_duenos_nombres()
                nombre_dueno = st.selectbox(
                    "Dueño", 
                    duenos,
                    index=0  # Valor por defecto: primer dueño
                )
            
            tratamientos = self.get_tratamientos()
            tratamiento = st.selectbox(
                "Tipo de cita", 
                tratamientos,
                index=tratamientos.index(event_data.get('title')) if event_data.get('title') in tratamientos else 0
            )
            
            if st.form_submit_button("Actualizar Cita"):
                self.actualizar_cita(
                    event_data.get('id'),
                    nombre_animal,
                    nombre_dueno,
                    tratamiento,
                    event_data.get('start'),
                    event_data.get('end'),
                    event_data.get('resourceId')
                )

    def actualizar_cita(self, cita_id, nombre_animal, nombre_dueno, tratamiento, hora_inicio, hora_fin, consulta):
        data = {
            "id": cita_id,
            "nombre_animal": nombre_animal,
            "nombre_dueno": nombre_dueno,
            "tratamiento": tratamiento,
            "fecha_inicio": hora_inicio,
            "fecha_fin": hora_fin,
            "consulta": consulta
        }
        
        response = self.cita_service.send(data, method="PUT", cita_id=cita_id)
        if response == '200':
            # Actualizar el evento en el estado local
            for event in st.session_state["events"]:
                if event["id"] == cita_id:
                    color = "#FFA500" if consulta == "B" else "#FF4444"
                    event.update({
                        "title": tratamiento,
                        "nombre_animal": nombre_animal,
                        "nombre_dueno": nombre_dueno,
                        "start": hora_inicio,
                        "end": hora_fin,
                        "backgroundColor": color,
                        "borderColor": color,
                        "resourceId": consulta,
                        "className": f"consultation-{consulta.lower()}"
                    })
            st.success("✅ Cita actualizada con éxito!")
            time.sleep(1)
            st.rerun()
        else:
            st.error(f"❌ Error al actualizar la cita: {response}")

    def cancelar_cita(self, cita_id):
        try:
            response = self.cita_service.send(None, method="DELETE", cita_id=cita_id)
            if response == '200':
                # Eliminar el evento del estado local
                st.session_state["events"] = [
                    event for event in st.session_state["events"] 
                    if event["id"] != cita_id
                ]
                st.success("✅ Cita cancelada con éxito!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Error al cancelar la cita: {response}")
        except Exception as e:
            st.error(f"❌ Error al cancelar la cita: {str(e)}")

    def _mostrar_resultado_dueno(self, resultado):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>Información del Dueño</h3>
                <p><strong>Nombre:</strong> {resultado.get('nombre_dueno', 'N/A')}</p>
                <p><strong>DNI:</strong> {resultado.get('dni_dueno', 'N/A')}</p>
                <p><strong>Teléfono:</strong> {resultado.get('telefono_dueno', 'N/A')}</p>
                <p><strong>Email:</strong> {resultado.get('email_dueno', 'N/A')}</p>
                <p><strong>Dirección:</strong> {resultado.get('direccion_dueno', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    def _mostrar_resultado_animal(self, resultado):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>Información del Animal</h3>
                <p><strong>Nombre:</strong> {resultado.get('nombre_animal', 'N/A')}</p>
                <p><strong>Chip:</strong> {resultado.get('chip_animal', 'N/A')}</p>
                <p><strong>Especie:</strong> {resultado.get('especie_animal', 'N/A')}</p>
                <p><strong>Sexo:</strong> {resultado.get('sexo_animal', 'N/A')}</p>
                <p><strong>Fecha de Nacimiento:</strong> {resultado.get('nacimiento_animal', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

# Inicialización
if "events" not in st.session_state:
    st.session_state["events"] = []

citas_backend = "http://fastapi:8000/citas"
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

cita_interface = CitaInterface(
    CitaService(citas_backend),
    DuenoService(duenos_backend),
    AnimalService(animales_backend)
)

cita_interface.mostrar_calendario()