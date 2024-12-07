import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import seaborn as sns
from datetime import datetime
import calendar

@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    listado = mijson['contratos']
    df = pd.DataFrame.from_records(listado)
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].str.replace('€', '')
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].str.replace('.', '')
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].str.replace(',', '.')
    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].str.replace('€', '')
    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].str.replace('.', '')
    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].str.replace(',', '.')

    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].astype(float)
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].astype(float)

    return df

def load_duenos(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()  # Devuelve la lista de dueños

def load_animales(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()  # Devuelve la lista de animales

def info_box(texto, color=None):
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{texto}</p></div>', unsafe_allow_html=True)

url_animales = "http://fastapi:8000/animales/"

# Cargar datos de animales desde el backend
r = requests.get(url_animales)
if r.status_code == 200:
    animales_data = r.json()
    df_animales = pd.DataFrame(animales_data)
    if "fecha_alta" in df_animales.columns:
        df_animales["fecha_alta"] = pd.to_datetime(df_animales["fecha_alta"])  # Asegurar datetime
else:
    df_animales = pd.DataFrame()  # Si no hay datos, crea un DataFrame vacío

# Detectar mes actual y rango de fechas
today = datetime.now()
current_year = today.year
current_month = today.month
days_in_month = calendar.monthrange(current_year, current_month)[1]

# Crear un rango completo de fechas para el mes actual
start_date = datetime(current_year, current_month, 1)
end_date = datetime(current_year, current_month, days_in_month)
date_range = pd.date_range(start=start_date, end=end_date)
df_full_dates = pd.DataFrame(date_range, columns=["fecha"])  # DataFrame con todas las fechas del mes

# Procesar los datos reales
if not df_animales.empty:
    df_evolucion = df_animales.groupby(df_animales["fecha_alta"].dt.date).size().reset_index(name="total")
    df_evolucion.rename(columns={"fecha_alta": "fecha"}, inplace=True)  # Asegurarnos del nombre
    df_evolucion["fecha"] = pd.to_datetime(df_evolucion["fecha"])  # Convertir a datetime si es necesario
else:
    df_evolucion = pd.DataFrame(columns=["fecha", "total"])  # DataFrame vacío si no hay datos

# Combinar el rango completo con los datos reales
df_full_dates["fecha"] = pd.to_datetime(df_full_dates["fecha"])  # Asegurar datetime
df_evolucion_full = pd.merge(df_full_dates, df_evolucion, on="fecha", how="left")
df_evolucion_full["total"] = df_evolucion_full["total"].fillna(0)  # Rellenar días sin datos con 0

st.title("Dashboard")

# GRÁFICO EVOLUCION AQUI

# Cargar datos de contratos
df_merged = load_data('http://fastapi:8000/retrieve_data')

# Cargar datos de dueños
duenos_data = load_duenos('http://fastapi:8000/duenos/')
num_clientes = str(len(duenos_data)) if duenos_data else "0"  # Contar dueños

# Cargar datos de animales
animales_data = load_animales('http://fastapi:8000/animales/')
num_animales = str(len(animales_data)) if animales_data else "0"  # Contar animales

# Asignar directamente el número de tratamientos
num_tratamientos = "11"  # Número fijo de tratamientos

# Otras métricas
registros = str(df_merged.shape[0])
adjudicatarios = str(len(df_merged.adjuducatario.unique()))
centro = str(len(df_merged.centro_seccion.unique()))
tipologia = str(len(df_merged.tipo.unique()))
presupuesto_medio = str(round(df_merged.presupuesto_con_iva.mean(), 2))
adjudicado_medio = str(round(df_merged.importe_adj_con_iva.mean(), 2))

sns.set_palette("pastel")

st.header("Información general")

# Definir columnas
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)  # Definir columnas adicionales

with col1:
    col1.subheader('# Clientes')
    info_box(num_clientes)  # Muestra el número de clientes únicos
with col2:
    col2.subheader('# Nº de tratamientos ')
    info_box(num_tratamientos)
with col3:
    col3.subheader('# Animales')
    info_box(num_animales)

with col4:
    col4.subheader('# Beneficio neto ')
    info_box(tipologia)

with col5:
    col5.subheader('# Facturación total')
    info_box(presupuesto_medio)

with col6:
    col6.subheader('# Ingreso medio por cita')
    info_box(adjudicado_medio)

# Crear el gráfico EVOLUCIÓN
st.header(f"Evolución de Altas de Animales en {today.strftime('%B %Y')}")

if not df_evolucion_full.empty:
    fig = px.line(
        df_evolucion_full,
        x="fecha",
        y="total",
        labels={"fecha": "Fecha", "total": "Animales dados de alta"},
        title=f"Evolución del Número de Altas de Animales por Día en {today.strftime('%B %Y')}",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay datos disponibles para mostrar la evolución.")
