# PGP 

## 1) Introduccion
### a. Proposito y alcance 

Este documento define los requisitos, caracteristicas, interfaces, pruebas y validaciones del proyecto "CAD" (Centro de Actividades Deportivas), una plataforma web progresiva (PWA) diseñada para digitalizar y automatizar la gestión de un centro deportivo que ofrece múltiples actividades.
Dirigido a Laura, Jose y SYNCRO, busca alinear la planeacion, diseño, implementacion y testing acordando costos, riesgos y tiempos de entrega.

El sistema automatiza procesos como registro de usuarios, reservas, pagos y gestión de actividades, mejorando la experiencia de los socios y optimizando las operaciones del centro deportivo. La planificacion del proyecto se divide en fases: análisis de requisitos, diseño, implementación, pruebas y despliegue, con entregas parciales para cada fase dentro de un cronograma acordado.


### b. Definiciones, acrónimos y abreviaturas

- **SRS:** Especificación de Requisitos de Software. Documento que detalla los requisitos funcionales y no funcionales del sistema.
- **PGP:** Plan de Gestión de Proyecto. Documento que describe cómo se gestionará el proyecto, incluyendo planificación, recursos, riesgos y comunicación.
- **Pila de producto:** Conjunto priorizado de historias de usuario, tareas y funcionalidades a implementar en el proyecto.
- **Demo:** Entrega parcial del sistema para mostrar avances y recolectar feedback.
- **Stakeholder:** Persona o grupo con interés en el proyecto (ej: Laura, Jose, Syncro).
- **Syncro:** Nombre del equipo de desarrollo responsable del proyecto.
- **API:** Interfaz de Programación de Aplicaciones. Permite la integración con servicios externos, como pasarelas de pago.
- **PWA:** Aplicación Web Progresiva. Aplicación web que se comporta como una aplicación nativa en dispositivos móviles.

### c. Referencias

Nombre del documento | Fecha de creacion | Autor 
--- | --- | ---
[Entrevista 1](../01-Entrevistas/Entrevista-1.md) | 30/03/2026 | Syncro
[Cuestionario](../01-Entrevistas/Cuestionario.md) | 30/03/2026 | Syncro
[Entrevista 2](../01-Entrevistas/Entrevista-2.md) | 01/04/2026 | Syncro
[Epicas](../02-Epícas/Epicas.md)| 06/04/2026 | Syncro
[SRS](../03-SRS/SRS.md) | 14/04/2026 | Syncro

## 2) Planes generales
### a. Entregables del proyecto

Fecha estimada | Entrega 
--- | ---
06/04/2026 | Entrevistas + Cuestionario + Epicas
20/04/2026 | SRS,PGP + Pila de producto
27/05/2026 | Demo 1
29/06/2026 | Demo 2

### b. Calendario y resumen del presupuesto 

Se estima una duración aproximada de 4 meses para el desarrollo completo del proyecto, con entregas parciales cada 4 semanas. El costo total del proyecto sera de USD 9.858.

### c. Plan del personal 
* Project Manager: Uno, con una participacion durante toda la duracion del proyecto.
* Desarrolladores: Tres, con una participacion durante toda la duracion del proyecto.

## 3) Presupuesto
### a. Principales actividades del proyecto

El desarrollo del sistema "CAD" se organiza en las siguientes actividades principales, estructuradas de manera secuencial e iterativa, siguiendo un enfoque ágil:

#### 1. Planificación y Análisis
- Revisión y validación de requisitos funcionales y no funcionales.
- Identificación de actores y historias de usuario.
- Estimación de esfuerzo y planificación inicial.

#### 2. Diseño del Sistema
- Diseño de la arquitectura del sistema.
- Modelado de base de datos.
- Definición de estructura de backend y frontend.
- Diseño de interfaces de usuario.

#### 3. Configuración del Entorno de Desarrollo
- Creación del repositorio y configuración de control de versiones.
- Definición de flujo de trabajo.
- Integración inicial de herramientas necesarias.

#### 4. Desarrollo del Backend
- Implementación de autenticación y gestión de usuarios.
- Desarrollo de lógica de negocio (actividades, turnos, reservas).
- Implementación de sistema de pagos.
- Gestión de roles y permisos.

