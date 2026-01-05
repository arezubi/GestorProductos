import sqlite3


def agregar_columna_stock():
    try:
        conn = sqlite3.connect('database/productos.db')
        cursor = conn.cursor()

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(producto)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if 'stock' not in columnas:
            cursor.execute("ALTER TABLE producto ADD COLUMN stock INTEGER DEFAULT 0")
            conn.commit()
            print("Columna 'stock' agregada exitosamente")
        else:
            print("La columna 'stock' ya existe")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    agregar_columna_stock()