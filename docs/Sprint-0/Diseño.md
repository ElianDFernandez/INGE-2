# Documento de Diseño Tecnico (TDD)

## Introducción
Este documento describe la planificacion y el diseño tecnico del sistema para el centro de actividades deportivas. Se detalla:
* Planificación de sprints y asignación de puntos a las historias de usuario
* La arquitectura del sistema
* Las tecnologías a utilizar
* El diseño de la base de datos
* Los diagramas de clases

## Planificación de Sprints y Asignación de Puntos
Se han identificado un total de 120 puntos distribuidos en 2 sprints.

* **Sprint 1:** Core del Sistema y ABMs Funcionales (60 puntos):
    - **Gestión de Usuarios (12 puntos)**
    3- Registrar socio = 5
    9- Iniciar Sesion = 2
    10- Cerrar sesion = 1
    11- Recuperar contraseña = 2
    13- Ver perfil de usuario = 1
    14- Editar perfil de usuario = 1
    - **Gestión de Empleados (8 puntos)**
    29- Registrar empleado = 3
    30- Modificar datos de empleado = 1
    31- Dar de baja empleado = 1
    32- Consultar actividades asignadas a un empleado = 1
    33- Asignar actividad a un empleado = 1
    34- Eliminar actividad asignada a un empleado = 1
    - **Gestión de Actividades y Turnos (16 puntos)**
    57- Crear actividad = 2
    58- Modificar actividad = 1
    59- Eliminar actividad = 1
    51- Crear turno de una actividad = 3
    52- Modificar turno de una actividad = 5
    53- Consultar turno de una actividad = 1
    54- Eliminar turno de una actividad = 3
    - **Flujo Principal del Socio (19 puntos)**
    18- Consultar turnos de actividades disponibles = 3
    42- Inscribirse a actividad en un turno específico = 3
    43- Reservar clases individuales = 3
    17- Consultar mis actividades y clases reservadas = 2
    21- Cancelar reserva a actividad = 8
    - **Operativa Básica (5 puntos)**
    16- Registrar asistencia manual = 2
    27- Registrar cobro manual = 3

* **Sprint 2:** Automatización, Pagos y Lógica Compleja (60 puntos):
  - **Tecnología QR (11 puntos)**
    56- Generar QR = 8
    15- Registrar asistencia con QR = 3
  - **Gestión Avanzada de Pagos (15 puntos)**
    26- Abonar seña = 8
    28- Registrar pago = 5
    22- Consultar mi crédito disponible = 2
  - **Listas de Espera y Notificaciones (11 puntos)**
    19- Entrar en lista de espera = 2
    20- Cancelar anotación en lista de espera = 1
    44- Notificar a socios en lista de espera sobre disponibilidad = 3
    45- Confirmación de asistencia por lista de espera = 2
    47- Notificar a socios sobre recordatorios de pago = 2
    55- Notificar a socios sobre confirmación de reservas = 1
  - **Métricas y Ajustes Finales (11 puntos)**
    60- Consultar métricas = 5
    23- Cancelar reserva a clase individual = 5
    12- Modificar contraseña = 1

## Arquitectura del Sistema
Como estaremos usando DJango, seguiremos su arquitectura MVT (Model-View-Template) que se adapta bien a las necesidades del proyecto.

````
💡 Nota Aclaratoria para el Equipo: 
**MVT**
- **Model (Modelo):** Define datos y reglas asociadas, representa la estructura de la base de datos.
- **View (Vista):** Contiene la lógica de negocio, procesa solicitudes y devuelve respuestas.
- **Template (Plantilla):** Define la presentación de los datos, es la interfaz de usuario.

En MVC el flujo es: Usuario -> Controlador -> Modelo -> Base de Datos -> Modelo -> Controlador -> Vista -> Usuario
En MVT el flujo es: Usuario -> URL -> Vista -> Modelo -> Base de Datos -> Modelo -> Vista -> Template -> Usuario
````
## Tecnologías a Utilizar
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript (con Django Templates)
- **Base de Datos:** SQLlite (para desarrollo)
- **Control de Versiones:** Git y GitHub
- **Herramientas de Gestión de Proyectos:** Taiga

## Diseño de la Base de Datos
Diagrma entidad-relación (ER) usando extension Mermaid para visualizar las tablas y sus relaciones.

````mermaid
---
config:
  layout: elk
---
erDiagram
    Usuarios {
        int id PK
        string nombre
        string email UK
        string contrasena
        string rol "ENUM: socio, empleado, admin"
        boolean activo
    }

    Actividades {
        int id PK
        string nombre
    }

    Actividad_empleado {
        int id PK
        int actividad_id FK
        int empleado_id FK
    }

    Clase {
        int id PK
        int turno_id FK
        datetime fecha_hora_inicio
        datetime fecha_hora_fin
        decimal costo
        integer cupo
    }

    Turnos {
        int id PK
        int actividad_id FK
        string nombre
    }

    Inscripciones_Turno {
        int id PK
        int socio_id FK
        int turno_id FK
        date fecha_alta
        string estado "ENUM: activa, de_baja"
        date fecha_baja "nullable"
    }

    Reservas {
        int id PK
        int socio_id FK
        int clase_id FK
        datetime fecha_reserva
        string estado "ENUM: activa, cancelada"
        datetime fecha_cancelacion "nullable"
        boolean asistio
        string metodo_asistencia "ENUM: manual, QR, nulo"
        datetime fecha_asistencia "nullable"
    }
    
    Lista_Espera {
        int id PK
        int socio_id FK
        int clase_id FK
        datetime fecha_anotacion
        string estado "ENUM: pendiente, notificado, resuelto"
    }

    Pagos {
        int id PK
        int socio_id FK
        int reserva_id FK "nullable"
        int clase_id FK "nullable"
        decimal monto
        datetime fecha_pago
        string tipo_pago "ENUM: sena, pago_total"
        string metodo_pago "ENUM: efectivo, trans."
    }

    %% Relaciones / Relacionales
    Usuarios ||--o{ Actividad_empleado : "asignado como empleado"
    Actividades ||--o{ Actividad_empleado : "tiene asignado"
    
    Actividades ||--o{ Turnos : "se organiza en"
    
    Turnos ||--o{ Clase : "agrupa"
    
    Usuarios ||--o{ Inscripciones_Turno : "se inscribe a"
    Turnos ||--o{ Inscripciones_Turno : "tiene inscriptos"

    Usuarios ||--o{ Reservas : "realiza (como socio)"
    Clase ||--o{ Reservas : "recibe"
    
    Usuarios ||--o{ Lista_Espera : "se anota en"
    Clase ||--o{ Lista_Espera : "tiene"
    
    Usuarios ||--o{ Pagos : "efectua (como socio)"

    Pagos ||--o{ Reservas : "puede estar asociado a"
    Pagos ||--o{ Clase : "puede estar asociado a"
````