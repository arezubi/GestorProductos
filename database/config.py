"""
Configuración de la base de datos usando SQLAlchemy
Permite cambiar fácilmente entre diferentes sistemas de bases de datos
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.models import Base
import os


class DatabaseConfig:
    """Configuración centralizada de la base de datos"""

    # Puedes cambiar esta URL para usar diferentes bases de datos:
    # SQLite: sqlite:///ruta/al/archivo.db
    # PostgreSQL: postgresql://usuario:contraseña@localhost/nombre_db
    # MySQL: mysql+pymysql://usuario:contraseña@localhost/nombre_db
    # SQL Server: mssql+pyodbc://usuario:contraseña@servidor/nombre_db

    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/productos.db')

    def __init__(self):
        self.engine = None
        self.Session = None

    def init_db(self):
        """Inicializa la conexión a la base de datos"""
        self.engine = create_engine(
            self.DATABASE_URL,
            echo=False,  # Cambia a True para ver las consultas SQL en consola
            pool_pre_ping=True,  # Verifica la conexión antes de usarla
            connect_args={'check_same_thread': False} if 'sqlite' in self.DATABASE_URL else {}
        )

        # Crear todas las tablas si no existen
        Base.metadata.create_all(self.engine)

        # Configurar la sesión
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)

        return self.Session

    def get_session(self):
        """Obtiene una nueva sesión de base de datos"""
        if self.Session is None:
            self.init_db()
        return self.Session()

    def close_session(self, session):
        """Cierra una sesión de base de datos"""
        if session:
            session.close()


# Instancia global de configuración
db_config = DatabaseConfig()

