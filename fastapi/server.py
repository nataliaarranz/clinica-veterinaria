import os
import pandas as pd
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel
from typing import List, Optional
from datetime import datetime, date
#from data import SessionLocal, engine
from data import *

app = FastAPI()
DATBASE_URL = "sqlite:///clinica_veterinaria.db"

# Modelos de datos
class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Tratamiento(BaseModel):
    id: Optional[int]
    nombre_tratamiento: str
    importe_con_iva: float
    fecha: datetime

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
    fecha_alta: Optional[datetime] = None
    dni_dueno: str

class Cita(BaseModel):
    id: Optional[int]
    nombre_animal: str
    nombre_dueno: str
    tratamiento: str
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None

class Factura(BaseModel):
    id: Optional[int]
    nombre_dueno: str
    nombre_animal: str
    tratamiento: str
    importe_con_iva: float
    fecha: datetime

# Interfaz para el manejo de datos
class DataRepository:
    def get_all(self) -> List[dict]:
        raise NotImplementedError

    def add(self, item: dict):
        raise NotImplementedError

    def delete(self, identifier: str):
        raise NotImplementedError
    
def beneficio_neto(df):
    if df is None or 'importe_adj_con_iva' not in df.columns:
        return "Error al cargar los contratos."
    
    # Calcular ingresos
    ingresos_totales = df['importe_adj_con_iva'].sum()
    
    # Definir gastos fijos
    material_consulta = 10
    gastos_totales = material_consulta
    
    # Calcular beneficio neto
    beneficio_neto = ingresos_totales - gastos_totales
    return beneficio_neto

# Implementación para Dueños
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

class TratamientoRepository(DataRepository):
    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["id", "nombre_tratamiento", "importe_con_iva", "fecha"])
            df.to_csv(self.filename, index=False)

    def add(self, tratamiento: Tratamiento):
        # Leer el archivo existente para obtener el siguiente ID
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            next_id = df['id'].max() + 1 if not df.empty else 1  # Obtener el siguiente ID
            tratamiento.id = next_id  # Asignar el ID al tratamiento
            nuevo_registro = pd.DataFrame([tratamiento.dict()])
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            df.to_csv(self.filename, index=False)
        else:
            raise HTTPException(status_code=404, detail="Archivo de tratamientos no encontrado.")

class FacturaRepository(DataRepository):
    def __init__(self, filename: str):
        self.filename = filename

    def get_all(self) -> List[dict]:
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df.to_dict(orient="records")
        raise HTTPException(status_code=404, detail="No hay facturas registradas")

    def add(self, factura: dict):
        nuevo_registro = pd.DataFrame([factura])
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = pd.concat([df, nuevo_registro], ignore_index=True)
        else:
            df = nuevo_registro
        df.to_csv(self.filename, index=False)

# Inicialización del repositorio de facturas
factura_repository = FacturaRepository("registroFacturas.csv")
# Implementación para Animales
class AnimalRepository(DataRepository):
    def __init__(self, filename: str):
        self.filename = filename

    def get_all(self) -> List[dict]:
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            return df.to_dict(orient="records")
        raise HTTPException(status_code=404, detail="No hay animales registrados")

    def add(self, animal: Animal):
        nuevo_registro = pd.DataFrame([animal.dict()])
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = pd.concat([df, nuevo_registro], ignore_index=True)
        else:
            df = nuevo_registro
        df.to_csv(self.filename, index=False)

    def delete(self, chip_animal: str):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df = df[df["chip_animal"].astype(str) != chip_animal]  # Asegúrate de que se compare como string
            df.to_csv(self.filename, index=False)
        else:
            raise HTTPException(status_code=404, detail="Archivo de registros no encontrado.")

# Inicialización de los repositorios
dueno_repository = DuenoRepository("registroDuenos.csv")
animal_repository = AnimalRepository("registroAnimales.csv")
tratamiento_repository = TratamientoRepository("registroTratamientos.csv")
factura_repository = FacturaRepository("registroFacturas.csv")

# Endpoints para dueños
@app.get("/duenos/")
def get_duenos():
    try:
        # Verificar si el archivo existe
        if not os.path.exists("registroDuenos.csv"):
            return {"duenos": []}  # Devolver lista vacía si no hay archivo
        
        return dueno_repository.get_all()
    except Exception as e:
        logging.error(f"Error al obtener dueños: {str(e)}")  # Agregar logging
        return {"duenos": []}  # Devolver lista vacía en caso de error

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

@app.get("/duenos/{dni_dueno}") 
async def buscar_dueno(dni_dueno: str): 
    try:
        duenos = dueno_repository.get_all()
        dueno = next((dueno for dueno in duenos if dueno['dni_dueno'].strip() == dni_dueno.strip()), None)
        if dueno is None:
            raise HTTPException(status_code=404, detail="Dueño no encontrado.")
        return dueno
    except Exception as e:
        logging.error(f"Error inesperado al buscar dueño: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al buscar dueño: {str(e)}")

