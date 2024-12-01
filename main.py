from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import time

app = FastAPI()

class UsuarioBase(BaseModel):
    nombre: str
    apellidos: str
    contrasenia: str
    direccion: str
    telefono: int
    email: str
    rol_usuario: str

class UsuarioBase2(BaseModel):
    id_usuario: int
    nombre: str
    apellidos: str
    contrasenia:str
    direccion: str
    telefono: int
    email: str
    rol_usuario: str

class CitasBase(BaseModel):
    id_usuario: int
    fecha_cita: str
    hora_cita: str

class CitasBase2(BaseModel):
    id_cita: int
    id_usuario: int
    fecha_cita: str
    hora_cita: str

class CitasBase3(BaseModel):
    fecha_cita: str
    hora_cita: str

class VideosBase(BaseModel):
    id_usuario: int
    link_video: str
    descripcion: str

class VideosBase2(BaseModel):
    id_ejercicio: int
    id_usuario: int
    link_video: str
    descripcion: str

class VideosBase3(BaseModel):
    link_video: str
    descripcion: str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/registro/", status_code=status.HTTP_201_CREATED, tags=['Usuario'])
async def crear_registro_usuario(registro:UsuarioBase, db:db_dependency):
    db_registro = models.Usuario(**registro.dict())
    db.add(db_registro)
    db.commit()
    return "El registro se ralizo exitosamente"

@app.get("/listarusuarios/", status_code=status.HTTP_200_OK, tags=['Usuario'])
async def consultar_registros_usuarios(db:db_dependency):
    registros = db.query(models.Usuario).all()
    return registros

@app.get("/consultarusuario/{nombre}", status_code=status.HTTP_200_OK, tags=['Usuario'])
async def consultar_registros_por_documento(nombre, db:db_dependency):
    registro = db.query(models.Usuario).filter(models.Usuario.nombre==nombre).first()
    if registro is None:
        HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.delete("/borrarusuario/{id_usuario}",status_code=status.HTTP_200_OK, tags=['Usuario'])
async def borrar_registro(id_usuario, db:db_dependency):
    registroborrar = db.query(models.Usuario).filter(models.Usuario.id_usuario==id_usuario).first()
    if registroborrar is None:
        HTTPException(status_code=404, detail="No se puede borrar porque no existe el registro")
        return "No se puede borrar porque no existe el registro"
    else:
        db.delete(registroborrar)
        db.commit()
        return "El registro se elimino exitosamente"

@app.put("/modificarusuario/{id_usuario}",status_code=status.HTTP_200_OK, tags=['Usuario'])
async def modificar_registro(id_usuario, registro:UsuarioBase,  db:db_dependency):
    registroactualizar = db.query(models.Usuario).filter(models.Usuario.id_usuario==id_usuario).first()
    if registroactualizar is None:
        HTTPException(status_code=404, detail="No se puede borrar porque no existe el registro")
        return "No se puede actualizar porque no existe el registro"
    else:
        registroactualizar.nombre = registro.nombre
        registroactualizar.apellidos = registro.apellidos
        registroactualizar.contrasenia = registro.contrasenia
        registroactualizar.direccion = registro.direccion
        registroactualizar.telefono = registro.telefono
        registroactualizar.email = registro.email
        registroactualizar.rol_usuario = registro.rol_usuario
        db.commit()
        db.refresh(registroactualizar)
        return "El registro se actualizo exitosamente"

@app.post("/actualizarusuario/", status_code=status.HTTP_200_OK, tags=['Usuario'])
async def actualizar_registro(registro:UsuarioBase2, db:db_dependency):
    registroactualizar = db.query(models.Usuario).filter(models.Usuario.id_usuario==registro.id_usuario).first()
    if registroactualizar is None:
        HTTPException(status_code=404, detail="No se encuentra el registro")
        return "No se puede actualizar porque no existe el registro"
    else:
        registroactualizar.nombre = registro.nombre
        registroactualizar.apellidos = registro.apellidos
        registroactualizar.contrasenia = registro.contrasenia
        registroactualizar.direccion = registro.direccion
        registroactualizar.telefono = registro.telefono
        registroactualizar.email = registro.email
        registroactualizar.rol_usuario = registro.rol_usuario
        db.commit()
        return "Registro actualizado exitosamente"
    

