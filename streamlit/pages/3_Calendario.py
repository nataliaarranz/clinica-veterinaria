import streamlit as st
from streamlit_calendar import calendar
import requests

st.title("Calendario de citas veterinarias 📆")

backend = "http://fastapi:8000/citas"
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

# Inicializar `st.session_state["events"]` como lista si no existe
if "events" not in st.session_state or not isinstance(st.session_state["events"], list):
    st.session_state["events"] = []

def send(data, method="POST", cita_id=None):
    try:
        url = backend if cita_id is None else f"{backend}/{cita_id}"
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

# Funcion para obtener los duenos registrados
def get_duenos():
    try:
        response = requests.get(duenos_backend)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener dueños: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Excepcion al obtener dueños: {e}")
        return []

# Funcion para obtener los animales registrados
def get_animales():
    try:
        response = requests.get(animales_backend)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener animales: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Excepcion al obtener animales: {e}")
        return []

@st.dialog("Registrar nueva cita")
def popup():
    st.write('Fecha de la cita:')
    with st.form("form_nueva_cita"):
        animales = get_animales()
        animales_nombre = [animal["nombre_animal"] for animal in animales] if animales else ["No hay animales registrados."]
        nombre_animal = st.selectbox("Nombre animal: ", animales_nombre)
        
        duenos = get_duenos()
        duenos_nombre = [dueno["nombre_dueno"] for dueno in duenos] if duenos else ["No hay dueños registrados."]
        nombre_dueno = st.selectbox("Nombre dueño: ", duenos_nombre)
        
        # Menu desplegable para seleccionar el tratamiento
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
                        "fecha_fin": st.session_state["time_final"]
                    }
                    response = send(data)
                    if isinstance(response, dict) and "id" in response:
                        st.session_state["events"].append({
                            "id": response["id"],
                            "title": tratamiento,
                            "color": "#FF6C6C",  # Color de fondo del evento
                            "start": st.session_state["time_inicial"],
                            "end": st.session_state["time_final"],
                        })
                        st.success("Registrado con exito, puede cerrar!")
                    else:
                        st.error("No se registro, status_code: {}".format(response))
        else:
            st.error("No se ha seleccionado una fecha.")

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

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

if state.get('select') is not None:
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    popup()

# Modificar cita
if state.get('eventChange') is not None:
    data = state.get('eventChange').get('event')
    modified_data = {
        "id": data["id"],
        "start": data["start"],
        "end": data["end"]
    }
    envio = send(modified_data, method="PUT")
    if envio == '200':
        st.success('Cita modificada con exito')
    else:
        st.error(f"No se pudo modificar la cita, status_code: {envio}")

# Cancelar cita
if state.get('eventClick') is not None:
    data = state['eventClick']['event']
    if st.button(f"Cancelar cita {data['title']}"):
        envio = send({"id": data["id"]}, method="DELETE")
        if envio == "200":
            st.session_state["events"] = [
                event for event in st.session_state["events"] if event["id"] != data["id"]
            ]
            st.success("Cita cancelada.")
        else:
            st.error(f"No se pudo cancelar la cita, status_code: {envio}")