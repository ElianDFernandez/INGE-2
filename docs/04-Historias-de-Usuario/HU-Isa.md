# 3.4 Historias de Usuario

## Plantilla

**ID**: [Identificador con accion y entidad, por ejemplo: Registrar Socio]
**Título**: [Título descriptivo de la historia de usuario]
**Reglas de Negocio:**
- [Regla de negocio 1]
- [Regla de negocio 2]

**Criterios de Aceptación:**
Escenario 1: [Descripción breve del escenario]
````
- Dado [contexto], cuando [acción], entonces [resultado].
````
Escenario 2: [Descripción breve del escenario]
````
- Dado [contexto], cuando [acción], entonces [resultado].
````
Escenario n: [Descripción breve del escenario]
````
- [...]
````

## Historias de Usuario

## Isabella
- RF-20: Anotarse en lista de espera. <-- no seria un escenario de inscribirse?? ✔
- RF-21: Cancelar reservas. <- separar
- RF-22: Registrar medio de pago.✔
- RF-23: Abonar seña de reserva. 
- RF-24: Registrar cobro manual.
- RF-25: Registrar pago.✔
- RF-26: Registrar asistencia mediante escaneo de código QR.
- RF-28: Eliminar medio de pago. ✔
- Cancelar anotacion en lista ✔

### ID: Cancelar reserva a actividad
### Título:
**como** usuario abonado
**quiero** cancelar una reserva
**para** indicar que no asistire

### Reglas de Negocio:
- si cancela con 48 horas o más de anticipación se genera un crédito
- si cancela con menos tiempo pierde el turno
- si acumula tres cancelaciones en el mes pierde el beneficio del 20% de descuento sobre el abono de las clases

### Criterios de Aceptación:
Escenario 1: Cancelación exitosa con antelación sin pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una reserva abonada activa con fecha de inicio 01/05/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 superando las 48 horas y que el contador de cancelaciones en el mes es menor que 3,
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, genera un crédito, informa que la reserva fue cancelada y el monto del crédito, aumenta en 1 el contador de cancelaciones en el mes, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera.

````
Escenario 2: Cancelación exitosa sin antelación sin pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una reserva abonada activa con fecha de inicio 16/04/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 con menos de 48 horas de diferencia y que el contador de cancelaciones en el mes es menor que 3,
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, informa que la reserva fue cancelada, aumenta en 1 el contador de cancelaciones en el mes, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera
````
Escenario 3: Cancelación exitosa con antelación y pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una reserva abonada activa con fecha de inicio 20/04/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 superando las 48 horas y que cuenta con 2 cancelaciones previas en el mes,
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, genera un crédito, informa que la reserva fue cancelada, el monto del crédito y la pérdida del descuento, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera.
````
Escenario 4: Cancelación exitosa sin antelación y pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una reserva abonada activa con fecha de inicio 16/04/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 con menos de 48 horas de diferencia y que cuenta con 2 cancelaciones previas en el mes,
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, informa que la reserva fue cancelada y la pérdida del descuento, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera. (setea el contador en 0? )
````

### ID: Cancelar reserva a clase individual
### Título:
**como** usuario no abonado
**quiero** cancelar una reserva
**para** indicar que no asistire

### Reglas de Negocio:
- si cancela con 24 horas o más se devuelve la seña, si cancela con menos tiempo pierde la seña

### Criterios de Aceptación:

Escenario 1: Cancelación exitosa con devolución de seña 
````
- Dado el usuario catab@gmail.com que cuenta con una reserva señada activa con fecha de inicio 17/04/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 con al menos 24 horas de diferencia 
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, informa que la reserva fue cancelada y el monto a reembolsar, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera.

````
Escenario 2: Cancelación exitosa sin devolución de seña 
````
- Dado el usuario catab@gmail.com que cuenta con una reserva señada activa con fecha de inicio 16/04/2026, y que dicho dia es posterior al dia de hoy 15/04/2026 con menos de 24 horas de diferencia 
Cuando se presiona 'Cancelar reserva' y confirma la operación,
Entonces el sistema cancela la reserva, informa que la reserva fue cancelada, el turno pasa a estar disponible y envia una notificación al primero de la lista de espera.

