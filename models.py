from sqlalchemy import String, Integer, Time, Column
from database import Base

class Usuario(Base):
    __tablename__="usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellidos = Column(String(50))
    contrasenia = Column(String(100))
    direccion = Column(String(100))
    telefono = Column(Integer)
    email = Column(String(100))
    rol_usuario = Column(String(20))

class Citas(Base):
    __tablename__="citas"
    id_cita = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    fecha_cita = Column(String(50))
    hora_cita = Column(Time)

class Videos(Base):
    __tablename__="videos"
    id_video = Column(Integer, primary_key=True, index=True)
    id_usuario =  Column(Integer)
    link_video = Column(String(500))
    descripcion = Column(String(500))

