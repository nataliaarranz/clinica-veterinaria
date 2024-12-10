import streamlit as st
import requests
import time

# Clase para manejar la lógica de la baja de dueños
class DuenoService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def dar_baja(self, dni_dueno):
        try:
            response = requests.delete(f"{self.backend_url}/{dni_dueno}")
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, "No existe un dueño con el DNI introducido."
            else:
                return False, f"Error al dar de baja: {response.status_code}, Detalle: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {e}"

# Clase para manejar la lógica de la baja de animales
class AnimalService:
    def __init__(self, backend_url):
        self.backend_url = backend_url

    def dar_baja(self, chip_animal):
        try:
            response = requests.delete(f"{self.backend_url}/{chip_animal}")
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, "No existe un animal con el número de chip introducido."
            else:
                return False, f"Error al dar de baja: {response.status_code}, Detalle: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {e}"

# Clase para manejar la interfaz de usuario
class BajaInterface:
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
                    ❌ Sistema de Bajas ❌
                </h1>
            </div>
        """, unsafe_allow_html=True)

    def crear_formulario_baja_duenos(self):
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
                        👤 Baja de Dueño
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("dar_baja_dueno"):
                dni_dueno = st.text_input("DNI del dueño:", 
                                        max_chars=10,
                                        placeholder="Introduce el DNI",
                                        help="Ingresa el DNI sin guiones ni espacios")
                
                col1, col2, col3 = st.columns([1,1,1])
                with col2:
                    submitted = st.form_submit_button("🗑️ Dar de Baja", 
                                                    use_container_width=True,
                                                    type="primary")
            
            if submitted:
                if not dni_dueno.strip():
                    st.error("❌ El campo DNI no puede estar vacío")
                else:
                    with st.spinner("Procesando baja..."):
                        time.sleep(0.5)
                        success, message = self.dueno_service.dar_baja(dni_dueno)
                        if success:
                            st.success("✅ Se ha dado de baja al dueño correctamente")
                            self._mostrar_resultado_baja(message)
                        else:
                            st.error(f"❌ {message}")

    def crear_formulario_baja_animal(self):
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
                        🐾 Baja de Animal
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("dar_baja_animal"):
                chip_animal = st.text_input("Chip del animal:", 
                                          max_chars=15,
                                          placeholder="Introduce el número de chip",
                                          help="Ingresa el número de chip completo")
                
                col1, col2, col3 = st.columns([1,1,1])
                with col2:
                    submitted = st.form_submit_button("🗑️ Dar de Baja",
                                                    use_container_width=True,
                                                    type="primary")
            
            if submitted:
                if not chip_animal.strip():
                    st.error("❌ El campo chip no puede estar vacío")
                else:
                    with st.spinner("Procesando baja..."):
                        time.sleep(0.5)
                        success, message = self.animal_service.dar_baja(chip_animal)
                        if success:
                            st.success("✅ Se ha dado de baja al animal correctamente")
                            self._mostrar_resultado_baja(message)
                        else:
                            st.error(f"❌ {message}")

    def _mostrar_resultado_baja(self, resultado):
        st.markdown(f"""
            <div style='background: #f8f9fa; 
                       padding: 1.5rem; 
                       border-radius: 8px; 
                       border-left: 4px solid #2B4162;
                       margin: 1rem 0;'>
                <h3 style='color: #2B4162; margin-bottom: 1rem;'>Detalles de la baja</h3>
                <pre style='background: white; 
                           padding: 1rem; 
                           border-radius: 4px;
                           font-family: monospace;'>{str(resultado)}</pre>
            </div>
        """, unsafe_allow_html=True)

# Inicialización de servicios y la interfaz
duenos_backend = "http://fastapi:8000/duenos"
animales_backend = "http://fastapi:8000/animales"

dueno_service = DuenoService(duenos_backend)
animal_service = AnimalService(animales_backend)
baja_interface = BajaInterface(dueno_service, animal_service)

# Mostrar interfaz
baja_interface.mostrar_titulo()

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
                🗑️ Opciones de Baja
            </h3>
        </div>
    """, unsafe_allow_html=True)
    opcion = st.radio("Seleccione tipo de baja:",
                      ["Dueño", "Animal"],
                      label_visibility="collapsed")

# Mostrar el formulario correspondiente
if opcion == "Dueño":
    baja_interface.crear_formulario_baja_duenos()
elif opcion == "Animal":
    baja_interface.crear_formulario_baja_animal()