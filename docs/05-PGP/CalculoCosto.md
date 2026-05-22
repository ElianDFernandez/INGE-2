# Cálculo del costo del proyecto

## 1. Actividades principales y estimación de esfuerzo

| Actividad                      | Horas por persona | Horas totales (4 personas) |
|-------------------------------|-------------------|----------------------------|
| Planificación y análisis       | 16 h              | 64 h                       |
| Diseño del sistema             | 20 h              | 80 h                       |
| Configuración del entorno      | 12 h              | 48 h                       |
| Desarrollo backend             | 60 h              | 240 h                      |
| Desarrollo frontend            | 60 h              | 240 h                      |
| Integraciones externas         | 24 h              | 96 h                       |
| Presentación de demos          | 16 h              | 64 h                       |
| Pruebas y validación           | 24 h              | 96 h                       |
| Despliegue                     | 12 h              | 48 h                       |

**Total por persona:** 244 horas  
**Total del proyecto:** 976 horas

La estimación incluye: desarrollo, pruebas, integración, corrección de errores y coordinación del equipo.

## 2. Valor hora y justificación

| Nivel de experiencia | Valor por hora (USD) |
|---------------------|----------------------|
| Junior              | 15 – 25              |
| Semi Senior         | 25 – 35              |
| Senior              | 35 – 55              |

## 3. Cálculo del costo

- **Horas totales del proyecto:** 976 h
- **Valor hora promedio:** USD 10

**Costo base del desarrollo:**  
976 h × USD 10 = USD 9.760

### Gastos adicionales

- Registro de dominio: USD 50
- Hosting: USD 12 mensuales × 4 meses = USD 48

**Total gastos adicionales:** USD 98

### Costo total del proyecto

**USD 9.760 + USD 98 = USD 9.858**

## 4. Detalle de historias de usuario


| RF    | Descripción          | Puntos | Asignación |
| ----- | -------------------- | ------ | ---------- |
| RF-01 | Registrarse          | 2      | Frontend   |
| RF-02 | Iniciar sesión       | 2      | Frontend   |
| RF-03 | Cerrar sesión        | 1      | Frontend   |
| RF-04 | Recuperar contraseña | 2      | Frontend   |
| RF-05 | Modificar contraseña | 1      | Frontend   |
| RF-06 | Ver perfil           | 1      | Frontend   |
| RF-07 | Editar perfil        | 1      | Frontend   |
| RF-08 | Ver mis actividades  | 2      | Frontend   |
| RF-09 | Listado disponibles  | 2      | Frontend   |
| RF-10 | Listado general      | 2      | Frontend   |
| RF-11 | Crear actividad      | 2      | Frontend   |
| RF-12 | Modificar actividad  | 2      | Frontend   |
| RF-13 | Baja actividad       | 1      | Frontend   |
| RF-14 | Filtros              | 2      | Frontend   |
| RF-15 | Crear turno          | 2      | Frontend   |
| RF-16 | Modificar turno      | 2      | Frontend   |
| RF-17 | Consultar turnos     | 1      | Frontend   |
| RF-18 | Eliminar turno       | 1      | Frontend   |
| RF-19 | Inscribirse          | 2      | Frontend   |
| RF-20 | Cancelar reserva     | 2      | Frontend   |
| RF-21 | Clase individual     | 2      | Frontend   |
| RF-22 | Cancelar individual  | 1      | Frontend   |
| RF-23 | Confirmación         | 2      | Frontend   |
| RF-24 | Anotarse             | 2      | Frontend   |
| RF-25 | Cancelar             | 1      | Frontend   |
| RF-26 | Ver crédito          | 1      | Frontend   |
| RF-27 | Registrar medio      | 1      | Frontend   |
| RF-28 | Eliminar medio       | 1      | Frontend   |
| RF-29 | Seña                 | 1      | Frontend   |
| RF-30 | Cobro manual         | 1      | Frontend   |
| RF-31 | Pago                 | 1      | Frontend   |
| RF-32 | Lista de espera      | 1      | Frontend   |
| RF-33 | Recordatorio pago    | 1      | Frontend   |
| RF-34 | Confirmación reserva | 1      | Frontend   |
| RF-35 | Listado              | 1      | Frontend   |
| RF-36 | Alta                 | 1      | Frontend   |
| RF-37 | Modificar            | 1      | Frontend   |
| RF-38 | Baja                 | 1      | Frontend   |
| RF-45 | QR                   | 1      | Frontend   |
| RF-46 | Manual               | 1      | Frontend   |
| RF-47 | Dashboard            | 1      | Frontend   |
| RF-01 | Registrarse          | 2      | Backend    |
| RF-02 | Iniciar sesión       | 2      | Backend    |
| RF-03 | Cerrar sesión        | 1      | Backend    |
| RF-04 | Recuperar contraseña | 2      | Backend    |
| RF-05 | Modificar contraseña | 1      | Backend    |
| RF-06 | Ver perfil           | 1      | Backend    |
| RF-07 | Editar perfil        | 1      | Backend    |
| RF-08 | Ver mis actividades  | 2      | Backend    |
| RF-09 | Listado disponibles  | 2      | Backend    |
| RF-10 | Listado general      | 2      | Backend    |
| RF-11 | Crear actividad      | 2      | Backend    |
| RF-12 | Modificar actividad  | 2      | Backend    |
| RF-13 | Baja actividad       | 1      | Backend    |
| RF-14 | Filtros              | 2      | Backend    |
| RF-15 | Crear turno          | 2      | Backend    |
| RF-16 | Modificar turno      | 2      | Backend    |
| RF-17 | Consultar turnos     | 1      | Backend    |
| RF-18 | Eliminar turno       | 1      | Backend    |
| RF-19 | Inscribirse          | 2      | Backend    |
| RF-20 | Cancelar reserva     | 2      | Backend    |
| RF-21 | Clase individual     | 2      | Backend    |
| RF-22 | Cancelar individual  | 1      | Backend    |
| RF-23 | Confirmación         | 2      | Backend    |
| RF-24 | Anotarse             | 2      | Backend    |
| RF-25 | Cancelar             | 1      | Backend    |
| RF-26 | Ver crédito          | 1      | Backend    |
| RF-27 | Registrar medio      | 1      | Backend    |
| RF-28 | Eliminar medio       | 1      | Backend    |
| RF-29 | Seña                 | 1      | Backend    |
| RF-30 | Cobro manual         | 1      | Backend    |
| RF-31 | Pago                 | 1      | Backend    |
| RF-32 | Lista de espera      | 1      | Backend    |
| RF-33 | Recordatorio pago    | 1      | Backend    |
| RF-34 | Confirmación reserva | 1      | Backend    |
| RF-35 | Listado              | 1      | Backend    |
| RF-36 | Alta                 | 1      | Backend    |
| RF-37 | Modificar            | 1      | Backend    |
| RF-38 | Baja                 | 1      | Backend    |
| RF-45 | QR                   | 1      | Backend    |
| RF-46 | Manual               | 1      | Backend    |
| RF-47 | Dashboard            | 1      | Backend    |

Total punto frontend: 60
Total punto backend: 60
Total puntos: 120
Cada Punto equivale a 4 horas, 120 puntos x 4 horas = 480 horas.

## 5. Referencias

- Jobbers: https://www.jobbers.io/argentina-freelancers-crypto-payments-dollar-income-inflation-proof-platforms/
- Devico: https://devico.io/blog/what-are-the-outsource-rates-for-software-developers-in-argentina
