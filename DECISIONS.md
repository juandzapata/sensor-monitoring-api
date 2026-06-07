# DECISIONS.md
---

## 1. ¿Cómo modelaste la relación entre sensores y zonas y por qué?

Como el ejercicio bien especificaba, contabamos con una relación muchos-a-muchos. 
Para esto se decidió modelar mediante tres tablas: `sensors`,
`zones` y una tabla intermedia `monitorings`.

`monitorings` no es una simple tabla intermedia, sino una **entidad asociativa**:
la asignación de un sensor a una zona posee información propia (fecha de
instalación, tipo de lectura, valor umbral y estado del monitoreo). Por eso
tiene clave primaria propia y se expone como un recurso independiente en la API.
Con la tabla monitorings podemos tener una mejor trazabilidad de todo el sistema.

---

## 2. ¿Qué validación o restricción consideras más importante y por qué?

Una restricción que me pareció bastante importante, fue la restricción realizada
en la base de datos. Más específicamente `UNIQUE(sensor_id, zone_id, tipo_lecutra)`.

Es importante dado que con el modelo que tenemos actualmente, no tiene sentido que 
existan dos sensores del mismo tipo, en la misma zona al tiempo. Esto se traduciría
como información duplicada. 

Adicionalmente, decidí que esta restricción esté presente en el `schema.sql` debido a 
que esta es nuestra fuente de verdad. Se protege la integridad del en sus capas más críticas.



[Tu respuesta. Pista de lo que decidimos: la restricción
`UNIQUE(sensor_id, zone_id, tipo_lectura)`. Explica qué problema evita y qué
pasaría en los datos si no existiera.]

---

## 3. ¿Cómo organizaste la estructura de tu backend y por qué elegiste esa organización?

El backend se organizó en capas con responsabilidades separadas:

- `models/` — modelos SQLAlchemy que mapean las tablas.
- `schemas/` — esquemas Pydantic para validación de entrada y serialización
  de salida (cumplen el rol de los tipos/interfaces que pide la prueba).
- `routers/` — definición de endpoints agrupados por recurso.
- `database.py` — configuración de la conexión y sesión.

La intención con la que se aplicó esta estructura para los directorios del programa se basa 
en que desacoplar las responsabilidades de cada parte del sistema. Se tienen apartados
específicos para las el código que se encarga de las peticiones HTTP, modelos de la base y 
schemas para validación de datos.

---

## 4. Si tuvieras un día adicional, ¿qué mejorarías primero y por qué?

Si tuviera un día adicional, lo dedicaría principalmente a fortalecer el apartado de seguridad del backend, que en esta versión quedó deliberadamente mínimo para priorizar la funcionalidad central y la reproducibilidad del proyecto.
Lo primero para cumplir con los críterios anteriores, sería implementar autenticación con un sistema de login y segregación de usuarios por roles. En un sistema real esto es relevante porque no todos los perfiles deberían tener los mismos permisos. Un operario podría consultar el estado de los sensores, pero modificar un valor umbral o pausar un monitoreo debería estar restringido a un supervisor. También me gustaría añadir un sistema logs, para mantener la trazibilidad de toda la operación.
En el frontend, me enfocaría en mejorar la experiencia de usuario. La interfaz actual cumple los requisitos funcionales pero por la naturalidad del problema, tiende a ser simple. Con más tiempo e información trabajaría en aspectos como retroalimentación visual más clara al crear o actualizar monitoreos, estados de carga y error más pulidos, y una presentación más enfocada en general.
Priorizaría la seguridad sobre la estética porque considero que es la carencia más crítica de cara a un uso real: una interfaz sencilla sigue siendo usable, pero un sistema sin control de acceso no sería viable en un entorno industrial.

---

## Decisiones adicionales

- **`schema.sql` como fuente de verdad del esquema**
- **Supabase solo para gestionar PostgreSQL**