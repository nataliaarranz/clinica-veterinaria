from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Base

#Configurar la base de datos
DATABASE_URL = "sqlite:///clinica_veterinaria.db"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)