# Endpoints para animales
@app.get("/animales/")
def get_animales():
    try:
        return animal_repository.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los animales: {str(e)}")

@app.get("/animales/{chip_animal}")
async def buscar_animal(chip_animal: str):
    try:
        animales = animal_repository.get_all()
        print(f"Animales actuales: {animales}")  # Para depuración
        print(f"Buscando animal con chip: {chip_animal}")  # Para depuración
        animal = next((a for a in animales if str(a['chip_animal']).strip() == chip_animal.strip()), None)
        if animal is None:
            raise HTTPException(status_code=404, detail="Animal no encontrado.")
        return animal
    except Exception as e:
        print(f"Error al buscar animal: {str(e)}")  # Imprimir el error
        raise HTTPException(status_code=500, detail=f"Error inesperado al buscar animal: {str(e)}")

@app.post("/alta_animal/")
async def alta_animal(data: Animal):
    try:
        data.fecha_alta = datetime.now()
        animal_repository.add(data)
        return {"message": "Animal registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

@app.delete("/animales/{chip_animal}")
def eliminar_animal(chip_animal: str):
    try:
        print(f"Intentando eliminar animal con chip: {chip_animal}")
        animales = animal_repository.get_all()
        print(f"Animales actuales: {animales}")
        animal_repository.delete(chip_animal)
        return {"detail": "Animal eliminado exitosamente"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Endpoints para citas
citas_db = []
next_id = 1


@app.get("/citas/")
def get_citas():
    try:
        return citas_db  # Devuelve la lista de citas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las citas: {str(e)}")

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
    global citas_db
    citas_db = [cita for cita in citas_db if cita.id != cita_id]
    return {"detail": "Cita eliminada exitosamente"}

# Endpoint para recuperar datos de contratos
@app.get("/retrieve_data/")
def retrieve_data():
    try:
        todosmisdatos = pd.read_csv('./contratos_inscritos_simplificado_2023.csv', sep=';')
        todosmisdatos = todosmisdatos.fillna(0)
        todosmisdatosdict = todosmisdatos.to_dict(orient='records')
        return {"contratos": todosmisdatosdict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar datos: {str(e)}")

# Endpoint para obtener los tratamientos:
@app.get("/tratamientos/")
def get_tratamientos():
    try:
        return tratamiento_repository.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los tratamientos: {str(e)}")
    

@app.post("/alta_tratamiento/")
async def alta_tratamiento(data: Tratamiento):
    try:
        tratamiento_repository.add(data)
        return {"message": "Tratamiento registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar los datos: {e}")

# Endpoint para obtener todas las facturas:
@app.get("/facturas/")
def get_facturas():
    try:
        df = factura_repository.get_all()
        # Convertir a DataFrame
        df_facturas = pd.DataFrame(df)
        
        # Asegurarse de que los valores sean válidos
        df_facturas['importe_con_iva'] = pd.to_numeric(df_facturas['importe_con_iva'], errors='coerce').fillna(0)
        
        # Eliminar filas con valores no válidos
        df_facturas = df_facturas.dropna()
        
        return df_facturas.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las facturas: {str(e)}")
    
@app.post("/alta_factura/")
async def alta_factura(data: Factura):
    try:
        # Agregar la factura al repositorio
        factura_repository.add(data.dict())  # Asegúrate de convertir a dict
        return {"message": "Factura registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la factura: {e}")
    
# Endpoint para el beneficio 
@app.get("/beneficio_neto/")
def get_beneficio_neto():
    try:
        # Cargar los datos de facturas
        df_facturas = pd.read_csv('registroFacturas.csv')
        df_facturas['importe_con_iva'] = df_facturas['importe_con_iva'].astype(float)

        # Definir gastos fijos
        gastos_fijos = 10  # Gastos fijos por factura

        # Calcular el beneficio neto
        df_facturas['beneficio_neto'] = df_facturas['importe_con_iva'] - gastos_fijos  # Restar gastos fijos a cada factura
        beneficio_neto_total = df_facturas['beneficio_neto'].sum()  # Sumar todos los beneficios netos

        return {"beneficio_neto": beneficio_neto_total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular el beneficio neto: {str(e)}")
    

@app.get("/facturacion_total/")
def get_facturacion_total():
    try:
        # Cargar los datos de facturas
        df_facturas = pd.read_csv('registroFacturas.csv')
        df_facturas['importe_con_iva'] = df_facturas['importe_con_iva'].astype(float)

        # Calcular la facturación total
        facturacion_total = df_facturas['importe_con_iva'].sum()

        return {"facturacion_total": facturacion_total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular la facturación total: {str(e)}")
    
# Endpoint para enviar formulario
class FormData(BaseModel):
    date: str

