import streamlit as st
import time

# Configuración de la página
st.set_page_config(
    page_title='Sistema de Gestión Veterinaria',
    layout='wide',
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con título más elaborado
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(120deg, #2B4162 0%, #12100E 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        margin: -4rem -4rem 2rem -4rem;
        position: relative;
        overflow: hidden;
    }
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }
    .header-content {
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
    }
    .main-title {
        color: #FFFFFF;
        font-size: 3.2rem;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        font-family: 'Georgia', serif;
        text-transform: uppercase;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 1rem;
        display: inline-block;
    }
    .subtitle {
        color: #E5E5E5;
        font-size: 1.4rem;
        font-weight: 300;
        margin: 1rem 0;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
    }
    .decorative-line {
        width: 150px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFFFFF, transparent);
        margin: 1.5rem auto;
    }
    .established {
        color: #CCCCCC;
        font-size: 1rem;
        font-style: italic;
        margin-top: 1rem;
        font-family: 'Georgia', serif;
    }
    </style>
    <div class="header-container">
        <div class="header-content">
            <h1 class="main-title">SISTEMA DE GESTIÓN VETERINARIA</h1>
            <div class="decorative-line"></div>
            <p class="subtitle">Clinica cuatro patas</p>
            <p class="established">Creada en 2024</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Logo centrado
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image('logo.jpg', use_column_width=True)

# Sección de información mejorada
st.markdown("""
    <style>
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        padding: 2rem;
        background: linear-gradient(to bottom, #FFFFFF, #F8F9FA);
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #2B4162;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .feature-title {
        color: #2B4162;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Georgia', serif;
        border-bottom: 2px solid #E5E5E5;
        padding-bottom: 0.5rem;
    }
    .feature-description {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .feature-item {
        color: #4A4A4A;
        padding: 0.5rem 0;
        border-bottom: 1px solid #F0F0F0;
        font-size: 0.95rem;
    }
    .section-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .section-title {
        color: #2B4162;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Georgia', serif;
    }
    .section-subtitle {
        color: #666;
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Contenido de la sección
st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Opciones de nuestra clinica</h2>
    </div>
""", unsafe_allow_html=True)

# Grid de características
st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <h3 class="feature-title">Gestión de Expedientes</h3>
            <ul class="feature-list">
                <li class="feature-item">• Dar de alta a un cliente</li>
                <li class="feature-item">• Dar de alta a un animal</li>
                <li class="feature-item">• Establecer una cita</li>
                <li class="feature-item">• Dar de baja a un cliente</li>
                <li class="feature-item">• Dar de baja a un animal</li>
                <li class="feature-item">• Buscar un cliente</li>
                <li class="feature-item">• Buscar un animal</li>
                <li class="feature-item">• Estadisticas</li>
            </ul>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar mejorado
st.sidebar.markdown("""
    <div style='background-color: #F8F9FA; padding: 1rem; border-radius: 8px;'>
        <h3 style='color: #2B4162; font-size: 1.2rem; margin-bottom: 1rem;'>Panel de Control</h3>
        <p style='color: #4A4A4A; font-size: 1rem;'>Seleccione una opción del menú para acceder a las diferentes funcionalidades del sistema.</p>
    </div>
""", unsafe_allow_html=True)