````

### ID: Entrar en lista de espera
### Título:
**como** usuario 
**quiero** entrar en lista de espera
**para** poder asistir a una actividad

### Reglas de Negocio:

### Criterios de Aceptación:

Escenario 1: Agregado exitoso
````
- Dada la actividad 'Futbol 5' que posee cupo lleno y un correo isacasta@gmail.com que corresponde a un usuario existente,
Cuando se presiona 'Ingresar en lista' y confirma la operación,
Entonces el sistema añade al usuario a la cola de espera, informa que ha sido agregado a la lista y el lugar en la cola de espera. 

````

### ID: Registrar metodo de pago
### Título:
**como** usuario 
**quiero** registrar un metodo de pago
**para** poder reservar una actividad

### Reglas de Negocio:


### Criterios de Aceptación:

Escenario 1: Agregado exitoso
````
- Dado un correo isacasta@gmail.com que corresponde a un usuario existente que no posee un método de pago y  que la conexión con la API de mercado pago es exitosa,
Cuando se presiona 'Agregar método' y selecciona MercadoPago,
Entonces el sistema redirige al usuario a la aplicación de MercadoPago, aguarda confirmación y añade el método de pago. 

````
Escenario 2: Agregado fallido por cuenta ya vinculada
````
- Dado un correo isacasta@gmail.com que corresponde a un usuario existente que ya posee un método de pago,
Cuando se presiona 'Agregar método' y selecciona MercadoPago,
Entonces el sistema informa 'Error. Usted ya ha registrado este metodo en su cuenta'.

````
Escenario 3: Agregado fallido por error en conexión
````
- Dado un correo isacasta@gmail.com que corresponde a un usuario existente que no posee un método de pago y la conexión con la API de mercado pago no pudo realizarse
Cuando se presiona 'Agregar método' y selecciona MercadoPago,
Entonces el sistema informa 'Error. No se ha podido establecer la conexión. Intente más tarde'.

````
### ID: Eliminar medios de pago
### Título:
**como** usuario 
**quiero** quiero eliminar mi medio de pago
**para** cambiar el MercadoPago asociado

### Reglas de Negocio:

### Criterios de Aceptación:

Escenario 1: Eliminación exitosa
````
- Dado un correo isacasta@gmail.com que corresponde a un usuario existente que posee un método de pago y  que la conexión con la API de mercado pago es exitosa,
Cuando se presiona 'Eliminar método' y selecciona MercadoPago,
Entonces el sistema elimina el método de pago e informa 'Método eliminado'. 

````

Escenario 2: Eliminación fallida por error en conexión
````
- Dado un correo isacasta@gmail.com que corresponde a un usuario existente que posee un método de pago y  que la conexión con la API de mercado pago no pudo realizarse,
Cuando se presiona 'Eliminar método' y selecciona MercadoPago,
Entonces el sistema informa 'Error. No se ha podido establecer la conexión. Intente más tarde'. 

````
### ID: Cancelar anotación en lista
### Título:
**como** usuario 
**quiero** quiero eliminar anotación en lista de espera
**para** organizar mi agenda

### Reglas de Negocio:

### Criterios de Aceptación:

Escenario 1: Eliminación exitosa
````
- Dada la actividad 'Futbol 5' que posee cupo lleno y un correo isacasta@gmail.com que corresponde a un usuario existente en lista de espera, 
Cuando se presiona 'Dar de baja'
Entonces el sistema quita al usuario de la cola e informa la baja.

````

### ID: Registrar pago
### Título:
**como** usuario abonado
**quiero** quiero pagar mi reserva
**para** hacer efectiva la misma

### Reglas de Negocio:

- Se aplica un descuento del 20% al monto total para socios abonados que mantengan el beneficio vigente. 

