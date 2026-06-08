# sensor-monitoring-api

API REST para la gestión de sensores industriales y su asignación a zonas de monitoreo. Permite registrar qué sensores están instalados en qué zonas de una planta industrial, con qué tipo de lectura operan, y hacer seguimiento de sus valores actuales frente a umbrales definidos.


## Stack

- Python 3.10+
- **FastAPI** — framework HTTP
- **SQLAlchemy** — ORM
- **psycopg2-binary** — driver PostgreSQL
- **Pydantic + pydantic-settings** — validación y configuración
- **Supabase** — base de datos PostgreSQL en la nube

## Estructura del proyecto

```
app/
├── main.py            # Entrada de la app, registro de routers
├── database.py        # Configuración SQLAlchemy y sesión DB
├── models/
│   ├── sensor.py      # Modelo Sensor
│   ├── zone.py        # Modelo Zone
│   └── monitoring.py  # Modelo Monitoring (tabla intermedia)
├── routers/
│   ├── sensors.py     # GET /sensors, GET /sensors/:id/zones
│   ├── zones.py       # GET /zones/:id/sensors
│   └── monitorings.py # GET, POST, PATCH /monitorings
└── schemas/
    ├── sensor.py
    ├── zone.py
    └── monitoring.py
schema.sql             # DDL completo + datos de prueba
```

## Reproducción local

### 1. Clonar y crear entorno virtual

```bash
git clone <repo-url>
cd sensor-monitoring-api

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con las credenciales de Supabase o PostgreSQL local:

```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
CORS_ORIGINS=http://localhost:5173
```

`CORS_ORIGINS` acepta múltiples orígenes separados por coma. Si se omite, usa `http://localhost:5173` por defecto.

En caso de utilizar Supabase y tener problemas de conexión por el método direct, se recomienda usar el Connection Session Pooler.

> **Importante:** el connection pooler de Supabase requiere el usuario en formato `postgres.PROJECT_REF`, no simplemente `postgres`. Copiar la cadena desde Supabase.

### 3. Inicializar la base de datos

SQL Editor, ejecutar el contenido completo de `schema.sql`. Esto crea las tres tablas, los índices, el trigger de `updated_at` y carga 12 monitoreos de prueba con 6 sensores y 5 zonas.

### 4. Levantar el servidor

```bash
uvicorn app.main:app --reload
```

### 5. Verificar

- API raíz: [http://localhost:8000](http://localhost:8000)
- Docs interactivos (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints

### Sensors

| Método | Ruta                    | Descripción                         |
|--------|-------------------------|-------------------------------------|
| GET    | `/sensors`              | Lista todos los sensores            |
| GET    | `/sensors/{id}/zones`   | Zonas donde está instalado el sensor |

### Zones

| Método | Ruta                    | Descripción                              |
|--------|-------------------------|------------------------------------------|
| GET    | `/zones`                | Lista todas las zonas                    |
| GET    | `/zones/{id}/sensors`   | Sensores activos en una zona             |

### Monitorings

| Método | Ruta                    | Descripción                                            |
|--------|-------------------------|--------------------------------------------------------|
| GET    | `/monitorings`          | Lista monitoreos; filtros opcionales `?status=activo\|pausado`, `?zone_id={id}` |
| POST   | `/monitorings`          | Crea un monitoreo (valida sensor, zona y duplicados)   |
| PATCH  | `/monitorings/{id}`     | Actualiza `valor_umbral`, `valor_actual` o `estado_monitoreo` |

---

## Modelo de datos

### sensors

| Campo               | Tipo         | Valores permitidos                             |
|---------------------|--------------|------------------------------------------------|
| `id`                | BIGINT PK    |                                                |
| `nombre`            | VARCHAR(120) |                                                |
| `tipo`              | VARCHAR(20)  | `temperatura`, `presion`, `vibracion`, `flujo` |
| `fabricante`        | VARCHAR(120) |                                                |
| `fecha_fabricacion` | DATE         |                                                |
| `created_at`        | TIMESTAMPTZ  |                                                |

### zones

| Campo              | Tipo         | Valores permitidos                              |
|--------------------|--------------|--------------------------------------------------|
| `id`               | BIGINT PK    |                                                  |
| `nombre`           | VARCHAR(120) |                                                  |
| `descripcion`      | TEXT         |                                                  |
| `ubicacion`        | VARCHAR(150) |                                                  |
| `estado_operativo` | VARCHAR(20)  | `operativa`, `mantenimiento`, `inactiva`         |
| `created_at`       | TIMESTAMPTZ  |                                                  |

### monitorings

| Campo               | Tipo          | Notas                                          |
|---------------------|---------------|------------------------------------------------|
| `id`                | BIGINT PK     |                                                |
| `sensor_id`         | BIGINT FK     | → `sensors.id` ON DELETE CASCADE               |
| `zone_id`           | BIGINT FK     | → `zones.id` ON DELETE CASCADE                 |
| `fecha_instalacion` | DATE          |                                                |
| `tipo_lectura`      | VARCHAR(20)   | `temperatura`, `presion`, `vibracion`, `flujo` |
| `valor_umbral`      | NUMERIC(12,2) |                                                |
| `valor_actual`      | NUMERIC(12,2) | Nullable                                       |
| `estado_monitoreo`  | VARCHAR(20)   | `activo`, `pausado`                            |
| `created_at`        | TIMESTAMPTZ   |                                                |
| `updated_at`        | TIMESTAMPTZ   | Auto-actualizado por trigger                   |

Restricción única: `(sensor_id, zone_id, tipo_lectura)` — un sensor no puede tener dos monitoreos del mismo tipo en la misma zona.
