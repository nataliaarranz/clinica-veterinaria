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
    fecha_nacimiento_animal: date
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
@app.delete("/baja_dueños/{dni_dueño}")
async def baja_dueño(dni_dueño: str):
    #Buscar dueño a dar de baja
    for index, registro in enumerate (registroDueños_csv):
        if registro["dni_dueño"] == dni_dueño:
            eliminado = registroDueños_csv.pop(index)
            return {"Dueño eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Dueño no encontrado")


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
                "nombre_animal", "chip_animal", "especie_animal", "fecha_nacimiento_animal",
                "sexo"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registroAnimales_csv, index=False)
        return {"message": "Animal registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

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
