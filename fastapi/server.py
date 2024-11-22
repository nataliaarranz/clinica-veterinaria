import shutil
import io
import os
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
import pandas as pd
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

# Definición de modelos
class Dueño(BaseModel):
    nombre_dueño: str
    telefono_dueño: Optional[str] = None
    email_dueño: str  
    dni_dueño: str
    direccion_dueño: str

class Animal(BaseModel):
    nombre_animal: str
    chip_animal: str
    especie_animal: str
    nacimiento_animal: date
    sexo: str

class Cita(BaseModel):
    id: Optional[int]
    nombre_animal: str
    nombre_dueño: str
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
registroDueños_csv = "registroDueños.csv"
registroAnimales_csv = "registroAnimales.csv"

# Endpoints para dueños
@app.get("/dueños/")
def get_dueños():
    if os.path.exists(registroDueños_csv):
        registro_df = pd.read_csv(registroDueños_csv)
        dueños = registro_df.to_dict(orient="records")
        return dueños
    else:
        raise HTTPException(status_code=404, detail="No hay dueños registrados")

@app.post("/alta_dueños/")
async def alta_dueño(data: Dueño):
    try:
        if os.path.exists(registroDueños_csv):
            registro_df = pd.read_csv(registroDueños_csv)
        else:
            registro_df = pd.DataFrame(columns=[
                "nombre_dueño", "telefono_dueño", "email_dueño", "dni_dueño",
                "direccion_dueño"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registroDueños_csv, index=False)
        return {"message": "Dueño registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

#Dar de baja dueño
@app.delete("/dar_baja_dueño/{dni_dueño}")
async def dar_baja_dueño(dni_dueño: str):
    try:
        #Verificar si existe el archivo
        if not os.path.exists(registroDueños_csv):
            raise HTTPException(status_code=404, detail="No se encontró el archivo.")
        # Cargamos los datos del CSV 
        registro_df = pd.read_csv(registroDueños_csv)
        #Buscar dueño a dar de baja
        if "dni_dueño" not in registro_df.columns:
            raise HTTPException(status_code=404, detail="Dueño no encontrado.")
        registro_df["dni_dueño"] = registro_df["dni_dueño"].astype(str).str.strip()
        dni_dueño = dni_dueño.strip()  # Limpiar cualquier espacio extra del DNI proporcionado
        #Verificar si existe el dueño
        if dni_dueño not in registro_df["dni_dueño"].values:
            raise HTTPException(status_code=404, detail="Dueño no encontrado.")
        #Eliminar dueño de la lista
        registro_df = registro_df[registro_df["dni_dueño"] != dni_dueño]
        #Actualizar el archivo CSV
        registro_df.to_csv(registroDueños_csv, index=False)
        return {"message": f"Dueño con DNI {dni_dueño} eliminado correctamente"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de registros no encontrado.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=500, detail="El archivo de registros está vacío o corrupto.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Buscar dueño por DNI 
@app.get("/buscar_dueño/{dni_dueño}") 
async def buscar_dueño(dni_dueño: str): 
    if not os.path.exists(registroDueños_csv):
        raise HTTPException(status_code = 404, detail = f"No se encontró el archivo de registros de dueños:{e}") 
    # Cargamos los datos del CSV 
    registro_df = pd.read_csv(registroDueños_csv) 
    # Buscamos el dueño por DNI 
    dueño = registro_df[registro_df['dni_dueño'] == dni_dueño]  
    if dueño.empty: 
        raise HTTPException(status_code = 404, detail = "Dueño no encontrado") 
    # Convertimos el resultado a un diccionario y lo devolvemos 
    return dueño.to_dict(orient = 'records')[0]


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
