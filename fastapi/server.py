import shutil

import io
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile,Form
import pandas as pd
from typing import  List

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
@app.post("/citas/{cita_id}", response_model=Cita)
def crear_cita(cita: Cita):
    global next_id
    cita.id = next_id
    next_id += 1
    citas_db.append(cita)
    return cita
#Modificar cita
@app.put("/citas/{cita_id}", response_model=Cita)
def modificar_cita(cita_id: int, cita_actualizada: Cita):
    for index, cita in enumerate(citas_db):
        if cita.id == cita_id:
            citas_db[index] = cita_actualizada
            citas_db[index].id = cita_id
            return citas_db[index]
    raise HTTPExecption(status_code=404, detail="Cita no encontrada")

#Eliminar cita
#revisar 
@app.delete("/citas/{cita_id}")
def eliminar_cita(cita_id: int):
    if cita.id == cita_id:
        return {"message": f"Cita con ID {cita_id} eliminada exitosamente"}
    else:
        return {"error": f"No se pudo borrar la cita"}