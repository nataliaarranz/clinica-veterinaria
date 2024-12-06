import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import seaborn as sns

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

st.title("Dashboard")
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

# Tablas y gráficos
tab1, tab2 = st.tabs(["Procedimientos negociados sin publicidad", "Distribución de importe en procedimiento Negociado sin publicidad"])

fig1 = px.scatter(df_merged, x='importe_adj_con_iva', y='presupuesto_con_iva', size='numlicit', color='procedimiento')
fig2 = px.box(df_merged.query("procedimiento == 'Negociado sin publicidad'"), x='importe_adj_con_iva')

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig2, theme=None, use_container_width=True)