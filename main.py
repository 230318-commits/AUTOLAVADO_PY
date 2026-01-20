from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from model import Genero, Role, Usuario

app = FastAPI()

db: List[Usuario] = [
    Usuario(
        id=uuid4(),
        primerNombre="Jonathan",
        apellidos="Lopez",
        genero=Genero.masculino,
        roles=[Role.user]
    ),
    Usuario(
        id=uuid4(),
        primerNombre="Angel",
        apellidos="Arteaga Carrillo",
        genero=Genero.otro,
        roles=[Role.user]
    ),
    Usuario(
        id=uuid4(),
        primerNombre="Jesus",
        apellidos="Tellez Carrillo",
        genero=Genero.otro,
        roles=[Role.user]
    )
]

@app.get("/")
async def root():
    return {"message": "Xicomich o q?"}

# 🔹 Obtener todos los usuarios
@app.get("/api/v1/users", response_model=List[Usuario])
async def get_users():
    return db

# 🔍 Buscar usuario por ID
@app.get("/api/v1/users/{user_id}", response_model=Usuario)
async def get_user_by_id(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# ✏️ Actualizar usuario
@app.put("/api/v1/users/{user_id}", response_model=Usuario)
async def update_user(user_id: UUID, user_updated: Usuario):
    for index, user in enumerate(db):
        if user.id == user_id:
            user_updated.id = user_id  # se conserva el ID
            db[index] = user_updated
            return user_updated
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# 🗑️ Eliminar usuario
@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)
            return {"message": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
