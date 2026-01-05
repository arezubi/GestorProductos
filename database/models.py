"""
Modelos de la base de datos usando SQLAlchemy ORM
"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Producto(Base):
    """Modelo de la tabla producto"""
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String, default='Sin categoría')
    stock = Column(Integer, default=0)

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio}, categoria='{self.categoria}', stock={self.stock})>"

    def __str__(self):
        return f"{self.nombre} - {self.precio}€"

