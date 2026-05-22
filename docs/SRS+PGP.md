# Especificación de Requisitos de Software (SRS) y Historias de Usuario

## 1) Introducción

### a. Propósito y alcance

El propósito de este documento es definir de manera clara y detallada los requisitos funcionales y no funcionales para el desarrollo del proyecto "CAD" (Centro de Actividades Deportivas), una plataforma integral para la gestión de un centro deportivo que ofrece diversas actividades y clases.

Este documento esta dirigido a Laura y Jose, y al equipo de desarrolladores del sistema, con el proposito de establecer un base comun de entendimiento sobre los requisitos del sistema y coordinar las expectativas entre las partes involucradas.

### b. Definiciones, acrónimos y abreviaturas

- **Abonado:** Socio con un turno fijo asignado en una actividad específica cada mes, con beneficios como descuentos y prioridad en reservas.
- **Ocasional:** Socio que no tiene un turno fijo asignado y reserva clases individuales.
- **Socio:** Usuario registrado en el sistema que puede reservar actividades y gestionar su cuenta.
- **Empleado:** Usuario operativo cuyo rol está asociado a una actividad específica que puede gestionar.
- **Administrador:** Usuario con permisos elevados para gestionar el sistema y acceder a información sensible.
- **Seña:** Pago parcial requerido para reservar una clase individual.
- **Crédito:** Saldo a favor del socio que puede ser utilizado para futuras reservas o cobros.
- **Lista de espera:** Mecanismo para gestionar reservas cuando una actividad está completa, con asignación automática de cupo si se libera uno.
- **Dashboard:** Panel de control para el administrador con indicadores clave del negocio.
- **API:** Interfaz de Programación de Aplicaciones. Permite la integración con servicios externos, como pasarelas de pago.
- **PWA:** Aplicación Web Progresiva. Aplicación web que se comporta como una aplicación nativa en dispositivos móviles.
- **CAD:** Nombre del sistema de gestión del Centro de Actividades Deportivas.
- **Rol:** Configuración que permite asignar permisos específicos a los usuarios empleados y definir sus accesos en el sistema.

### 1.4 Referencias

Nombre del documento | Fecha de creacion | Autor 
--- | --- | ---
[Entrevista 1](../01-Entrevistas/Entrevista-1.md) | 30/03/2026 | Syncro
[Cuestionario](../01-Entrevistas/Cuestionario.md) | 30/03/2026 | Syncro
[Entrevista 2](../01-Entrevistas/Entrevista-2.md) | 06/04/2026 | Syncro
[Epicas](../02-Epícas/Epicas.md)| 06/04/2026 | Syncro


## 2) Descripción general

### a. Resumen de la idea del producto

"CAD" es una plataforma web progresiva (PWA) diseñada para digitalizar y automatizar la gestión de un centro deportivo que ofrece múltiples actividades. 

El sistema permitirá a los socios registrarse, reservar actividades, gestionar pagos y recibir notificaciones, mientras que los empleados podrán administrar las operaciones diarias y el administrador tendrá acceso a métricas clave para la toma de decisiones estratégicas.

La plataforma distingue claramente entre roles operativos (empleados) y gerenciales (administrador), con funcionalidades específicas para cada uno, y busca reducir la carga manual mediante automatizaciones, como la gestión de listas de espera y recordatorios de pago.

Los empleados podrán gestionar actividades, turnos y asistencias mediante QR, mientras que los socios podrán reservar tanto actividades regulares como clases individuales con seña. El sistema también manejará la suspensión automática por mora y la liberación de cupos, optimizando la experiencia tanto para los usuarios como para el personal del centro. Por otro lado el administrador tendrá un dashboard con indicadores clave del negocio, como cantidad de socios activos, socios abonados vs ocasionales, entre otros que le permitirán tener una visión general del estado del centro y tomar decisiones en base a los datos.

"CAD" se concibe como una solución integral que no solo mejora la eficiencia operativa, sino que también ofrece una experiencia de usuario fluida y moderna, adaptada a las necesidades específicas de un centro deportivo.

### b. Perspectiva del producto

"CAD" es un producto independiente que no forma parte de un sistema más grande, pero que se integra con servicios externos como pasarelas de pago online y sistemas de mensajería para notificaciones. Los problemas con estos servicios externos afectarian solo parcialmente al sistema.

### c. Características de los usuarios

- Socio:
    - Registrarse e iniciar sesión.
    - Registrar un medio de pago.
    - Reservar clases.
    - Reservar una actividad.
    - Cancelar reservas.
    - Ver actividades disponibles y horarios.
    - Ver clases disponibles.
    - Recibir notificaciones de recordatorios de pago y avisos de lista de espera.
    - Confirmar asistencia a clase por estar en lista de espera.

- Empleado:
    - Iniciar sesión.
    - Gestionar actividad y sus turnos.
    - Validar asistencia por QR.
    - Registrar cobros manuales.

