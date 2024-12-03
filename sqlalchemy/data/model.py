from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo Dueño
class Dueno(Base):
    __tablename__ = 'duenos'

    id_dueno = Column(Integer, primary_key=True, autoincrement=True)
    nombre_dueno = Column(String, nullable=False)
    telefono_dueno = Column(String, nullable=True)
    email_dueno = Column(String, nullable=False)
    dni_dueno = Column(String, unique=True, nullable=False)
    direccion_dueno = Column(String, nullable=False)

    # Relación con Animales
    animales = relationship("Animal", back_populates="dueno")

# Modelo Animal
class Animal(Base):
    __tablename__ = 'animales'

    id_animal = Column(Integer, primary_key=True, autoincrement=True)
    nombre_animal = Column(String, nullable=False)
    chip_animal = Column(String, unique=True, nullable=False)
    especie_animal = Column(String, nullable=False)
    nacimiento_animal = Column(Date, nullable=False)
    sexo = Column(String, nullable=False)

    # Relación con Dueño
    dueno_id = Column(Integer, ForeignKey('duenos.id'), nullable=False)
    dueno = relationship("Dueno", back_populates="animales")

    # Relación con Citas
    citas = relationship("Cita", back_populates="animal")

# Modelo Cita
class Cita(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_animal = Column(String, nullable=False)
    nombre_dueno = Column(String, nullable=False)
    tratamiento = Column(String, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)

    # Relación con Animal
    animal_id = Column(Integer, ForeignKey('animales.id'), nullable=False)
    animal = relationship("Animal", back_populates="citas")
