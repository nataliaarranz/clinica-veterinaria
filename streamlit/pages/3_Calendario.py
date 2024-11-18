import streamlit as st
from streamlit_calendar import calendar
import requests

st.title("Calendario de citas veterinarias 📆")

backend = "http://fastapi:8000/citas"
dueños_backend = "http://fastapi:8000/dueños"
animales_backend = "http://fastapi:8000/animales"

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

# Función para obtener los dueños registrados
def get_dueños():
    try:
        response = requests.get(dueños_backend)
        if response.status_code == 200:
            return response.json()  # Suponemos que devuelve una lista de dueños
        else:
            return []
    except Exception as e:
        return []

# Función para obtener los animales registrados
def get_animales():
    try:
        response = requests.get(animales_backend)
        if response.status_code == 200:
            return response.json()  # Suponemos que devuelve una lista de dueños
        else:
            return []
    except Exception as e:
        return []
    
@st.dialog("Registrar nueva cita")
def popup():
    st.write('Fecha de la cita:')
    with st.form("form_nueva_cita"):
        animales = get_animales()
        animales_nombre = [animal["nombre_animal"] for animal in animales] if animales else ["No hay animales registrados."]
        nombre_animal = st.selectbox("Nombre animal: ", animales_nombre)
        
        dueños = get_dueños()
        dueños_nombre = [dueño["nombre_dueño"] for dueño in dueños] if dueños else ["No hay dueños registrados."]
        nombre_dueño = st.selectbox("Nombre dueño: ", dueños_nombre)
        
        tratamiento = st.text_input("Tipo de cita:")
        submitted = st.form_submit_button("Registrar cita")

    if submitted:
        if "time_inicial" in st.session_state:
            if nombre_animal == "No hay animales registrados." or nombre_dueño == "No hay dueños registrados.":
                st.error("Por favor, asegúrate de que hay animales y dueños registrados.")
            elif not tratamiento:
                st.error("El campo 'Tipo de cita' es obligatorio.")
            else:
                data = {
                    "nombre_animal": nombre_animal,
                    "nombre_dueño": nombre_dueño,
                    "tratamiento": tratamiento,
                    "fecha_inicio": st.session_state["time_inicial"],
                }
                response = send(data)
        
                if isinstance(response, dict) and "id" in response:
                    st.session_state["events"].append({
                        "id": response["id"],
                        "title": tratamiento,
                        "color": "#FF6C6C",
                        "start": st.session_state["time_inicial"],
                        "end": st.session_state["time_final"],
                    })
                    st.success("Registrado con éxito, puede cerrar!")
                else:
                    st.error("No se registró, status_code: {}".format(response))
        else:
            st.error("No se ha seleccionado una fecha.")

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "resource-daygrid",  # consultas
        "resource-timegrid",
        "resource-timeline",  # asignar y visualizar citas en diferentes lugares
        "list",
        "multimonth",
    ),
)

events = [
    {
        "title": "Consulta Perrito",
        "color": "#FF6C6C",
        "start": "2024-11-03",
        "end": "2024-11-05",
        "resourceId": "a",
    },
]

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
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key='timegrid',
)

if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

if state.get('select') is not None:
    st.session_state["time_inicial"] = state["select"]["start"]
    st.session_state["time_final"] = state["select"]["end"]
    popup()

#Modificar cita
if state.get('eventChange') is not None:
    data = state.get('eventChange').get('event')
    modified_data = {
        "id": data["id"],
        "start": data["start"],
        "end": data["end"]
    }
    envio = send(modified_data, method="PUT")
    if envio == '200':
        st.success('Cita modificada con éxito')
    else:
        st.error(f"No se pudo modificar la cita, status_code: {envio}")

#Cancelar cita
if state.get('eventClick') is not None:
    data = state['eventClick']['event']
    if st.button(f"Cancelar cita {data['title']}"):
        envio = send({"id": data["id"]}, method="DELETE")
        if envio == "200":
            st.success("Cita cancelada.")
            st.session_state["events"] = [event for event in st.session_state["events"] if event["id"] != data["id"]]
        else:
            st.error(f"No se pudo cancelar la cita, status_code: {envio}")
