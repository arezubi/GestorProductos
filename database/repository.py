"""
Repositorio para operaciones CRUD de productos usando SQLAlchemy
"""
from database.models import Producto
from database.config import db_config
from sqlalchemy.exc import SQLAlchemyError


class ProductoRepository:
    """Clase que maneja todas las operaciones de base de datos para productos"""

    def __init__(self):
        self.session = None

    def _get_session(self):
        """Obtiene una sesión de base de datos"""
        if self.session is None or not self.session.is_active:
            self.session = db_config.get_session()
        return self.session

    def crear_producto(self, nombre, precio, categoria='', stock=0):
        session = self._get_session()
        try:
            nuevo_producto = Producto(
                nombre=nombre,
                precio=float(precio),
                categoria=categoria if categoria else 'Sin categoría',
                stock=int(stock) if stock else 0
            )
            session.add(nuevo_producto)
            session.commit()
            session.refresh(nuevo_producto)
            return nuevo_producto
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al crear producto: {e}")
            return None

    def obtener_todos_productos(self, orden_por='nombre', descendente=True):
        session = self._get_session()
        try:
            query = session.query(Producto)

            # Ordenar según el campo especificado
            campo_orden = getattr(Producto, orden_por, Producto.nombre)
            if descendente:
                query = query.order_by(campo_orden.desc())
            else:
                query = query.order_by(campo_orden.asc())

            return query.all()
        except SQLAlchemyError as e:
            print(f"Error al obtener productos: {e}")
            return []

    def obtener_producto_por_nombre(self, nombre):
        session = self._get_session()
        try:
            return session.query(Producto).filter(Producto.nombre == nombre).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener producto: {e}")
            return None

    def obtener_producto_por_id(self, id_producto):
        session = self._get_session()
        try:
            return session.query(Producto).filter(Producto.id == id_producto).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener producto: {e}")
            return None

    def actualizar_producto(self, nombre_antiguo, nombre_nuevo=None, precio_nuevo=None,
                          categoria_nueva=None, stock_nuevo=None):
        session = self._get_session()
        try:
            producto = self.obtener_producto_por_nombre(nombre_antiguo)
            if producto:
                if nombre_nuevo is not None and nombre_nuevo.strip():
                    producto.nombre = nombre_nuevo
                if precio_nuevo is not None:
                    producto.precio = float(precio_nuevo)
                if categoria_nueva is not None:
                    producto.categoria = categoria_nueva
                if stock_nuevo is not None:
                    producto.stock = int(stock_nuevo)

                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al actualizar producto: {e}")
            return False

    def eliminar_producto(self, nombre):
        session = self._get_session()
        try:
            producto = self.obtener_producto_por_nombre(nombre)
            if producto:
                session.delete(producto)
                session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al eliminar producto: {e}")
            return False

    def buscar_productos(self, termino):
        session = self._get_session()
        try:
            return session.query(Producto).filter(
                (Producto.nombre.like(f'%{termino}%')) |
                (Producto.categoria.like(f'%{termino}%'))
            ).all()
        except SQLAlchemyError as e:
            print(f"Error al buscar productos: {e}")
            return []

    def cerrar(self):
        if self.session:
            self.session.close()
            self.session = None

