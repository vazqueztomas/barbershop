# Barbershop Frontend

Frontend web para el sistema de gestión de barbería, construido con React + TypeScript + Vite.

## Estructura

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx    # Componente principal
│   │   ├── HaircutForm.tsx  # Formulario para crear/editar
│   │   └── HaircutList.tsx  # Tabla de haircuts
│   ├── hooks/
│   │   └── useHaircuts.ts   # Hook personalizado para API
│   ├── services/
│   │   └── haircutService.ts # Servicio de API
│   ├── types/
│   │   └── index.ts         # Tipos TypeScript
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Instalación

```bash
cd frontend
npm install
```

## Desarrollo

```bash
npm run dev
```

El servidor de desarrollo corre en `http://localhost:3000` y proxyifica las peticiones `/haircuts` al backend en `http://localhost:8000`.

## Construcción

```bash
npm run build
```

## Características

- Listado de cortes de cabello
- Crear nuevos cortes
- Editar cortes existentes
- Eliminar cortes
- Interfaz responsive
- Manejo de errores
