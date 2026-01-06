# Gestor de Productos

Aplicación de escritorio para gestión de productos con interfaz gráfica desarrollada en Python con Tkinter y SQLAlchemy.

## 📋 Características

- ✅ Agregar productos (nombre, precio, categoría, stock)
- ✅ Editar productos existentes
- ✅ Eliminar productos
- ✅ Listar productos con formato europeo de precios (1.000,00 €)
- ✅ Interfaz gráfica intuitiva con Tkinter
- ✅ Base de datos SQLite con SQLAlchemy ORM
- ✅ Soporte para cambiar a PostgreSQL, MySQL o SQL Server
- ✅ Mensajes de confirmación con código de colores (verde/rojo)

## 🔧 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/arezubi/GestorProductos.git
cd GestorProductos
```

### 2. Crear un entorno virtual (recomendado)

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecutar la aplicación

```bash
python app.py
```

## 🗄️ Estructura del Proyecto

```
GestorProductos/
├── app.py                      # Aplicación principal con interfaz gráfica
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── database/
│   ├── __init__.py            # Inicialización del paquete
│   ├── config.py              # Configuración de base de datos
│   ├── models.py              # Modelos ORM (Producto)
│   ├── repository.py          # Repositorio para operaciones CRUD
│   ├── limpiar_precios.py     # Script de limpieza de precios
│   ├── actualizar_db.py       # Script para actualizar estructura de BD
│   ├── migrar.py              # Script de migración de datos
│   ├── ejemplos_configuracion.py  # Ejemplos de configuración
│   └── productos.db           # Base de datos SQLite (se genera automáticamente)
├── recursos/
│   └── icono.ico              # Icono de la aplicación
└── test_precios.py            # Suite de pruebas para conversión de precios
```

## 💡 Características Técnicas

### Formato de Precios
La aplicación maneja precios en formato europeo:
- **Entrada**: Acepta varios formatos (300, 300,00, 3.000,00, 3.000,00 €)
- **Almacenamiento**: Float en base de datos
- **Visualización**: Formato europeo (3.000,00 €)

### Base de Datos
- **Por defecto**: SQLite (productos.db)
- **Soporta**: PostgreSQL, MySQL, SQL Server
- **ORM**: SQLAlchemy 2.0+

Para cambiar de base de datos, edita `database/config.py` y modifica la variable `DATABASE_URL`.

## 🛠️ Scripts Útiles

### Limpiar precios en la base de datos
```bash
python -c "from database.limpiar_precios import limpiar_precios; limpiar_precios()"
```

### Ejecutar pruebas de conversión de precios
```bash
python test_precios.py
```

## 📝 Notas

- La aplicación requiere **tkinter**, que viene incluido con Python en la mayoría de las instalaciones
- En macOS, si tkinter no está disponible, puede que necesites reinstalar Python desde python.org
- En Linux, puede que necesites instalar: `sudo apt-get install python3-tk`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Andrés Reyes (@arezubi)

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio de GitHub.

