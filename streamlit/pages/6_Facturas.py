import streamlit as st
import requests
from datetime import datetime

# URL del microservicio FastAPI
animales_backend = "http://fastapi:8000/animales"
dueños_backend = "http://fastapi:8000/dueños"

# Título de la página
st.title("Factura de la consulta")

# Función para obtener los detalles del dueño desde el backend
def obtener_dueños():
    try:
        response = requests.get(dueños_backend)
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
        response = requests.get(animales_backend)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener animales: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error al obtener animales: {e}")
        return []

# Función para mostrar la factura
def generar_factura(nombre_dueño, nombre_animal, tratamiento, precio_sin_iva, precio_con_iva):
    st.subheader("Factura de Consulta Veterinaria")
    st.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Nombre del Dueño: {nombre_dueño}")
    st.write(f"Nombre del Animal: {nombre_animal}")
    
    st.write("Tratamiento realizado:")
    st.write(f"- {tratamiento} - {precio_sin_iva:.2f}€ (sin IVA)")
    st.write(f"- {tratamiento} - {precio_con_iva:.2f}€ (con IVA)")
    
    st.write(f"**Total a Pagar: {precio_con_iva:.2f}€**")
    
    # Información del centro veterinario
    st.write(f"**Información del Centro**")
    st.write("Clinica Veterinaria Cuatro Patas")
    st.write("Ubicación: Paseo de la Castellana, 14")
    st.write("Teléfono: 912457890")

# Función principal para el registro de consultas
def registrar_consulta():
    st.title("Registro de Consulta Veterinaria")

    # Obtener los datos de dueños y animales
    dueños = obtener_dueños()
    animales = obtener_animales()

    if not dueños or not animales:
        st.error("No se han podido obtener los datos necesarios.")
        return

    # Selección de dueño y animal
    nombre_dueño = st.selectbox("Selecciona el dueño:", [dueño["nombre_dueño"] for dueño in dueños])
    nombre_animal = st.selectbox("Selecciona el animal:", [animal["nombre_animal"] for animal in animales])

    # Definición de tratamientos y precios
    tratamientos = {
        "Análisis": 15,
        "Vacunación": 15,
        "Desparasitación": 25,
        "Revisión general": 30,
        "Revisión cardiología": 55,
        "Revisión cutánea": 45,
        "Revisión broncología": 35,
        "Ecografías": 50,
        "Limpieza bucal": 50,
        "Extracción de piezas dentales": 70,
        "Cirugía": 250
    }

    # Selección del tratamiento
    tratamiento_seleccionado = st.selectbox("Selecciona el tipo de tratamiento:", list(tratamientos.keys()))
    precio_sin_iva = tratamientos[tratamiento_seleccionado]

    # Calcular precio con IVA (suponiendo un IVA del 21%)
    iva = 0.21
    precio_con_iva = precio_sin_iva * (1 + iva)


    # Botón para generar la factura
    if st.button("Generar Factura"):
        if nombre_dueño and nombre_animal and tratamiento_seleccionado:
            generar_factura(nombre_dueño, nombre_animal, tratamiento_seleccionado, precio_sin_iva, precio_con_iva)
        else:
            st.error("Por favor, completa todos los campos.")

# Llamar a la función para registrar la consulta y generar la factura
registrar_consulta()