### Criterios de Aceptación:

Escenario 1: Pago exitoso con descuento aplicado
````
Dado que el usuario es un socio abonado con el beneficio del 20% vigente
Y la conexión con la API de Mercado Pago es exitosa
Cuando el cliente seleccione "Inscribirse"
Entonces el sistema calcula el monto total aplicando el descuento, envía el cobro a Mercado Pago y, al recibir la confirmación, retorna a la página de reservas informando que la operación se realizó correctamente.

````
Escenario 2: Pago fallido
````
Dado que el usuario es un socio abonado con el beneficio del 20% vigente
Y la conexión con la API de Mercado Pago es exitosa
Cuando el cliente seleccione "Inscribirse"
Entonces el sistema calcula el monto con el descuento aplicado, solicita el pago a Mercado Pago y, al recibir la confirmación de que el pago fue rechazado, retorna a la página de reservas informando que la operación no pudo realizarse.

````
Escenario 3: Pago fallido por error en la conexión con MercadoPago
````
Dado que la conexión con la API de mercado pago no pudo realizarse
Cuando el cliente seleccione "Inscribirse"
Entonces el sistema rechaza la operación e informa 'Error en el pago. No se ha podido establecer la conexión. Intente más tarde'.

````
Escenario 4: Pago exitoso sin descuento por pérdida de beneficio
````
Dado que el usuario es un socio abonado pero ha acumulado 3 o más cancelaciones en el mes corriente
Y la conexión con la API de Mercado Pago es exitosa
Cuando el cliente seleccione "Inscribirse"
Entonces el sistema calcula el monto total de la actividad sin aplicar el descuento del 20%, envía el cobro a Mercado Pago y, tras recibir la confirmación de pago, informa al usuario que la reserva fue confirmada al valor total por pérdida del beneficio mensual.
````
### ID: Abonar seña
### Título:
**como** usuario no abonado
**quiero** quiero pagar una seña
**para** hacer efectiva la reserva

### Reglas de Negocio:

- La seña corresponde obligatoriamente al 50% del valor total de la clase o turno suelto.
- El pago de la seña es una condición necesaria para confirmar la reserva; si el pago no se completa, el cupo no se descuenta del inventario.

### Criterios de Aceptación:

Escenario 1: Pago de seña exitoso 
````
Dado un socio ocasional que ha seleccionado la actividad 'Futbol 5' y el horario '17:00 hs' con cupo disponible, y la conexión con la API de Mercado Pago es exitosa
Cuando el usuario presiona 'Inscribirse'
Entonces el sistema calcula el valor de la seña (50% del total) envía el cobro a Mercado Pago y, al recibir la confirmación, retorna a la página de reservas informando que la operación se realizó correctamente, confirma la reserva y disminuye en 1 el cupo disponible.

````
Escenario 2: Pago de seña fallido 
````
Dado un socio ocasional que ha seleccionado la actividad 'Futbol 5' y el horario '17:00 hs' con cupo disponible,  la conexión con la API de Mercado Pago es exitosa
Cuando el usuario presiona 'Inscribirse'
Entonces el sistema calcula el valor de la seña (50% del total) envía el cobro a Mercado Pago y recibe notificación del rechazo del pago, retorna a la página de reservas informando que el pago no pudo procesarse.

````
Escenario 3: Pago de seña fallido por error en conexión
````
Dado que la conexión con la API de mercado pago no pudo realizarse
Cuando el cliente seleccione "Inscribirse"
Entonces el sistema rechaza la operación e informa 'Error en el pago de la seña. No se ha podido establecer la conexión. Intente más tarde'.

````

### ID: Registrar cobro manual
### Título:
**como** personal de recepcion
**quiero** registrar manualmente el pago de un socio
**para** confirmar reservas

### Reglas de Negocio:

