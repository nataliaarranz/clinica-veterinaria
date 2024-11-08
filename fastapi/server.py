import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, UploadFile,Form
import pandas as pd
from typing import  List, Optional
from datetime import datetime, date
from pydantic import BaseModel, EmailStr

from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Contrato(BaseModel):
    #titulo:str
    #autor:str
    #pais:str
    #genero:str
    fecha:str
    centro_seccion:str
    nreg:str
    nexp:str
    objeto:str
    tipo:str
    procedimiento:str
    numlicit:str
    numinvitcurs:str
    proc_adjud:str
    presupuesto_con_iva:str
    valor_estimado:str
    importe_adj_con_iva:str
    adjuducatario:str
    fecha_formalizacion:str
    I_G:str


class ListadoContratos(BaseModel):
    contratos = List[Contrato]

app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, pero podríamos hacer muchas otras cosas, la la la.""",
    version="0.1.0",
)

@app.get("/retrieve_data/")
def retrieve_data ():
    todosmisdatos = pd.read_csv('./contratos_inscritos_simplificado_2023.csv',sep=';')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoContratos()
    listado.contratos = todosmisdatosdict
    return listado

class FormData(BaseModel):
    date: str
    description: str
    option: str
    amount: float

@app.post("/envio/")
async def submit_form(data: FormData):
    return {"message": "Formulario recibido", "data": data}

#CITAS
class Cita(BaseModel):
    id: Optional[int]
    nombre_animal: str
    nombre_dueño: str
    tratamiento: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
#Base de datos simulada para guardar las citas
citas_db = []

#Nueva cita
@app.post("/citas/", response_model=Cita) ## revisar y no meter el cita_id
def crear_cita(cita: Cita):
    global next_id
    cita.id = next_id
    next_id += 1
    citas_db.append(cita)
    return cita
#Modificar cita
@app.put("/citas/{cita_id}", response_model=Cita)  ## Ojo, aquí en algún momento habrás tenido que enviar el id de la cita que quieres modificar
def modificar_cita(cita_id: int, cita_actualizada: Cita):
    for index, cita in enumerate(citas_db):
        if cita.id == cita_id:
            citas_db[index] = cita_actualizada
            citas_db[index].id = cita_id
            return citas_db[index]
    raise HTTPException(status_code=404, detail="Cita no encontrada")

#Eliminar cita
#revisar 
@app.delete("/citas/{cita_id}") # Lo mismo que en put
def eliminar_cita(cita_id: int):
    for index, cita in enumerate(citas_db):
        if cita.id == cita_id:
            del citas_db[index]
            return {"message": f"Cita con ID {cita_id} eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Cita no encontrada")

class Dueño(BaseModel):
    nombre_dueño: str
    telefono_dueño: str
    email_dueño: str  
    dni_dueño: str
    direccion_dueño: str

class Animal(BaseModel):
    nombre_animal: str
    numero_chip_animal: str
    especie_animal: str
    fecha_nacimiento_animal: date
    sexo: str

#Registrar dueño
@app.post("/alta_dueños/")
async def alta_dueño(data: RegistroDueños):
    #validar datos
    try:
        #cargar csv
        if os.path.exists(registro_csv):
            registro_df = pd.read_csv(registro_csv)
        #crear csv
        else:
            registro_df = pd.DataFrame(columns=[
                "nombre_dueño", "telefono_dueño", "email_dueño", "dni_dueño",
                "direccion_dueño"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registro_csv, index=False)
        # Responder con un mensaje de éxito
        return {"message": "Dueño registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

#Registrar animal
@app.post("/alta_animal/")
async def alta_animal(data: RegistroAnimal):
    #validar datos
    try:
        #cargar csv
        if os.path.exists(registro_csv):
            registro_df = pd.read_csv(registro_csv)
        #crear csv
        else:
            registro_df = pd.DataFrame(columns=[
                "nombre_animal", "numero_chip_animal", "especie_animal", 
                "fecha_nacimiento_animal", "sexo_animal"
            ])
        nuevo_registro = pd.DataFrame([data.dict()])
        registro_df = pd.concat([registro_df, nuevo_registro], ignore_index=True)
        registro_df.to_csv(registro_csv, index=False)
        # Responder con un mensaje de éxito
        return {"message": "Dueño y Animal registrados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")
#Buscar dueño y animal
@app.get("/buscar_registros/")
def buscar_registros(nombre_dueño: Optional[str] = None):
    if not os.path.exists(registro_csv):
        raise HTTPException(status_code=404, detail="Archivo de registros no encontrado")
    
    registro_df = pd.read_csv(registro_csv)
    
    if nombre_dueño:
        # Filtrar registros por el nombre del dueño
        resultados = registro_df[registro_df['nombre_dueño'].str.contains(nombre_dueño, case=False, na=False)]
        if resultados.empty:
            return {"message": "No se encontraron registros para ese dueño"}
        return resultados.to_dict(orient="records")
    
    return registro_df.to_dict(orient="records")
