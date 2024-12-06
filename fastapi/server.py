from fastapi import FastAPI, HTTPException
import pandas as pd
import os
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel as PydanticBaseModel

app = FastAPI()

# Modelos de datos
class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

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

# Repositorios de datos
class DataRepository:
    def get_all(self) -> List[dict]:
        raise NotImplementedError

    def add(self, item: dict):
        raise NotImplementedError

    def delete(self, identifier: str):
        raise NotImplementedError

class DuenoRepository(DataRepository):
    def __init__(self, filename: str):
        self.filename = filename

    def get_all(self) -> List[dict]:
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df.to_dict(orient="records")
        raise HTTPException(status_code=404, detail="No hay dueños registrados")

    def add(self, dueno: Dueno):
        nuevo_registro = pd.DataFrame([dueno.dict()])
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = pd.concat([df, nuevo_registro], ignore_index=True)
        else:
            df = nuevo_registro
        df.to_csv(self.filename, index=False)

    def delete(self, dni_dueno: str):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = df[df["dni_dueno"] != dni_dueno]
            df.to_csv(self.filename, index=False)
        else:
            raise HTTPException(status_code=404, detail="Archivo de registros no encontrado.")

# Repositorios inicializados
dueno_repository = DuenoRepository("registroDuenos.csv")

# Endpoints para Dueños
@app.get("/duenos/")
def get_duenos():
    return dueno_repository.get_all()

@app.post("/alta_duenos/")
async def alta_dueno(data: Dueno):
    try:
        dueno_repository.add(data)
        return {"message": "Dueño registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

@app.delete("/duenos/{dni_dueno}")
async def dar_baja_dueno(dni_dueno: str):
    try:
        dueno_repository.delete(dni_dueno)
        return {"message": f"Dueño con DNI {dni_dueno} eliminado correctamente"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Inicio del servidor sin uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