#### 5. Desarrollo del Frontend
- Implementación de interfaces de usuario.
- Desarrollo de funcionalidades principales (reservas, pagos, perfil).
- Adaptación a diseño responsive (PWA).

#### 6. Integraciones Externas
- Integración con pasarela de pagos (Mercado Pago).
- Implementación de lectura de QR para asistencia.
- Configuración de notificaciones.

#### 7. Presentación de Demos
- Preparación de demostraciones funcionales del sistema.
- Presentación de avances al cliente o stakeholders.
- Recolección de feedback.
- Ajuste de funcionalidades en base a las observaciones recibidas.

#### 8. Pruebas y Validación
- Pruebas funcionales.
- Pruebas de integración.
- Corrección de errores.
- Validación con los requisitos.

#### 9. Despliegue
- Configuración del entorno de producción.
- Publicación de la aplicación.
- Verificación del correcto funcionamiento en entorno real.

### b. Asignación de esfuerzo

La estimación del esfuerzo se realizó en base a las actividades principales del proyecto, considerando el nivel de experiencia del equipo (desarrolladores en formación) y contemplando tiempos adicionales por coordinación, aprendizaje y retrabajo.

| Actividad | Horas por persona | Horas totales (4 personas) |
|----------|------------------|---------------------------|
| Planificación y análisis | 16 h | 64 h |
| Diseño del sistema | 20 h | 80 h |
| Configuración del entorno | 12 h | 48 h |
| Desarrollo backend | 60 h | 240 h |
| Desarrollo frontend | 60 h | 240 h |
| Integraciones externas | 24 h | 96 h |
| Presentación de demos | 16 h | 64 h |
| Pruebas y validación | 24 h | 96 h |
| Despliegue | 12 h | 48 h |

**Total por persona:** 244 horas  
**Total del proyecto:** 976 horas

Se incluye dentro de esta estimación:
- Desarrollo
- Pruebas
- Integración
- Corrección de errores
- Coordinación del equipo

---

### c. Presupuesto final

El presupuesto del proyecto se calculó a partir del esfuerzo total estimado y un valor hora acorde al nivel del equipo.

- **Horas totales del proyecto:** 976 horas
- **Valor hora promedio del equipo:** USD 10

> El valor de hora promedio se estableció tomando una referencia de mercado para desarrolladores en formación o junior, y considerando que el equipo esta compuesto por desarrolladores aun en formacion.

**Cálculo del costo**

- **Costo base del desarrollo:**  
  976 h × USD 10 = USD 9.760

**Gastos adicionales**

- Registro de dominio: USD 50  
- Hosting: USD 12 mensuales × 4 meses = USD 48

- **Total gastos adicionales:** USD 98  

**Costo total del proyecto**

**USD 9.760 + USD 98 = USD 9.858**

## 4) Riesgos

Riesgo | Probabilidad de que ocurra | Impacto | Mitigación | Plan de contingencia | Responsable
--- | --- | --- | --- | --- | ---
Falta de experiencia del equipo en desarrollo | 80% | Catastrófico | Dividir tareas en módulos pequeños, capacitaciones iniciales y uso de buenas prácticas | Reasignación de tareas críticas y simplificación del alcance | Elian Fernandez
Dificultades en el uso de Git | 75% | Serio | Definir flujo de trabajo simple, uso de ramas por feature y buenas prácticas | Centralizar commits en un responsable y resolución manual de conflictos | Valentin Volatile
Falta de tiempo del equipo | 70% | Catastrófico | Planificación con margen y priorización de funcionalidades críticas | Reducción del alcance del sistema y enfoque en funcionalidades esenciales | Isabella Castañeda
Retrasos en el desarrollo | 60% | Serio | Seguimiento semanal del avance y ajuste de tareas | Replanificación del cronograma y reducción de funcionalidades no críticas | Vladimir Agreda
Fallas en integración con Mercado Pago | 50% | Catastrófico | Uso de entorno sandbox y pruebas anticipadas | Implementar pagos manuales temporales o deshabilitar pagos online | Elian Fernandez
Problemas de concurrencia en reservas | 50% | Catastrófico | Uso de transacciones y control de cupos en base de datos | Corrección de inconsistencias manualmente y bloqueo temporal de reservas | Isabella Castañeda