- El sistema debe registrar qué usuario realizó el cobro manual, la fecha, la hora y el monto ingresado.
- Al registrar el cobro manual, el sistema debe actualizar el estado de la reserva o del abono a "Confirmado" o "Pagado" de forma inmediata, liberando las restricciones de acceso al socio.
- Se debe especificar el medio de pago manual utilizado para facilitar el cierre de caja posterior.

### Criterios de Aceptación:

Escenario 1: Registro exitoso de cobro de seña
````
Dado un empleado de recepción que ha seleccionado la reserva a la clase 'Futbol 5' pendiente de un socio ocasional y el socio se presenta en el local para abonar el 50% de la seña en efectivo
Cuando el empleado selecciona la opción "Registrar Cobro Manual", ingresa el monto y confirma la operación
Entonces el sistema cambia el estado de la reserva a "Confirmada", emite un comprobante digital y registra el ingreso en el reporte diario de caja.

````
Escenario 2: Registro exitoso de pago de abono mensual 
````
Dado un socio abonado se encuentra en estado "Activo" (dentro del periodo del día 1 al 10) y el socio se presenta en recepción para pagar su cuota mensual dentro de los primeros 10 dias del mes
Cuando el empleado selecciona "Registrar Cobro Manual"
Entonces el sistema calcula el monto con el 20% de descuento, registra el pago, mantiene el estado "Activo" del socio y genera el comprobante de pago.

````
Escenario 3: Registro exitoso de pago de socio moroso
````
Dado que un socio abonado figura en estado "Moroso" por falta de pago (después del día 11) y el socio realiza el pago total de la cuota en recepción en los primeros 10 dias del mes
Cuando el empleado selecciona la opción "Registrar Cobro Manual", ingresa el monto y confirma la operación
Entonces el sistema actualiza el estado del socio a "Activo", añade el beneficio del 20% de descuento al abono y notifica que el pago fue recibido.

````
Escenario 4: Registro exitoso de pago de abono atrasado
````
Dado un socio abonado se encuentra en estado "Activo" y el socio se presenta en recepción para pagar su cuota mensual pasados los primeros 10 dias del mes
Cuando el empleado selecciona la opción "Registrar Cobro Manual", ingresa el monto y confirma la operación
Entonces el sistema actualiza el estado del socio a "Moroso", remueve el descuento del 20% del pago y notifica que el pago fue recibido fuera de término.

````
Escenario 5: Registro fallido por omisión de datos obligatorios en el registro manual
````
Dado un empleado que está registrando un cobro manual
Cuando intenta confirmar la operación sin haber seleccionado el "Medio de Pago" o sin ingresar el monto percibido
Entonces el sistema resalta los campos obligatorios y no permite guardar el cambio hasta que la información esté completa.
````

### ID: Consultar mi crédito disponible 
### Título:
**como** socio abonado
**quiero** visualizar el saldo de crédito a mi favor y su fecha de expiración
**para** saber si puedo aplicarlo a una nueva reserva antes de que termine el mes

### Reglas de Negocio:

- Todo crédito acumulado tiene vigencia hasta el último día del mes calendario en el que se generó. Al iniciar un nuevo mes, el saldo vuelve a cero automáticamente.

### Criterios de Aceptación:

Escenario 1: Consulta con crédito vigente
````
Dado un socio abonado que posee un saldo de $5000 a favor generado por una cancelación previa en el mes corriente
Cuando el usuario accede a su perfil en la sección de "Mis Créditos"
Entonces el sistema muestra el monto disponible de $5000 y la leyenda: "Vence el [último día del mes actual]".
````
Escenario 2: Consulta sin crédito disponible
````
Dado un socio que no ha realizado cancelaciones con el tiempo de aviso requerido o ya utilizó su saldo previo
Cuando el usuario accede a la sección de "Mis Créditos"
Entonces el sistema muestra un saldo de $0 
````
Escenario 3: Visualización de crédito tras cambio de mes
````
Dado un socio con crédito a favor el día 31 de marzo
Cuando el usuario consulta su saldo el día 1 de abril
Entonces el sistema muestra saldo $0
````
Escenarfio 4: Acumulación de múltiples créditos
````
Dado un socio que realizó dos cancelaciones válidas (48hs de aviso) en diferentes semanas del mismo mes
Cuando el usuario consulta su crédito
Entonces el sistema muestra la suma total de ambos créditos como un único saldo disponible, con la misma fecha de vencimiento (fin de mes).
````

