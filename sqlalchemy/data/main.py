from database import engine, Base
from models.user import User
from models.post import Post
from datetime import datetime

# Crear todas las tablas en la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")

# Crear una sesión
db = SessionLocal()

# Agregar un dueño
dueno = Dueno(name="Juan Pérez", address="Calle Falsa 123", phone="123456789")
db.add(dueno)
db.commit()
db.refresh(dueno)

# Agregar un animal
animal = Animal(name="Fido", species="Perro", age=3, owner_id=owner.id)
db.add(animal)
db.commit()
db.refresh(animal)

# Agregar una cita
cita = cita(date=datetime(2024, 12, 10, 10, 30), reason="Vacunación", animal_id=animal.id)
db.add(cita)
db.commit()
db.close()