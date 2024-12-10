import requests
import streamlit as st
import time

# Clase para manejar la lógica de búsqueda de dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def buscar(self, dni_dueno):
        try:
            response = requests.get(f"{self.backend_url}/{dni_dueno}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "No existe dueño con el DNI introducido"}
            else:
                return {"error": f"Error al buscar los datos: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error de conexión al buscar los datos: {e}"}

# Clase para manejar la lógica de búsqueda de animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def buscar(self, chip_animal):
        try:
            response = requests.get(f"{self.backend_url}/{chip_animal}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "No existe animal con el chip introducido"}
            else:
                return {"error": f"Error al buscar los datos: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error de conexión al buscar los datos: {e}"}

# Clase para manejar la interfaz de usuario
class SearchInterface:
    def __init__(self, dueno_service, animal_service):
        self.dueno_service = dueno_service
        self.animal_service = animal_service

    def mostrar_titulo(self):
        st.markdown("""
            <div style='background: linear-gradient(120deg, #2B4162 0%, #12100E 100%); 
                        padding: 2rem; 
                        border-radius: 10px; 
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                <h1 style='color: white; 
                           font-size: 2.2rem; 
                           margin-bottom: 0.5rem; 
                           text-align: center;
                           font-weight: 600;'>
                    🔍 Sistema de Búsqueda 🔍
                </h1>
            </div>
        """, unsafe_allow_html=True)

    def buscar_dueno(self):
        with st.container():
            st.markdown("""
                <div style='background: white; 
                           padding: 2rem; 
                           border-radius: 10px; 
                           box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                           margin-bottom: 1rem;'>
                    <h2 style='color: #2B4162; 
                             font-size: 1.5rem; 
                             margin-bottom: 1rem;'>
                        👤 Búsqueda de Dueño
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("buscar_dueno_form"):
                dni_dueno = st.text_input("DNI del dueño:", 
                                        max_chars=10,
                                        placeholder="Introduce el DNI",
                                        help="Ingresa el DNI sin guiones ni espacios")
                
                col1, col2, col3 = st.columns([1,1,1])
                with col2:
                    submitted = st.form_submit_button("🔍 Buscar", 
                                                    use_container_width=True,
                                                    type="primary")
            
            if submitted:
                with st.spinner("Buscando..."):
                    time.sleep(0.5)  # Pequeña pausa para la animación
                    resultado = self.dueno_service.buscar(dni_dueno)
                    if "error" not in resultado:
                        st.success("✅ Dueño encontrado")
                        self._mostrar_resultado_dueno(resultado)
                    else:
                        st.error(f"❌ {resultado['error']}")

    def buscar_animal(self):
        with st.container():
            st.markdown("""
                <div style='background: white; 
                           padding: 2rem; 
                           border-radius: 10px; 
                           box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                           margin-bottom: 1rem;'>
                    <h2 style='color: #2B4162; 
                             font-size: 1.5rem; 
                             margin-bottom: 1rem;'>
                        🐾 Búsqueda de Animal
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("buscar_animal_form"):
                chip_animal = st.text_input("Chip del animal:", 
                                          max_chars=15,
                                          placeholder="Introduce el número de chip",
                                          help="Ingresa el número de chip completo")
                
                col1, col2, col3 = st.columns([1,1,1])
                with col2:
                    submitted = st.form_submit_button("🔍 Buscar",
                                                    use_container_width=True,
                                                    type="primary")
            
            if submitted:
                with st.spinner("Buscando..."):
                    time.sleep(0.5)  # Pequeña pausa para la animación
                    resultado = self.animal_service.buscar(chip_animal)
                    if "error" not in resultado:
                        st.success("✅ Animal encontrado")
                        self._mostrar_resultado_animal(resultado)
                    else:
                        st.error(f"❌ {resultado['error']}")

    def _mostrar_resultado_dueno(self, resultado):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>Información del Dueño</h3>
                <p><strong>Nombre:</strong> {resultado.get('nombre_dueno', 'N/A')}</p>
                <p><strong>DNI:</strong> {resultado.get('dni_dueno', 'N/A')}</p>
                <p><strong>Teléfono:</strong> {resultado.get('telefono_dueno', 'N/A')}</p>
                <p><strong>Email:</strong> {resultado.get('email_dueno', 'N/A')}</p>
                <p><strong>Dirección:</strong> {resultado.get('direccion_dueno', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

    def _mostrar_resultado_animal(self, resultado):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>Información del Animal</h3>
                <p><strong>Nombre:</strong> {resultado.get('nombre_animal', 'N/A')}</p>
                <p><strong>Chip:</strong> {resultado.get('chip_animal', 'N/A')}</p>
                <p><strong>Especie:</strong> {resultado.get('especie_animal', 'N/A')}</p>
                <p><strong>Sexo:</strong> {resultado.get('sexo_animal', 'N/A')}</p>
                <p><strong>Fecha de Nacimiento:</strong> {resultado.get('nacimiento_animal', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)

# Inicialización de servicios y la interfaz
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
search_interface = SearchInterface(dueno_service, animal_service)

# Mostrar interfaz
search_interface.mostrar_titulo()

# Sidebar mejorado
with st.sidebar:
    st.markdown("""
        <div style='padding: 1rem; 
                    background: white; 
                    border-radius: 8px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
            <h3 style='color: #2B4162; 
                      margin-bottom: 1rem; 
                      font-size: 1.2rem;'>
                🔍 Opciones de Búsqueda
            </h3>
        </div>
    """, unsafe_allow_html=True)
    opcion_buscar = st.radio("Seleccione tipo de búsqueda:",
                            ["Buscar Dueño", "Buscar Animal"],
                            label_visibility="collapsed")

# Mostrar el formulario correspondiente
if opcion_buscar == "Buscar Dueño":
    search_interface.buscar_dueno()
elif opcion_buscar == "Buscar Animal":
    search_interface.buscar_animal()