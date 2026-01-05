"""
Script para limpiar precios en la base de datos
Convierte precios con formato string a float
"""
from database.config import db_config
from database.models import Producto
from sqlalchemy.exc import SQLAlchemyError


def limpiar_precios():
    """Limpia y convierte todos los precios a formato numérico"""
    print("Inicializando base de datos...")
    db_config.init_db()
    session = db_config.get_session()
    print("Sesión creada...")

    try:
        productos = session.query(Producto).all()
        print(f"Se encontraron {len(productos)} productos")
        productos_actualizados = 0

        for producto in productos:
            print(f"\nAnalizando producto: {producto.nombre}")
            # Verificar si el precio es string o necesita limpieza
            precio_original = producto.precio
            print(f"  Precio original: {precio_original} (tipo: {type(precio_original).__name__})")

            # Si el precio es un string, limpiarlo
            if isinstance(precio_original, str):
                print(f"  -> Es string, limpiando...")
                # Remover símbolos y convertir formato europeo a número
                precio_str = str(precio_original).replace(' €', '').replace('€', '').strip()
                # Remover separadores de miles (.) y cambiar separador decimal (,) a punto
                precio_str = precio_str.replace('.', '').replace(',', '.')

                try:
                    precio_float = float(precio_str)
                    producto.precio = precio_float
                    productos_actualizados += 1
                    print(f"  ✓ Precio actualizado de '{precio_original}' a {precio_float}")
                except ValueError as e:
                    print(f"  ✗ Error al convertir precio: {e}")
            else:
                # Si ya es numérico, asegurarse que sea float
                print(f"  -> Ya es numérico")
                try:
                    producto.precio = float(precio_original)
                except (ValueError, TypeError) as e:
                    print(f"  ✗ Error al convertir precio: {e}")

        print("\nGuardando cambios...")
        session.commit()
        print(f"\n✓ Proceso completado. {productos_actualizados} productos actualizados.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"✗ Error al limpiar precios: {e}")
    finally:
        session.close()
        print("Sesión cerrada.")


if __name__ == "__main__":
    print("Iniciando limpieza de precios en la base de datos...")
    limpiar_precios()
    print("Limpieza finalizada.")

