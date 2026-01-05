"""
Paquete de base de datos con SQLAlchemy ORM
"""
from .models import Producto, Base
from .config import db_config
from .repository import ProductoRepository

__all__ = ['Producto', 'Base', 'db_config', 'ProductoRepository']

