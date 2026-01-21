# Barbershop Management System

Una aplicación completa y moderna para la gestión de barberías, desarrollada con arquitectura full-stack. Este sistema permite registrar cortes de cabello, gestionar clientes, visualizar estadísticas avanzadas y mantener un historial completo de las operaciones con interfaces tanto de escritorio como web.

## 🚀 Características

### Funcionalidades Principales
- **Registro de Cortes**: Sistema completo para registrar nuevos cortes de cabello con información del cliente, tipo de corte, precio y fecha
- **Gestión de Clientes**: Mantenimiento de base de datos de clientes y su historial de cortes
- **Tipos de Servicio**: Soporte para diferentes tipos de cortes (pelo, barba, pelo y barba)
- **Historial Completo**: Visualización y filtrado avanzado del historial de cortes por fecha y tipo
- **Eliminación de Registros**: Funcionalidad para eliminar cortes individuales o por fecha
- **Estadísticas en Tiempo Real**: Dashboard completo con gráficos interactivos y métricas avanzadas
- **Edición de Precios**: Funcionalidad para actualizar precios de cortes existentes
- **Exportación de Datos**: Exportar historial y datos a formato Excel

El frontend se encuentra en un repositorio separado: [barbershop-frontend](https://github.com/tu-usuario/barbershop-frontend)

### Arquitectura
- **Backend API**: REST API construida con FastAPI y validación con Pydantic
- **Base de Datos**: SQLite ligera y eficiente con repositorios estructurados
- **Frontend Web**: React 18 + TypeScript + Vite con gráficos Recharts
- **Interfaz de Escritorio**: Tkinter y CustomTkinter para aplicación nativa
- **Testing**: Suite completa de pruebas con pytest y Vitest
- **Calidad de Código**: Configuración con Ruff, Pylint y pre-commit hooks

## 📋 Requisitos del Sistema

### Backend
- **Python**: 3.8 o superior
- **Poetry**: Gestor de dependencias de Python
- **SQLite**: Base de datos (incluida por defecto)

### Frontend Web
- **Node.js**: 18 o superior
- **npm**: Gestor de paquetes de Node.js

### Sistema Operativo
- **Windows**, **macOS** o **Linux**

## 🛠️ Instalación

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd barbershop
```

### 2. Instalar Backend (Python + Poetry)
```bash
# Instalar Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias del backend
poetry install

# Activar entorno virtual
poetry shell
```

### Frontend Web
El frontend está en un repositorio separado. Para instalarlo:
```bash
cd ../barbershop-frontend
npm install
```

### 4. Configurar Variables de Entorno (Opcional)
Crea un archivo `.env` en la raíz del proyecto para configuración personalizada:
```env
# Configuración de la base de datos (SQLite por defecto)
DATABASE_URL="sqlite:///barbershop.db"

# Configuración del servidor
HOST="127.0.0.1"
PORT="8000"
```

## 🚀 Ejecución

### Opción 1: Ejecución Completa (Recomendado)
```bash
# Terminal 1: Iniciar el servidor API
poetry run uvicorn barbershop.app:app --reload

# Terminal 2: Iniciar el frontend web
cd ../barbershop-frontend
npm run dev

# Terminal 3: Iniciar la aplicación de escritorio (opcional)
poetry run python -m barbershop.gui.main
```

### Opción 2: Solo Backend + Escritorio
```bash
# Iniciar el servidor API
poetry run uvicorn barbershop.app:app --reload

# En otra terminal, iniciar la aplicación de escritorio
poetry run python -m barbershop.gui.main
```

### Opción 3: Solo Frontend Web (con API corriendo)
```bash
# Asegúrate que el backend está corriendo en http://127.0.0.1:8000
cd ../barbershop-frontend
npm run dev
```

### URLs de Acceso
- **API REST**: `http://127.0.0.1:8000`
- **Documentación API (Swagger)**: `http://127.0.0.1:8000/docs`
- **Frontend Web**: `http://localhost:3000`
- **Aplicación de Escritorio**: Ventana nativa

## 📁 Estructura del Proyecto

```
barbershop/
├── barbershop/                 # Paquete principal del backend
│   ├── __init__.py
│   ├── app.py                  # Aplicación FastAPI principal
│   ├── main.py                 # Punto de entrada
│   ├── gui/                    # Interfaz gráfica de escritorio
│   │   ├── __init__.py
│   │   ├── main.py            # Ventana principal de la GUI
│   │   ├── constants.py       # Constantes y configuración
│   │   ├── haircut_registration.py
│   │   ├── show_historico.py
│   │   ├── read_register.py
│   │   ├── update_information_in_display.py
│   │   └── utils/             # Utilidades de la GUI
│   │       ├── __init__.py
│   │       ├── generate_label.py
│   │       └── update_tree_view.py
│   ├── models/                 # Modelos de datos Pydantic
│   │   ├── __init__.py
│   │   └── haircut.py
│   ├── routes/                 # Rutas de la API REST
│   │   ├── __init__.py
│   │   └── haircuts.py
│   ├── repositories/           # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── haircuts.py
│   │   └── handler_errors.py
│   └── database/               # Conexión a la base de datos
│       ├── __init__.py
│       └── create_connection.py
├── tests/                      # Suite de pruebas completa
│   ├── api/                    # Tests de API
│   ├── core/                   # Tests de lógica de negocio
│   ├── database/               # Tests de base de datos
│   └── desktop/                # Tests de aplicación de escritorio
├── .env                        # Variables de entorno
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml             # Configuración de Poetry y proyecto
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

### Backend Tests
```bash
# Ejecutar todas las pruebas del backend
poetry run pytest

# Con cobertura de código
poetry run pytest --cov=barbershop

# Ejecutar pruebas específicas
poetry run pytest tests/api/
poetry run pytest tests/database/
poetry run pytest tests/core/
```

### Frontend Tests
El frontend está en un repositorio separado. Para ejecutar los tests:
```bash
cd ../barbershop-frontend
npm run test
```

### Estructura de Pruebas
- **Tests de API**: Pruebas para los endpoints de FastAPI
- **Tests de Base de Datos**: Pruebas de repositorios y conexión
- **Tests de Lógica de Negocio**: Pruebas de funciones core
- **Tests de Escritorio**: Pruebas de la aplicación de escritorio

## 📊 API Endpoints

### Haircuts
- `GET /` - Estado de la API
- `GET /haircuts/` - Obtener todos los cortes
- `GET /haircuts/{haircut_id}` - Obtener un corte específico
- `POST /haircuts/` - Crear un nuevo corte
- `PUT /haircuts/{haircut_id}` - Actualizar un corte existente
- `PATCH /haircuts/{haircut_id}/price` - Actualizar precio de un corte
- `DELETE /haircuts/{haircut_id}` - Eliminar un corte específico
- `DELETE /haircuts/date/{date}` - Eliminar cortes por fecha
- `GET /haircuts/date/{date}` - Obtener cortes por fecha específica
- `GET /haircuts/summary/daily` - Obtener resumen diario de ingresos

### Documentación de la API
Una vez iniciado el servidor, puedes acceder a:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`

## 🎨 Interfaz de Usuario

### Interfaz Web (React)
La interfaz web se encuentra en el repositorio [barbershop-frontend](https://github.com/tu-usuario/barbershop-frontend) e incluye:
- **Dashboard Principal**: Vista completa con estadísticas y acciones rápidas
- **Gestión de Cortes**: Formulario intuitivo para crear, editar y eliminar cortes
- **Panel de Estadísticas**: Gráficos interactivos con Recharts
  - Gráfico de área: Ingresos de los últimos 7 días
  - Gráfico de barras: Cortes por día de la semana
  - Gráfico circular: Distribución por tipo de servicio
  - Gráfico de línea: Tendencia mensual
- **Tabla de Historial**: Listado completo con opciones de filtrado y búsqueda
- **Exportación de Datos**: Descargar historial en formato Excel

### Interfaz de Escritorio (Tkinter)
La aplicación nativa incluye:
- **Registro de Cortes**: Formulario con validación en tiempo real
- **Historial Completo**: Tabla con filtrado por fecha y tipo
- **Edición de Precios**: Funcionalidad para actualizar precios existentes
- **Estadísticas en Tiempo Real**: Métricas actualizadas instantáneamente
- **Calendario Integrado**: Selección visual de fechas
- **Eliminación Masiva**: Opción para eliminar cortes por fecha

### Características Compartidas
- Validación de datos en tiempo real
- Sincronización automática con la base de datos
- Interfaz responsive y accesible
- Manejo robusto de errores

## 🔮 Roadmap (Ver TODO.md)

### ✅ Recientemente Completado
- [x] Migración de MongoDB a SQLite para mayor simplicidad
- [x] Implementación de arquitectura de repositorios
- [x] Desarrollo completo de frontend React + TypeScript
- [x] Adición de gráficos interactivos con Recharts
- [x] Configuración de Poetry para gestión de dependencias
- [x] Suite completa de pruebas con pytest y Vitest

### En Progreso
- [ ] Sistema de autenticación y usuarios admin
- [ ] Mejoras en la interfaz de escritorio
- [ ] Optimización de consultas a base de datos

### Próximamente
- [ ] Integración con MercadoPago para pagos
- [ ] Sistema de citas y reservas online
- [ ] Dashboard avanzado con métricas en tiempo real
- [ ] Aplicación móvil (React Native)
- [ ] Integración con calendarios externos (Google Calendar)
- [ ] Sistema de notificaciones por email/SMS

### Mejoras Técnicas
- [ ] Implementación de WebSocket para actualizaciones en tiempo real
- [ ] Caching con Redis para mejor rendimiento
- [ ] Dockerización para despliegue simplificado
- [ ] CI/CD pipeline automatizado

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

### Backend
- **Lenguaje**: Python 3.8+
- **Framework**: FastAPI con Pydantic
- **Base de Datos**: SQLite con arquitectura de repositorios
- **Testing**: pytest con cobertura de código
- **Calidad de Código**: Ruff, Pylint, Pre-commit hooks

### Frontend
El frontend se encuentra en un repositorio separado: [barbershop-frontend](https://github.com/tu-usuario/barbershop-frontend)

### DevOps
- **Gestión de Dependencias**: Poetry (Python), npm (Node.js)
- **Control de Versiones**: Git con hooks pre-commit
- **Calidad**: Linting automático y formateo de código
- **Testing**: Suite completa con integración continua

---

**Desarrollado con ❤️ para la comunidad de barberías**