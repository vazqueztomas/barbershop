# Barbershop Management System

Una aplicación de escritorio para gestionar una barbería con interfaz gráfica y API backend.

## Arquitectura

- **Frontend**: Interfaz gráfica con Tkinter y CustomTkinter
- **Backend**: API REST con FastAPI
- **Base de datos**: MongoDB

## Estructura del Proyecto

```
barbershop/
├── app.py                 # Aplicación FastAPI principal
├── gui/                   # Interfaz gráfica
│   ├── main.py           # Ventana principal
│   ├── constants.py      # Configuración GUI
│   ├── haircut_registration.py
│   ├── show_historico.py
│   ├── update_information_in_display.py
│   └── utils/            # Utilidades GUI
├── routes/               # Rutas API
│   └── haircuts.py       # Endpoints de cortes
├── models/               # Modelos de datos
│   └── haircut.py        # Modelo Haircut
└── database/             # Configuración DB
    └── database.py       # Conexión MongoDB
```

## Funcionalidades

- **Registro de cortes**: Clientes, tipo de corte, precio, fecha
- **Tipos de servicio**: Pelo, barba, pelo y barba
- **Historial**: Visualización y eliminación de registros
- **Estadísticas**: Total ganado y cortes realizados
- **API REST**: CRUD completo para cortes

## Instalación

```bash
pip install fastapi uvicorn pymongo python-dotenv tkinter customtkinter tkcalendar requests
```

## Ejecución

1. Iniciar servidor API:
```bash
uvicorn barbershop.app:app --reload
```

2. Iniciar interfaz gráfica:
```bash
python -m barbershop.gui.main
```

## Variables de Entorno

Crear `.env` con:
```
MONGODB_URL=mongodb://localhost:27017/
```

## Endpoints API

- `GET /` - Estado API
- `GET /haircuts/` - Listar todos los cortes
- `POST /haircuts/` - Crear nuevo corte
- `DELETE /haircuts/{id}` - Eliminar corte