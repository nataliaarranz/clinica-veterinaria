import requests
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    return mijson

# Funciones para obtener los datos
def obtener_numero_clientes():
    dueños = load_data("http://fastapi:8000/duenos")
    print("Dueños obtenidos:", dueños)  # Imprimir los datos obtenidos
    if dueños is not None:
        return len(dueños), dueños
    else:
        return 0, []

def obtener_numero_animales():
    animales = load_data("http://fastapi:8000/animales")  # Asegúrate de que esta URL sea correcta
    print("Animales obtenidos:", animales)  # Imprimir los datos obtenidos
    if animales is not None:
        return len(animales), animales
    else:
        return 0, []

def obtener_numero_tratamientos():
    tratamientos = load_data("http://fastapi:8000/tratamientos")  # Asegúrate de que esta URL sea correcta
    print("Tratamientos obtenidos:", tratamientos)  # Imprimir los datos obtenidos
    if tratamientos is not None:
        return len(tratamientos), tratamientos
    else:
        return 0, []

def obtener_facturacion():
    facturas = load_data("http://fastapi:8000/facturas")
    if facturas is None or not isinstance(facturas, list):
        return 0, []
    total_facturado = sum([factura["importe_con_iva"] for factura in facturas if "importe_con_iva" in factura])
    return total_facturado, facturas

def calcular_kpis():
    facturas = load_data("http://fastapi:8000/facturas")
    if facturas is None or not isinstance(facturas, list):
        return 0, 0
    
    total_facturado = sum([factura["importe_con_iva"] for factura in facturas if "importe_con_iva" in factura])
    
    # Beneficio neto (esto es un ejemplo, deberías ajustarlo según los datos de costos)
    costos_totales = sum([factura["costo"] for factura in facturas if "costo" in factura])
    beneficio_neto = total_facturado - costos_totales
    
    # Ingreso medio por cita
    numero_de_citas = len(facturas)
    ingreso_medio_por_cita = total_facturado / numero_de_citas if numero_de_citas > 0 else 0
    
    return beneficio_neto, ingreso_medio_por_cita

# Obtener los datos y preparar las métricas
numero_clientes, clientes_data = obtener_numero_clientes()
numero_animales, animales_data = obtener_numero_animales()  # Obtener el número de animales
numero_tratamientos, tratamientos_data = obtener_numero_tratamientos()  # Obtener el número de tratamientos
facturacion_total, facturas_data = obtener_facturacion()

# KPIs
beneficio_neto, ingreso_medio_por_cita = calcular_kpis()

# Mostrar el dashboard con los nuevos KPIs
st.title("Dashboard de seguimiento de Consultas Veterinarias")

st.header("Información general")

# Definir los valores para mostrar en las cajas de información
col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)
with col1:
    col1.subheader('# Clientes')
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{numero_clientes}</p></div>', unsafe_allow_html=True)
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
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{ingreso_medio_por_cita:.2f}</p></div>', unsafe_allow_html=True)

# **Evolución del número de clientes**
# Convertimos los datos de clientes a un DataFrame
clientes_data = pd.DataFrame(clientes_data)
print("Datos de clientes:", clientes_data.head())  # Imprimir las primeras filas
print("Columnas en clientes_data:", clientes_data.columns)  # Imprimir los nombres de las columnas

# **Evolución de la facturación**
# Convertimos las fechas de las facturas a formato datetime
facturas_data = pd.DataFrame(facturas_data)

# Imprimir las columnas disponibles en facturas_data
print("Datos de facturas:", facturas_data.head())  # Imprimir las primeras filas
print("Columnas en facturas_data:", facturas_data.columns)  # Imprimir los nombres de las columnas

# Gráfico de la evolución del número de clientes
if not clientes_data.empty:
    clientes_data['fecha'] = pd.to_datetime(clientes_data['fecha'])  # Asegúrate de que la columna de fecha exista
    clientes_evolucion = clientes_data.groupby('fecha').size().reset_index(name='numero_clientes')
    fig_clientes = px.line(clientes_evolucion, x='fecha', y='numero_clientes', title='Evolución del Número de Clientes')
    st.plotly_chart(fig_clientes)

# Gráfico de la evolución de la facturación
if not facturas_data.empty:
    facturas_data['fecha'] = pd.to_datetime(facturas_data['fecha'])  # Asegúrate de que la columna de fecha exista
    facturacion_evolucion = facturas_data.groupby('fecha')['importe_con_iva'].sum().reset_index()
    fig_facturacion = px.line(facturacion_evolucion, x='fecha', y='importe_con_iva', title='Evolución de la Facturación')
    st.plotly_chart(fig_facturacion)