- Administrador:
    - Iniciar sesión.	
    - ver listado de empleados.
    - Dar de alta a un empleado.
    - Dar de baja a un empleado.
    - Modificar datos de un empleado.
    - Consultar dashboard de indicadores de negocio.

### d. Evolución previsible del sistema

- Integración con múltiples pasarelas de pago.
- Reglas dinámicas de precios/promociones.
- Analítica avanzada de ocupación y predicción de demanda.
- Integración con control de acceso físico (molinete/lector QR dedicado).

## 3) Requisitos del Software

### 3.1 Requisitos de Interfaz

#### a. Interfaz de Usuario

- La interfaz de usuario debe ser intuitiva y fácil de navegar, con un diseño responsive que se adapte tanto a pc como a dispositivos móviles.

<div style="text-align: center;">
    <p style="font-size: 1.2em; font-weight: bold;">Logo Propuesto por Syncro:</p>
    <img src="../../assets/Logo.png" alt="Logo" width="180"/>
</div>

#### b. Interfaces de Software

- **Mercado Pago:** 
    * Propósito: Facilitar el proceso de pagos en línea para reservas tanto de actividades como de clases.
    * Uso: El usuario del sistema podra registrar su medio de pago (Mercado pago) y realizar pagos de seña o pagos completos para confirmar sus reservas. El sistema se integrara con la API de Mercado Pago para procesar estos pagos de manera segura y eficiente.
    * Integraciones: El sistema se comunicara con la API de Mercado Pago para gestionar la transaccion.
    * Consideraciones: La funcionalidad depende de la disponibilidad de la API de Mercado Pago, y se implementaran medidas de seguridad para proteger los datos de pago de los usuarios.

#### c. Interfaces de Hardware

- Cámara de dispositivo móvil para validación de asistencia.

### 3.2 Requisitos funcionales

### 3.2 Requisitos funcionales

#### 3.2.1 Gestión de Autenticación y Usuarios
#### 3.2.2 Gestión de Actividades y Reservas
#### 3.2.3 Turnos
#### 3.2.4 Reservas
#### 3.2.5 Gestión de Lista de Espera
#### 3.2.6 Gestión de Créditos y Pagos
#### 3.2.7 Gestión de Notificaciones
#### 3.2.8 Gestión de Personal
#### 3.2.9 Gestión de Roles y Permisos
#### 3.2.10 Gestión de Asistencia
#### 3.2.11 Métricas

Link a Taiga: https://tree.taiga.io/project/isa-cast-ing2_2026_grupo_47/epics

### 3.3 Requisitos no funcionales

- **Fiabilidad:** El sistema deberá garantizar la integridad de los datos ante fallos de red o energía, permitiendo la recuperación de las operaciones una vez restablecidas las condiciones normales.

- **Mantenibilidad:** El sistema será entregado sin compromiso de mantenimiento posterior a la entrega final. Cualquier mantenimiento adicional quedará fuera del alcance de este proyecto.

- **Multiplataforma:** El sistema, al ser implementando como Progressive Web App (PWA), es multiplataforma por definición, pudiendo ser utilizado en cualquier dispositivo con un navegador web, como ordenadores, tablets o móviles.

- **Seguridad:** El sistema contará con autenticación para el acceso a funcionalidades específicas a través de cuentas, distinguiendo entre usuario general, empleado y gerente (administrador). Si no se inició sesión, no se podra acceder a ninguna funcionalidad del sistema. Las contraseñas deberán almacenarse de forma cifrada mediante algoritmos seguros.

- **Privacidad:** El sistema implementará estrictas medidas de privacidad para garantizar la protección de la información personal y los datos de los usuarios, asegurando que toda información personal se maneje de acuerdo con las normativas de protección de datos vigentes.

- **Concurrencia:** El sistema debe soportar múltiples usuarios accediendo simultáneamente, garantizando que las operaciones como reservas, pagos y actualizaciones de datos se realicen sin conflictos. Se implementará un mecanismo de control de concurrencia en la base de datos (como transacciones) para evitar inconsistencias, por ejemplo, en la reserva simultánea de una misma actividad.

- **Rendimiento:** El sistema debe ser capaz de manejar un número significativo de usuarios simultáneos (al menos 200 usuarios activos) sin degradación significativa del rendimiento. Las operaciones críticas, como la reserva de actividades o el procesamiento de pagos, deben completarse en un tiempo razonable para garantizar una experiencia de usuario fluida.

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
Fallas en integración con Mercado Pago | 50% | Catastrófico | Pruebas anticipadas | Implementar pagos manuales temporales o deshabilitar pagos online | Elian Fernandez
Problemas de concurrencia en reservas | 50% | Catastrófico | Uso de transacciones y control de cupos en base de datos | Corrección de inconsistencias manualmente y bloqueo temporal de reservas | Isabella Castañeda
