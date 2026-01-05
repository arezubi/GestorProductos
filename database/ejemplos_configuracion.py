"""
Ejemplo de cómo configurar diferentes bases de datos
"""

# =====================================
# EJEMPLO 1: SQLite (Por defecto)
# =====================================
# No necesitas cambiar nada, funciona automáticamente
# La base de datos se crea en: database/productos.db


# =====================================
# EJEMPLO 2: PostgreSQL
# =====================================
# 1. Instalar el driver:
#    pip install psycopg2-binary
#
# 2. Crear la base de datos en PostgreSQL:
#    CREATE DATABASE gestor_productos;
#
# 3. Modificar database/config.py:
#    DATABASE_URL = 'postgresql://usuario:contraseña@localhost:5432/gestor_productos'
#
# 4. Ejecutar la aplicación (se crearán las tablas automáticamente)


# =====================================
# EJEMPLO 3: MySQL
# =====================================
# 1. Instalar el driver:
#    pip install pymysql
#
# 2. Crear la base de datos en MySQL:
#    CREATE DATABASE gestor_productos;
#
# 3. Modificar database/config.py:
#    DATABASE_URL = 'mysql+pymysql://usuario:contraseña@localhost:3306/gestor_productos'
#
# 4. Ejecutar la aplicación (se crearán las tablas automáticamente)


# =====================================
# EJEMPLO 4: SQL Server
# =====================================
# 1. Instalar el driver:
#    pip install pyodbc
#
# 2. Crear la base de datos en SQL Server:
#    CREATE DATABASE gestor_productos;
#
# 3. Modificar database/config.py:
#    DATABASE_URL = 'mssql+pyodbc://usuario:contraseña@servidor/gestor_productos?driver=ODBC+Driver+17+for+SQL+Server'
#
# 4. Ejecutar la aplicación (se crearán las tablas automáticamente)


# =====================================
# EJEMPLO 5: Usar variables de entorno
# =====================================
# 1. Instalar python-dotenv:
#    pip install python-dotenv
#
# 2. Crear archivo .env:
#    DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/gestor_productos
#
# 3. Modificar database/config.py para cargar el .env:
#    from dotenv import load_dotenv
#    load_dotenv()
#    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/productos.db')


# =====================================
# VENTAJAS DE SQLALCHEMY
# =====================================
# ✅ Cambio de base de datos sin modificar código de la aplicación
# ✅ Protección contra inyección SQL automática
# ✅ Manejo de transacciones y sesiones
# ✅ Consultas más legibles y mantenibles
# ✅ Migraciones de esquema más fáciles
# ✅ Soporte para múltiples bases de datos simultáneas