#Manejo de las citas
@app.post("/registrocitas/", status_code=status.HTTP_201_CREATED, tags=['Citas'])
async def crear_registro_cita(registro:CitasBase, db:db_dependency):
    registrarcita = db.query(models.Usuario).filter(models.Usuario.id_usuario==registro.id_usuario).first()
    if registrarcita is None:
        HTTPException(status_code=404, detail="No se puede registrar cita porque el usuario no existe")
        return "No se puede agendar cita porque no existe el usuario"
    else:
        db_registro = models.Citas(**registro.dict())
        db.add(db_registro)
        db.commit()
        return "El registro se ralizo exitosamente"

@app.get("/listarcitas/", status_code=status.HTTP_200_OK, tags=['Citas'])
async def consultar_citas(db:db_dependency):
    registros = db.query(models.Citas).all()
    return registros

@app.get("/consultarcita/{id_usuario}", status_code=status.HTTP_200_OK, tags=['Citas'])
async def consultar_registros_por_documento(id_usuario, db:db_dependency):
    registro = db.query(models.Citas).filter(models.Citas.id_usuario==id_usuario).first()
    if registro is None:
        HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.delete("/borrarcita/{id_cita}",status_code=status.HTTP_200_OK, tags=['Citas'])
async def borrar_registro(id_cita, db:db_dependency):
    registroborrar = db.query(models.Citas).filter(models.Citas.id_cita==id_cita).first()
    if registroborrar is None:
        HTTPException(status_code=404, detail="No se puede borrar porque no existe el registro")
        return "No se puede borrar porque no existe el registro"
    else:
        db.delete(registroborrar)
        db.commit()
        return "El registro se elimino exitosamente"

@app.put("/modificarcita/{id_usuario}",status_code=status.HTTP_200_OK, tags=['Citas'])
async def modificar_registro(id_usuario, registro:CitasBase3,  db:db_dependency):
    registroactualizar = db.query(models.Citas).filter(models.Citas.id_usuario==id_usuario).first()
    if registroactualizar is None:
        HTTPException(status_code=404, detail="No se puede actualizar porque no existe el registro")
        return "No se puede actualizar porque no existe el registro"
    else:
        registroactualizar.fecha_cita = registro.fecha_cita
        registroactualizar.hora_cita = registro.hora_cita
        db.commit()
        db.refresh(registroactualizar)
        return "El registro se actualizo exitosamente"

#Manejo de los videos
@app.post("/registrovideos/", status_code=status.HTTP_201_CREATED, tags=['Videos'])
async def crear_registro_video(registro:VideosBase, db:db_dependency):
    registrarvideo = db.query(models.Usuario).filter(models.Usuario.id_usuario==registro.id_usuario).first()
    if registrarvideo is None:
        HTTPException(status_code=404, detail="No se puede añadir video porque no existe el usuario")
        return "No se puede añadir video porque no existe el usuario"
    else:
        db_registro = models.Videos(**registro.dict())
        db.add(db_registro)
        db.commit()
        return "El video se añadido de manera exitosa"

@app.get("/listarvideos/", status_code=status.HTTP_200_OK, tags=['Videos'])
async def consultar_videos(db:db_dependency):
    registros = db.query(models.Videos).all()
    return registros

@app.get("/consultarvideo/{id_video}", status_code=status.HTTP_200_OK, tags=['Videos'])
async def consultar_registros_por_documento(id_video, db:db_dependency):
    registro = db.query(models.Videos).filter(models.Videos.id_video==id_video).first()
    if registro is None:
        HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.delete("/borrarvideo/{id_video}",status_code=status.HTTP_200_OK, tags=['Videos'])
async def borrar_registro(id_video, db:db_dependency):
    registroborrar = db.query(models.Videos).filter(models.Videos.id_video==id_video).first()
    if registroborrar is None:
        HTTPException(status_code=404, detail="No se puede borrar porque no existe el registro")
        return "No se puede borrar porque no existe el registro"
    else:
        db.delete(registroborrar)
        db.commit()
        return "El registro se elimino exitosamente"

@app.put("/modificarvideo/{id_video}",status_code=status.HTTP_200_OK, tags=['Videos'])
async def modificar_registro(id_video, registro:VideosBase3,  db:db_dependency):
    registroactualizar = db.query(models.Videos).filter(models.Videos.id_video==id_video).first()
    if registroactualizar is None:
        HTTPException(status_code=404, detail="No se puede actualizar porque no existe el registro")
        return "No se puede actualizar porque no existe el registro"
    else:
        registroactualizar.link_video = registro.link_video
        registroactualizar.descripcion = registro.descripcion
        db.commit()
        db.refresh(registroactualizar)
        return "El registro se actualizo exitosamente"
    
