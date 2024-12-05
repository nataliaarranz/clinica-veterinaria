import requests
import streamlit as st
import pandas as pd
import plotly.express as px

#SERVER
@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    return mijson

# Función para obtener el número de dueños
def obtener_numero_duenos():
    try:
        duenos = load_data("http://fastapi:8000/duenos")
        if duenos is not None:
            return len(duenos), duenos
        else:
            return 0, []
    except Exception as e:
        st.error(f"Error al obtener los dueños: {e}")
        return 0, []

#Función para obtener el número de animales
def obtener_numero_animales():
    try:
        animales = load_data("http://fastapi:8000/animales")
        if animales is not None:
            return len(animales), animales  #Devuelve número de animales y la lista de animales
        else:
            return 0, []  #Devuelve una lista vacía si no hay animales
    except Exception as e:
        st.error(f"Error al obtener los animales: {e}")
        return 0, []

#Función para obtener el número de tratamientos
def obtener_numero_tratamientos():
    try:
        tratamientos = load_data("http://fastapi:8000/tratamientos")
        if tratamientos is not None:
            return len(tratamientos), tratamientos  #Devuelve el número de tratamientos y la lista de tratamientos
        else:
            return 0, []  #Devuelve 0 y una lista vacía si no hay tratamientos
    except Exception as e:
        st.error(f"Error al obtener los tratamientos: {e}")
        return 0, []

#Función para obtener la facturación
def obtener_facturacion():
    try:
        facturas = load_data("http://fastapi:8000/facturas")
        if facturas is not None:
            # Calcular el total facturado sumando los importes con IVA
            total_facturado = sum(factura["importe_con_iva"] for factura in facturas if "importe_con_iva" in factura)
            return total_facturado, facturas  # Retorna el total facturado y la lista de facturas
        else:
            return 0.0, []  # Retorna 0 y una lista vacía si no hay facturas
    except Exception as e:
        st.error(f"Error al obtener la facturación: {e}")
        return 0.0, []

#Calcular KPIs
#Función para obtener el beneficio neto
def calcular_beneficio_neto():
    #Definir gastos fijos
    alquiler = 500
    sueldo_dueno = 400
    gastos_totales = alquiler + sueldo_dueno
    #Obtener el total facturado
    url = "http://fastapi:8000/facturas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            facturas = response.json()
            total_facturado = sum(factura["importe_con_iva"] for factura in facturas if "importe_con_iva" in factura)
            #Beneficio neto
            beneficio_neto = total_facturado - gastos_totales
            return beneficio_neto
        else:
            st.error(f"Error al obtener la facturación: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None
#Función para obtener el ingreso medio por cita
#def ingreso_medio():

# Obtener los datos y preparar las métricas
numero_duenos, duenos_data = obtener_numero_duenos()
numero_animales, animales_data = obtener_numero_animales()  # Obtener el número de animales
numero_tratamientos, tratamientos_data = obtener_numero_tratamientos()  # Obtener el número de tratamientos
facturacion_total, facturas_data = obtener_facturacion()

# KPIs
beneficio_neto = calcular_beneficio_neto()
ingreso_medio = ingreso_medio()


# Mostrar el dashboard con los nuevos KPIs
st.title("Dashboard de seguimiento de Consultas Veterinarias")

st.header("Información general")
# Definir los valores para mostrar en las cajas de información
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

# **Evolución del número de dueños**
# Convertimos los datos de dueños a un DataFrame
duenos_data = pd.DataFrame(duenos_data)
print("Datos de clientes:", duenos_data.head())  # Imprimir las primeras filas
print("Columnas en clientes_data:", duenos_data.columns)  # Imprimir los nombres de las columnas

# **Evolución de la facturación**
# Convertimos las fechas de las facturas a formato datetime
facturas_data = pd.DataFrame(facturas_data)

# Imprimir las columnas disponibles en facturas_data
print("Datos de facturas:", facturas_data.head())  # Imprimir las primeras filas
print("Columnas en facturas_data:", facturas_data.columns)  # Imprimir los nombres de las columnas

# Gráfico de la evolución del número de clientes
if not duenos_data.empty:
    duenos_data['fecha'] = pd.to_datetime(duenos_data['fecha'])  # Asegúrate de que la columna de fecha exista
    duenos_evolucion = duenos_data.groupby('fecha').size().reset_index(name='numero_duenos')
    fig_duenos = px.line(duenos_evolucion, x='fecha', y='numero_duenos', title='Evolución del Número de Dueños')
    st.plotly_chart(fig_duenos)

# Gráfico de la evolución de la facturación
if not facturas_data.empty:
    facturas_data['fecha'] = pd.to_datetime(facturas_data['fecha'])  # Asegúrate de que la columna de fecha exista
    facturacion_evolucion = facturas_data.groupby('fecha')['importe_con_iva'].sum().reset_index()
    fig_facturacion = px.line(facturacion_evolucion, x='fecha', y='importe_con_iva', title='Evolución de la Facturación')
    st.plotly_chart(fig_facturacion)