### ID: Registrar asistencia con QR
### Título:
**como** personal de recepción
**quiero** validar el ingreso de los socios mediante el escaneo de un código QR
**para** registrar su asistencia 

### Reglas de Negocio:

- El código QR debe estar vinculado a un socio con una reserva confirmada para la actividad, día y hora actual.
- El sistema solo permitirá registrar la asistencia dentro de un margen configurado.
- Si el socio se encuentra en estado "Moroso" (por falta de pago), el sistema debe denegar el acceso e informar el motivo al recepcionista, incluso si tiene una reserva previa.
- Un código QR no puede ser utilizado más de una vez para la misma sesión de actividad.

### Criterios de Aceptación:

Escenario 1: Registro de asistencia exitoso
````
Dado que un socio con estado "Activo" tiene una reserva confirmada para la hora corriente y presenta su código QR por primera vez en la recepción
Cuando el empleado escanea el código 
Entonces el sistema marca al socio como "Presente", registra la hora exacta de ingreso y muestra un mensaje visual de éxito.
````
Escenario 2: Registro de asistencia fallida por socio moroso
````
Dado que un socio abonado posee una reserva para la actividad actual y su estado es "Moroso" y presenta su código QR por primera vez
Cuando se escanea su código QR
Entonces el sistema bloquea el registro de asistencia, e informa: "Acceso denegado: Socio con deuda pendiente".
````
Escenario 3: Registro de asistencia fallido por código QR fuera de horario o sin reserva
````
Dado que un socio presenta su código QR por primera vez y no posee una reserva confirmada para el turno actual o se presenta fuera del margen de tiempo permitido
Cuando se realiza el escaneo
Entonces el sistema informa: "Sin reserva activa para este horario".
````
Escenario 4: Registro de asistencia fallido por escaneo duplicado
````
Dado que el socio presenta su código QR por segunda vez
Cuando se intenta escanear el mismo código QR por segunda vez 
Entonces el sistema muestra un mensaje de advertencia indicando que la asistencia ya fue tomada previamente.

````
### ID: Registrar asistencia manualmente
### Título:
**como** personal de recepción
**quiero** buscar a un socio en la lista de turnos y marcar su asistencia de forma manual
**para** permitir el ingreso de aquellos socios que no puedan utilizar el código QR o cuando el hardware de escaneo presente fallas. 

### Reglas de Negocio:

- El código QR debe estar vinculado a un socio con una reserva confirmada para la actividad, día y hora actual.
- El sistema debe registrar qué empleado realizó el marcado manual para evitar registros fraudulentos.
- Si el socio se encuentra en estado "Moroso" (por falta de pago), el sistema debe denegar el acceso e informar el motivo al recepcionista, incluso si tiene una reserva previa.

### Criterios de Aceptación:

Escenario 1: Registro manual exitoso
````
Dado un socio activo que se presenta en recepción sin su código QR y el empleado de recepción visualiza la lista de inscriptos para la clase actual
Cuando el empleado selecciona al socio y hace clic en "Marcar Asistencia"
Entonces el sistema cambia el estado del socio a "Presente", registra la hora y el nombre del empleado que autorizó el ingreso.
````
Escenario 2:  Registro manual fallido por socio moroso
````
Dado un socio moroso que se presenta en recepción sin su código QR y el empleado de recepción visualiza la lista de inscriptos para la clase actual
Cuando el empleado selecciona al socio y hace clic en "Marcar Asistencia"
Entonces el sistema denega la acción y muestra un mensaje de alerta: "Operación denegada: Socio con deuda. Dirigase a la sección de pagos" 
````


