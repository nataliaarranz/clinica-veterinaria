import streamlit as st
import requests
from datetime import datetime

# URL del microservicio FastAPI
tratamientos_url = "http://fastapi:8000/tratamientos"
animales_url = "http://fastapi:8000/animales"
dueños_url = "http://fastapi:8000/dueños"
registro_consulta_url = "http://fastapi:8000/consultas"

# Título de la página
st.title("Factura de la consulta")

# Función para obtener los tratamientos disponibles desde el backend
def obtener_tratamientos():
    try:
        response = requests.get(tratamientos_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener tratamientos: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error al obtener tratamientos: {e}")
        return []

# Función para obtener los detalles del dueño desde el backend
def obtener_dueños():
    try:
        response = requests.get(dueños_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener dueños: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error al obtener dueños: {e}")
        return []

# Función para obtener los detalles del animal desde el backend
def obtener_animales():
    try:
        response = requests.get(animales_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener animales: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error al obtener animales: {e}")
        return []

# Función para registrar la consulta y generar la factura
def registrar_consulta_dueño_animal(nombre_dueño, nombre_animal, tratamientos_seleccionados):
    # Crear el cuerpo de la consulta
    consulta_data = {
        "nombre_dueño": nombre_dueño,
        "nombre_animal": nombre_animal,
        "tratamientos": tratamientos_seleccionados,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(registro_consulta_url, json=consulta_data)
        if response.status_code == 200:
            st.success("Consulta registrada con éxito.")
            st.json(response.json())  # Mostrar la respuesta de la consulta
        else:
            st.error(f"Error al registrar la consulta: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error al registrar la consulta: {e}")

# Función para calcular el total de la factura
def calcular_total(tratamientos):
    total = sum([tratamiento['precio'] for tratamiento in tratamientos])
    return total

# Función para mostrar la factura
def generar_factura(nombre_dueño, nombre_animal, tratamientos, total):
    st.subheader("Factura de Consulta Veterinaria")
    st.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Nombre del Dueño: {nombre_dueño}")
    st.write(f"Nombre del Animal: {nombre_animal}")
    
    st.write("Tratamientos realizados:")
    for tratamiento in tratamientos:
        st.write(f"- {tratamiento['nombre']} - {tratamiento['precio']}€")
    
    st.write(f"**Total a Pagar: {total}€**")

# Función principal para el registro de consultas
def registrar_consulta():
    st.title("Registro de Consulta Veterinaria")

    # Obtener los datos de dueños y animales
    dueños = obtener_dueños()
    animales = obtener_animales()
    tratamientos_disponibles = obtener_tratamientos()

    if not dueños or not animales or not tratamientos_disponibles:
        st.error("No se han podido obtener los datos necesarios.")
        return
    
    # Selección de dueño y animal
    nombre_dueño = st.selectbox("Selecciona el dueño:", [dueño["nombre_dueño"] for dueño in dueños])
    nombre_animal = st.selectbox("Selecciona el animal:", [animal["nombre_animal"] for animal in animales])

    # Mostrar los tratamientos disponibles
    tratamientos_seleccionados = []
    st.subheader("Tratamientos Realizados")
    for tratamiento in tratamientos_disponibles:
        if st.checkbox(f"{tratamiento['nombre']} ({tratamiento['precio']}€)", key=tratamiento['nombre']):
            tratamientos_seleccionados.append(tratamiento)
    
    # Botón para generar la factura
    if st.button("Generar Factura"):
        if nombre_dueño and nombre_animal and tratamientos_seleccionados:
            # Calcular el total
            total = calcular_total(tratamientos_seleccionados)
            
            # Registrar la consulta y generar la factura
            registrar_consulta_dueño_animal(nombre_dueño, nombre_animal, tratamientos_seleccionados)
            generar_factura(nombre_dueño, nombre_animal, tratamientos_seleccionados, total)
        else:
            st.error("Por favor, completa todos los campos y selecciona al menos un tratamiento.")

# Llamar a la función para registrar la consulta y generar la factura
registrar_consulta()
