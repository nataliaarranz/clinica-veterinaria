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

def info_box(texto, color=None):
    st.markdown(f'<div style="background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{texto}</p></div>', unsafe_allow_html=True)

# Cargar los datos
df_merged = load_data('http://fastapi:8000/retrieve_data')

# Verificar si los datos se cargaron correctamente
if df_merged is None:
    st.error("No se pudieron cargar los datos. Verifica la conexión con el servidor o la URL.")
else:
    registros = str(df_merged.shape[0])
    adjudicatarios = str(len(df_merged.adjudicatario.unique()))
    centro = str(len(df_merged.centro_seccion.unique()))
    tipologia = str(len(df_merged.tipo.unique()))
    presupuesto_medio = str(round(df_merged.presupuesto_con_iva.mean(), 2))
    adjudicado_medio = str(round(df_merged.importe_adj_con_iva.mean(), 2))

    sns.set_palette("pastel")

    st.title("Dashboard de seguimiento ∭∭∭∭∭")
    st.header("Información general")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        col1.subheader('# contratos')
        info_box(registros)
    with col2:
        col2.subheader('# adjudicatarios')
        info_box(adjudicatarios)
    with col3:
        col3.subheader('# centros')
        info_box(centro)

    with col4:
        col4.subheader('# tipologías')
        info_box(tipologia)

    with col5:
        col5.subheader('# presupuesto medio')
        info_box(presupuesto_medio)
    with col6:
        col6.subheader('# importe medio adjud')
        info_box(adjudicado_medio)

    tab1, tab2 = st.tabs(["Procedimientos negociados sin publicidad", "Distribución de importe en procedimiento Negociado sin publicidad"])

    fig1 = px.scatter(df_merged, x='importe_adj_con_iva', y='presupuesto_con_iva', size='numlicit', color='procedimiento')
    fig2 = px.box(df_merged.query("procedimiento == 'Negociado sin publicidad'"), x='importe_adj_con_iva')

    with tab1:
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig2, theme=None, use_container_width=True)