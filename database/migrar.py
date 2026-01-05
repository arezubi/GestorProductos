"""
Script para migrar datos de la base de datos antigua a SQLAlchemy
"""
import sqlite3
from database.config import db_config
from database.repository import ProductoRepository


def migrar_datos():
    """Migra datos de la base de datos antigua si existe"""
    try:
        # Inicializar SQLAlchemy
        db_config.init_db()
        repo = ProductoRepository()

        # Conectar a la base de datos antigua
        conn = sqlite3.connect('database/productos.db')
        cursor = conn.cursor()

        # Verificar si hay datos para migrar
        cursor.execute("SELECT COUNT(*) FROM producto")
        count = cursor.fetchone()[0]

        if count == 0:
            print("No hay datos para migrar.")
            conn.close()
            return

        print(f"Encontrados {count} productos para verificar...")

        # Obtener todos los productos
        cursor.execute("SELECT nombre, precio, categoria, stock FROM producto")
        productos = cursor.fetchall()

        migrados = 0
        errores = 0

        for producto in productos:
            nombre, precio, categoria, stock = producto

            # Verificar si el producto ya existe
            producto_existente = repo.obtener_producto_por_nombre(nombre)

            if not producto_existente:
                # Crear el producto
                nuevo_producto = repo.crear_producto(
                    nombre=nombre,
                    precio=precio,
                    categoria=categoria if categoria else 'Sin categoría',
                    stock=stock if stock else 0
                )

                if nuevo_producto:
                    print(f"✓ Migrado: {nombre}")
                    migrados += 1
                else:
                    print(f"✗ Error al migrar: {nombre}")
                    errores += 1
            else:
                print(f"- Ya existe: {nombre}")

        conn.close()

        print("\n" + "="*50)
        print(f"Migración completada:")
        print(f"  - Productos migrados: {migrados}")
        print(f"  - Productos existentes: {count - migrados - errores}")
        print(f"  - Errores: {errores}")
        print("="*50)

    except sqlite3.OperationalError as e:
        print(f"Error: No se pudo acceder a la base de datos antigua: {e}")
    except Exception as e:
        print(f"Error durante la migración: {e}")


if __name__ == "__main__":
    print("Iniciando migración de datos...")
    migrar_datos()

