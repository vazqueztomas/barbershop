# Barbershop Management System

Una aplicación completa para la gestión de barberías, desarrollada con Python, FastAPI y Tkinter. Este sistema permite registrar cortes de cabello, gestionar clientes, visualizar estadísticas y mantener un historial completo de las operaciones.

## 🚀 Características

### Funcionalidades Principales
- **Registro de Cortes**: Sistema completo para registrar nuevos cortes de cabello con información del cliente, tipo de corte, precio y fecha
- **Gestión de Clientes**: Mantenimiento de base de datos de clientes y su historial de cortes
- **Tipos de Servicio**: Soporte para diferentes tipos de cortes (pelo, barba, pelo y barba)
- **Historial Completo**: Visualización y filtrado del historial de cortes por fecha y tipo
- **Eliminación de Registros**: Funcionalidad para eliminar cortes registrados
- **Estadísticas en Tiempo Real**: Visualización de ingresos totales y número de cortes realizados

### Arquitectura
- **Backend API**: REST API construida con FastAPI para la gestión de datos
- **Base de Datos**: MongoDB con Motor para operaciones asíncronas
- **Interfaz Gráfica**: Aplicación de escritorio con Tkinter y CustomTkinter
- **Validación de Datos**: Pydantic para la validación y serialización de datos
- **Testing**: Suite de pruebas con pytest

## 📋 Requisitos del Sistema

- **Python**: 3.13 o superior
- **MongoDB**: Base de datos MongoDB (local o en la nube)
- **Sistema Operativo**: Windows, macOS o Linux

## 🛠️ Instalación

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd barbershop
```

### 2. Configurar Entorno Virtual
```bash
# Usando pipenv (recomendado)
pipenv install
pipenv shell

# O usando venv tradicional
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
MONGODB_URL="mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
```

### 4. Instalar Dependencias de Desarrollo
```bash
pipenv install --dev
```

## 🚀 Ejecución

### Opción 1: Usando los Scripts de Pipenv
```bash
# Iniciar la aplicación de escritorio
pipenv run start

# Iniciar el servidor API
pipenv run start-server

# Formatear y lintear el código
pipenv run format
```

### Opción 2: Ejecución Manual
```bash
# Iniciar el servidor FastAPI
uvicorn barbershop.app:app --reload

# Iniciar la aplicación Tkinter (en otra terminal)
python -m barbershop.gui.main
```

### Opción 3: Usando Python Directamente
```bash
# Servidor API
python -m barbershop.app

# Aplicación GUI
python -m barbershop.gui.main
```

## 📁 Estructura del Proyecto

```
barbershop/
├── barbershop/                 # Paquete principal
│   ├── __init__.py
│   ├── app.py                  # Aplicación FastAPI
│   ├── gui/                    # Interfaz gráfica
│   │   ├── __init__.py
│   │   ├── main.py            # Ventana principal
│   │   ├── constants.py       # Constantes de la GUI
│   │   ├── haircut_registration.py
│   │   ├── show_historico.py
│   │   ├── update_information_in_display.py
│   │   └── utils/             # Utilidades de la GUI
│   │       ├── __init__.py
│   │       ├── generate_label.py
│   │       └── update_treeview.py
│   ├── models/                 # Modelos de datos
│   │   ├── __init__.py
│   │   └── haircut.py
│   ├── routes/                 # Rutas de la API
│   │   ├── __init__.py
│   │   └── haircuts.py
│   └── database/               # Conexión a la base de datos
│       ├── __init__.py
│       └── database.py
├── tests/                      # Pruebas
│   ├── api/
│   │   └── haircuts/
│   │       ├── conftest.py
│   │       └── test_haircuts.py
│   └── utils/
│       ├── __init__.py
│       └── test_functions.py
├── .env                        # Variables de entorno
├── .gitignore
├── .pre-commit-config.yaml
├── Pipfile                     # Dependencias de Pipenv
├── Pipfile.lock
├── pyproject.toml             # Configuración del proyecto
├── README.md
└── TODO.md                     # Tareas pendientes
```

## 🔧 Configuración

### Base de Datos MongoDB
La aplicación utiliza MongoDB para almacenar los datos. Asegúrate de:

1. Tener una instancia de MongoDB corriendo (local o en la nube)
2. Configurar la URL de conexión en el archivo `.env`
3. La base de datos se creará automáticamente en el primer uso

### Configuración de Linting y Formateo
El proyecto incluye configuración para:
- **Ruff**: Formateo y linting rápido
- **Pylint**: Análisis estático detallado
- **Pre-commit**: Hooks de git para asegurar la calidad del código

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Usando pytest
pytest

# Usando pipenv
pipenv run pytest

# Con cobertura
pytest --cov=barbershop
```

### Estructura de Pruebas
- **Tests de API**: Pruebas para los endpoints de FastAPI
- **Tests de Utilidades**: Pruebas para funciones auxiliares
- **Tests de Integración**: Pruebas de flujo completo

## 📊 API Endpoints

### Haircuts
- `GET /` - Estado de la API
- `GET /haircuts/` - Obtener todos los cortes
- `GET /haircuts/{haircut_id}` - Obtener un corte específico
- `POST /haircuts/` - Crear un nuevo corte
- `DELETE /haircuts/{haircut_id}` - Eliminar un corte

### Documentación de la API
Una vez iniciado el servidor, puedes acceder a:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🎨 Interfaz de Usuario

### Pestañas Principales
1. **Registro**: Formulario para registrar nuevos cortes
2. **Gráficos**: Visualización de estadísticas (en desarrollo)

### Funcionalidades de la GUI
- Formulario de registro con validación
- Calendario para selección de fechas
- Radio buttons para tipo de corte
- Tabla con historial de cortes
- Botones para eliminar y ver historial
- Estadísticas en tiempo real

## 🔮 Roadmap (Ver TODO.md)

### Base de Datos
- [x] Conexión a MongoDB
- [x] Migración de CSV a base de datos
- [ ] Creación de usuarios admin
- [ ] Testing de conexión a base de datos

### Mejoras de UI/UX
- [ ] Mejorar estilos de botones y formularios
- [ ] Reorganizar etiquetas y componentes
- [ ] Solución para pestañas en Tkinter
- [ ] Filtros con lógica correcta

### Funcionalidades Avanzadas
- [ ] Integración con IA para mejoras
- [ ] Gráficos con matplotlib
- [ ] Integración con MercadoPago
- [ ] Sistema de citas y reservas

## 🤝 Contribución

1. Fork del repositorio
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

### Guía de Estilo
- Seguir la configuración de Ruff y Pylint
- Usar type hints en todo el código
- Escribir pruebas para nuevas funcionalidades
- Documentar cambios importantes

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🐛 Issues y Soporte

Si encuentras algún bug o necesitas soporte:
1. Revisa la sección de [Issues](../../issues) existentes
2. Crea un nuevo issue describiendo el problema
3. Incluye capturas de pantalla si es posible
4. Proporciona información del entorno (Python, OS, etc.)

## 📈 Estadísticas del Proyecto

- **Lenguaje**: Python
- **Framework Backend**: FastAPI
- **Framework Frontend**: Tkinter + CustomTkinter
- **Base de Datos**: MongoDB
- **Testing**: pytest
- **Calidad de Código**: Ruff, Pylint, Pre-commit

---

**Desarrollado con ❤️ para la comunidad de barberías**