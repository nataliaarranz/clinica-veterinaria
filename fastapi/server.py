import shutil
import io
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import pandas as pd
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel as PydanticBaseModel

#NUEVO PARA ARREGLAR DASHBOARD
app = FastAPI()

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

# Definición de modelos
class Dueno(BaseModel):
    nombre_dueno: str
    telefono_dueno: Optional[str] = None
    email_dueno: str  
    dni_dueno: str
    direccion_dueno: str

class Animal(BaseModel):
    nombre_animal: str
    chip_animal: str
    especie_animal: str
    nacimiento_animal: date
    sexo: str

class Cita(BaseModel):
    id: Optional[int]
    nombre_animal: str
    nombre_dueno: str
    tratamiento: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None

# Rutas para contratos (se mantiene tu implementación actual)
class Contrato(BaseModel):
    fecha: str
    centro_seccion: str
    nreg: str
    nexp: str
    objeto: str
    tipo: str
    procedimiento: str
    numlicit: str
    numinvitcurs: str
    proc_adjud: str
    presupuesto_con_iva: str
    valor_estimado: str
    importe_adj_con_iva: str
    adjuducatario: str
    fecha_formalizacion: str
    I_G: str

class ListadoContratos(BaseModel):
    contratos = List[Contrato]

app = FastAPI(
    title="Servidor de datos",
    description="Servimos datos de contratos y citas veterinarias.",
    version="0.1.0",
)

# Archivos CSV
registroDuenos_csv = "registroDuenos.csv"
registroAnimales_csv = "registroAnimales.csv"

#NUEVO PARA ARREGLAR DASHBOARD
@app.get("/retrieve_data")
async def retrieve_data():
    try:
        if os.path.exists("contratos_incritos_simplificado_2023.csv"):
            contratos_df = pd.read_csv("contratos_incritos_simplificado_2023.csv")
            contratos = contratos_df.to_dict(orient="records")
            return {"contratos": contratos}
        else:
            raise HTTPException(status_code=404, detail="No se encontraron contratos registrados")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")

# Endpoints para dueños
@app.get("/duenos/")
def get_duenos():
    if os.path.exists(registroDuenos_csv):
        registro_df = pd.read_csv(registroDuenos_csv)
        duenos = registro_df.to_dict(orient="records")
        return duenos
    else:
        raise HTTPException(status_code=404, detail="No hay dueños registrados")

