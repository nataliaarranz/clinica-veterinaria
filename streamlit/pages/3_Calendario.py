import streamlit as st
from streamlit_calendar import calendar
import requests

st.title("Calendario de citas veterinarias 📆")

backend = "http://fastapi:8000/citas"

def send(data, method="POST"):
    try:
        if method == "POST":
            response = requests.post(backend, json=data)
        elif method == "PUT":
            response = requests.put(backend, json=data)
        elif method == "DELETE":
            response = requests.delete(backend, json=data)
        if response.status_code == 200:
            return '200'
        else:
            return str(response.status_code)
    except Exception as e:
        return str(e)

@st.dialog("Registrar nueva cita")
def popup():
    st.write('Fecha de la cita:')
    with st.form("form_nueva_cita"):
        nombre_animal = st.text_input("Nombre animal: ")
        nombre_dueño = st.text_input("Nombre dueño: ")
        tratamiento = st.text_input("Tipo de cita:")
        submitted = st.form_submit_button("Registrar cita")

    if submitted:
            if "time_inicial" in st.session_state:
                data = {
                    "nombre_animal": nombre_animal,
                    "nombre_dueño": nombre_dueño,
                    "tratamiento": tratamiento,
                    "fecha_inicio": st.session_state["time_inicial"],
                }
                envio = send(data)
                if envio == '200':
                    st.success("Registrado con éxito, puede cerrar!")
                else:
                    st.error("No se registró, status_code: {}".format(envio))
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