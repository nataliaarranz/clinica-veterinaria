import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import seaborn as sns
from datetime import datetime
import calendar
import matplotlib.pyplot as plt

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

# Llamar al endpoint para obtener el beneficio neto
beneficio_neto_url = "http://fastapi:8000/beneficio_neto/"
r_beneficio = requests.get(beneficio_neto_url)

if r_beneficio.status_code == 200:
    beneficio_neto_value = r_beneficio.json().get("beneficio_neto", 0)
else:
    beneficio_neto_value = 0  # Si no se puede obtener el beneficio, establecer en 0


# Llamar al endpoint para obtener la facturación total
facturacion_total_url = "http://fastapi:8000/facturacion_total/"
r_facturacion = requests.get(facturacion_total_url)

if r_facturacion.status_code == 200:
    facturacion_total_value = r_facturacion.json().get("facturacion_total", 0)
else:
    facturacion_total_value = 0  # Si no se puede obtener la facturación, establecer en 0


# Cargar datos de citas
citas_url = "http://fastapi:8000/citas/"
r_citas = requests.get(citas_url)

if r_citas.status_code == 200:
    citas_data = r_citas.json()
    num_citas = len(citas_data)  # Número total de citas
else:
    num_citas = 0  # Si no se puede obtener, establecer en 0

# Calcular ingreso promedio por cita
ingreso_promedio_por_cita = facturacion_total_value / num_citas if num_citas > 0 else 0





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
    col1.subheader('Clientes')
    info_box(num_clientes)  # Muestra el número de clientes únicos
with col2:
    col2.subheader('Nº de tratamientos ')
    info_box(num_tratamientos)
with col3:
    col3.subheader('Animales')
    info_box(num_animales)

with col4:
    col4.subheader('Beneficio neto')
    info_box(f'{beneficio_neto_value:,.2f} €')  # Asegúrate de que el valor sea un número

with col5:
    col5.subheader('Facturación total')
    info_box(f'{facturacion_total_value:,.2f} €')

with col6:
    col6.subheader('Ingreso medio por cita')
    info_box(f'{ingreso_promedio_por_cita:,.2f} €')

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



# Crear el gráfico de relación entre facturación total y número de clientes
st.header("Relación entre Facturación Total y Número de Clientes")

# Convertir num_clientes a entero para el gráfico
num_clientes_int = int(num_clientes)

# Crear un DataFrame para el gráfico
df_relacion = pd.DataFrame({
    'Número de Clientes': [num_clientes_int],
    'Facturación Total': [facturacion_total_value]
})

# Usar Plotly para crear un gráfico de dispersión
fig = px.scatter(df_relacion, 
                 x='Número de Clientes', 
                 y='Facturación Total', 
                 title='Relación entre Facturación Total y Número de Clientes',
                 labels={'Número de Clientes': 'Número de Clientes', 'Facturación Total': 'Facturación Total (€)'},
                 size='Facturación Total',  # Tamaño de los puntos basado en la facturación
                 hover_name='Facturación Total')  # Mostrar la facturación al pasar el ratón

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)