@app.post("/alta_duenos/")
async def alta_dueno(data: Dueno):
    try:
        if os.path.exists(registroDuenos_csv):
            registro_df = pd.read_csv(registroDuenos_csv)
        else:
            registro_df = pd.DataFrame(columns=[
                "nombre_dueno", "telefono_dueno", "email_dueno", "dni_dueno",
                "direccion_dueno"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registroDuenos_csv, index=False)
        return {"message": "Dueño registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

#Dar de baja dueño
@app.delete("/duenos/{dni_dueno}")
async def dar_baja_dueno(dni_dueno: str):
    try:
        if not os.path.exists(registroDuenos_csv):
            raise HTTPException(status_code=404, detail="Archivo de registros no encontrado.")
        registro_df = pd.read_csv(registroDuenos_csv)
        registro_df["dni_dueno"] = registro_df["dni_dueno"].astype(str).str.strip()
        if dni_dueno.strip() not in registro_df["dni_dueno"].values:
            raise HTTPException(status_code=404, detail="Dueño con DNI especificado no encontrado.")
        registro_df = registro_df[registro_df["dni_dueno"] != dni_dueno.strip()]
        registro_df.to_csv(registroDuenos_csv, index=False)
        return {"message": f"Dueño con DNI {dni_dueno} eliminado correctamente"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de registros no encontrado.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=500, detail="El archivo de registros está vacío o corrupto.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")    

# Buscar dueño por DNI 
@app.get("/duenos/{dni_dueno}") 
async def buscar_dueno(dni_dueno: str): 
    try:
        if not os.path.exists(registroDuenos_csv):
            raise HTTPException(status_code=404, detail="Archivo de registros de dueños no encontrado.")
        registro_df = pd.read_csv(registroDuenos_csv)
        dueño = registro_df[registro_df['dni_dueno'].str.strip() == dni_dueno.strip()]
        if dueño.empty:
            raise HTTPException(status_code=404, detail="Dueño no encontrado.")
        return dueño.to_dict(orient='records')[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado al buscar dueño: {str(e)}")

# Endpoints para animales
@app.get("/animales/")
def get_animales():
    if os.path.exists(registroAnimales_csv):
        registro_df = pd.read_csv(registroAnimales_csv)
        animales = registro_df.to_dict(orient="records")
        return animales
    else:
        raise HTTPException(status_code=404, detail="No hay animales registrados")

@app.post("/alta_animal/")
async def alta_animal(data: Animal):
    try:
        if os.path.exists(registroAnimales_csv):
            registro_df = pd.read_csv(registroAnimales_csv)
        else:
            registro_df = pd.DataFrame(columns=[
                "nombre_animal", "chip_animal", "especie_animal", "nacimiento_animal",
                "sexo"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registroAnimales_csv, index=False)
        return {"message": "Animal registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

#Dar de baja animal
@app.delete("/dar_baja_animal/{chip_animal}")
async def dar_baja_animal(chip_animal: str):
    try:
        #Verificar si existe el archivo
        if not os.path.exists(registroAnimales_csv):
            raise HTTPException(status_code=404, detail="No se encontró el archivo.")
        # Cargamos los datos del CSV 
        registro_df = pd.read_csv(registroAnimales_csv)
        registro_df["chip_animal"] = registro_df["chip_animal"].astype(str)
        chip_animal = chip_animal.strip()  # Limpiar cualquier espacio extra del chip proporcionado
        #Buscar animal a dar de baja
        if chip_animal not in registro_df["chip_animal"].values:
            raise HTTPException(status_code=404, detail="Animal no encontrado.")
        
        #Eliminar animal de la lista
        registro_df = registro_df[registro_df["chip_animal"] != chip_animal]
        #Actualizar el archivo CSV
        registro_df.to_csv(registroAnimales_csv, index=False)
        return {"message": f"Animal con chip {chip_animal} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Animal no encontrado")


#Dar de baja animal
@app.delete("/baja_animal/{chip_animal}")
async def baja_animal(chip_animal: str):
    #Buscar animal a dar de baja
    for index, registro in enumerate (registroAnimales_csv):
        if registro["chip_animal"] == chip_animal:
            eliminado = registroAnimales_csv.pop(index)
            return {"Animal eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Animal no encontrado")

# Buscar animal por chip 
@app.get("/animales/{chip_animal}")
async def buscar_animal(chip_animal: str):
    try:
        if not os.path.exists(registroAnimales_csv):
            raise HTTPException(status_code=404, detail="Archivo de registros de animales no encontrado.")
        registro_df = pd.read_csv(registroAnimales_csv)
        animal = registro_df[registro_df['chip_animal'].str.strip() == chip_animal.strip()]
        if animal.empty:
            raise HTTPException(status_code=404, detail="Animal no encontrado.")
        return animal.to_dict(orient='records')[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado al buscar animal: {str(e)}")



# Endpoints para citas (se mantiene tu implementación actual)
citas_db = []
next_id = 1

@app.post("/citas/", response_model=Cita)
def crear_cita(cita: Cita):
    global next_id
    cita.id = next_id
    next_id += 1
    citas_db.append(cita)
    return cita

@app.put("/citas/{cita_id}", response_model=Cita)
def modificar_cita(cita_id: int, cita_actualizada: Cita):
    for index, cita in enumerate(citas_db):
        if cita.id == cita_id:
            citas_db[index] = cita_actualizada
            citas_db[index].id = cita_id
            return citas_db[index]
    raise HTTPException(status_code=404, detail="Cita no encontrada")

@app.delete("/citas/{cita_id}")
def eliminar_cita(cita_id: int):
    for index, cita in enumerate(citas_db):
        if cita.id == cita_id:
            del citas
