import requests
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la URL base del servidor FastAPI
BASE_URL = "http://localhost:8000"

# Cargar datos desde el servidor FastAPI
@st.cache_data(ttl=600)
def load_data(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            st.error(f"Error al cargar datos: {r.status_code} - {r.text}")
            return None
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None

# Función para obtener el número de dueños
def obtener_numero_duenos():
    try:
        duenos = load_data(f"{BASE_URL}/duenos")
        if duenos is not None:
            return len(duenos), duenos
        else:
            return 0, []
    except Exception as e:
        st.error(f"Error al obtener los dueños: {e}")
        return 0, []

# Función para obtener el número de animales
def obtener_numero_animales():
    try:
        animales = load_data(f"{BASE_URL}/animales")
        if animales is not None:
            return len(animales), animales
        else:
            return 0, []
    except Exception as e:
        st.error(f"Error al obtener los animales: {e}")
        return 0, []

# Función para obtener el número de tratamientos
def obtener_numero_tratamientos():
    try:
        tratamientos = load_data(f"{BASE_URL}/tratamientos")
        if tratamientos is not None:
            return len(tratamientos), tratamientos
        else:
            return 0, []
    except Exception as e:
        st.error(f"Error al obtener los tratamientos: {e}")
        return 0, []

# Función para obtener la facturación total
def obtener_facturacion():
    try:
        facturas = load_data(f"{BASE_URL}/facturas")
        if facturas is not None:
            total_facturado = sum(factura["importe_con_iva"] for factura in facturas if "importe_con_iva" in factura)
            return total_facturado, facturas
        else:
            return 0.0, []
    except Exception as e:
        st.error(f"Error al obtener la facturación: {e}")
        return 0.0, []

# Función para calcular el beneficio neto
def calcular_beneficio_neto():
    alquiler = 500
    sueldo_dueno = 400
    gastos_totales = alquiler + sueldo_dueno
    total_facturado, _ = obtener_facturacion()
    return total_facturado - gastos_totales

# Función para calcular el ingreso medio por cita
def ingreso_medio_por_cita():
    try:
        citas = load_data(f"{BASE_URL}/citas")
        if citas:
            total_facturado, _ = obtener_facturacion()
            ingreso_medio = total_facturado / len(citas) if citas else 0.0
            return ingreso_medio
        return 0.0
    except Exception as e:
        st.error(f"Error al calcular el ingreso medio: {e}")
        return 0.0

# Obtener datos y métricas
numero_duenos, duenos_data = obtener_numero_duenos()
numero_animales, animales_data = obtener_numero_animales()
numero_tratamientos, tratamientos_data = obtener_numero_tratamientos()
facturacion_total, facturas_data = obtener_facturacion()
beneficio_neto = calcular_beneficio_neto()
ingreso_medio = ingreso_medio_por_cita()

# Mostrar el dashboard
st.title("Dashboard de seguimiento de Consultas Veterinarias")

st.header("Información general")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    col1.subheader('# Clientes registrados')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{numero_duenos}</p></div>', unsafe_allow_html=True)
with col2:
    col2.subheader('# Animales registrados')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{numero_animales}</p></div>', unsafe_allow_html=True)
with col3:
    col3.subheader('# Facturación total (€)')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{facturacion_total:.2f}</p></div>', unsafe_allow_html=True)
with col4:
    col4.subheader('# Número de tratamientos')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{numero_tratamientos}</p></div>', unsafe_allow_html=True)
with col5:
    col5.subheader('# Beneficio neto (€)')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{beneficio_neto:.2f}</p></div>', unsafe_allow_html=True)
with col6:
    col6.subheader('# Ingreso medio por cita (€)')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{ingreso_medio:.2f}</p></div>', unsafe_allow_html=True)

# Gráficos de evolución
if duenos_data:
    duenos_df = pd.DataFrame(duenos_data)
    if 'fecha' in duenos_df.columns:
        duenos_df['fecha'] = pd.to_datetime(duenos_df['fecha'])
        duenos_evolucion = duenos_df.groupby('fecha').size().reset_index(name='numero_duenos')
        fig_duenos = px.line(duenos_evolucion, x='fecha', y='numero_duenos', title='Evolución del Número de Dueños')
        st.plotly_chart(fig_duenos)

if facturas_data:
    facturas_df = pd.DataFrame(facturas_data)
    if 'fecha' in facturas_df.columns and 'importe_con_iva' in facturas_df.columns:
        facturas_df['fecha'] = pd.to_datetime(facturas_df['fecha'])
        facturacion_evolucion = facturas_df.groupby('fecha')['importe_con_iva'].sum().reset_index()
        fig_facturacion = px.line(facturacion_evolucion, x='fecha', y='importe_con_iva', title='Evolución de la Facturación')
        st.plotly_chart(fig_facturacion)