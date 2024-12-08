from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# Modelo Dueño
class Dueno(Base):
    __tablename__ = 'Duenos'

    id_dueno = Column(Integer, primary_key=True, autoincrement=True)
    nombre_dueno = Column(String, nullable=False)
    telefono_dueno = Column(String, nullable=True)
    email_dueno = Column(String, nullable=False)
    dni_dueno = Column(String, unique=True, nullable=False)
    direccion_dueno = Column(String, nullable=False)

    # Relación con Animales
    animales = relationship("Animal", back_populates="dueno")
    facturas = relationship("Factura", back_populates="dueno")
    citas = relationship("Cita", back_populates="dueno")

# Modelo Animal
class Animal(Base):
    __tablename__ = 'Animales'

    id_animal = Column(Integer, primary_key=True, autoincrement=True)
    nombre_animal = Column(String, nullable=False)
    chip_animal = Column(String, unique=True, nullable=False)
    especie_animal = Column(String, nullable=False)
    nacimiento_animal = Column(Date, nullable=False)
    sexo_animal = Column(String, nullable=False)
    id_dueno = Column(Integer, ForeignKey('Duenos.id_dueno'), nullable=False)
    
    # Relaciones
    dueno = relationship("Dueno", back_populates="animales")
    facturas = relationship("Factura", back_populates="animal")
    citas = relationship("Cita", back_populates="animal")

#Modelo Factura
class Factura(Base):
    __tablename__ = 'Facturas'
    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_dueno = Column(Integer, ForeignKey('Duenos.id_dueno'), nullable=False)
    id_animal = Column(Integer, ForeignKey('Animales.id_animal'), nullable=False)
    tratamiento = Column(Text, nullable=False)
    fecha_factura = Column(Date, nullable=False)
    precio_sin_iva = Column(Float, nullable=False)
    precio_con_iva = Column(Float, nullable=False)
    
    #Relaciones
    dueno = relationship("Dueno", back_populates="facturas")
    animal = relationship("Animal", back_populates="facturas")

#Modelo Tratamiento
class Tratamiento(Base):
    __tablename__ = 'Tratamientos'
    id_tratamiento = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tratamiento = Column(String, nullable=False)
    precio_sin_iva = Column(Float, nullable=False)


# Modelo Cita
class Cita(Base):
    __tablename__ = 'citas'

    id_cita = Column(Integer, primary_key=True, autoincrement=True)
    id_dueno = Column(Integer, ForeignKey('Duenos.id_dueno'), nullable=False)
    id_animal = Column(Integer, ForeignKey('Animales.id_animal'), nullable=False)
    #nombre_animal = Column(String, nullable=False)
    #nombre_dueno = Column(String, nullable=False)
    tratamiento = Column(String, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)

    # Relación con Animal
    dueno = relationship("Dueno", back_populates="citas")
    animal = relationship("Animal", back_populates="citas")

