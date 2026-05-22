# Historias de Usuario

## ID: Registrar Socio
### Título:
**como** cliente 
**quiero** registrarme en el sistema
**para** poder reservar actividades o clases.

**Título**: Como administrador quiero registrar un empleado en el sistema para que pueda operar en el establecimiento 

**Reglas de Negocio:**

-    -El DNI debe ser unico
-    -El correo electronico debe ser unico
-    -El correo electronico sera el nombre de usuario

**Criterios de Aceptación:**

Escenario 1: Registro de empleado exitoso
````
- Dado un nombre de usuario "Jose Martinez", un email "joseMartinez@mail.com", el cual no se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente completa el formulario de registro y lo envía, 
Entonces el sistema crea una nueva cuenta de socio y muestra un mensaje de confirmación.
````
Escenario 2: Registro de empleado fallido por DNI existente 
````
- Dado un nombre de usuario "Maria Lopez", un email "mariaLopez@mail.com", el cual ya se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente completa el formulario de registro y lo envía,
Entonces el sistema muestra un mensaje de error indicando que el email ya está en uso.
````
Escenario 3: Registro de empleado fallido por correo electronico existente 
````
- Dado un nombre de usuario "Carlos Gomez", un email "carlosGomez@mail.com", el cual no se encuentra registrado, y una contraseña "password"
Cuando el cliente completa el formulario de registro y lo envía
Entonces el sistema muestra un mensaje de error indicando que la contraseña no cumple con los requisitos.
````
Escenario 4: Campos obligatorios vacíos
````
- Dado un nombre de usuario vacio, un email "carlosGomez@mail.com", el cual no se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente completa el formulario de registro y lo envía,
Entonces el sistema muestra un mensaje de error indicando que los campos obligatorios están vacíos.
````
Escenario 5: Formato de email inválido
````
- Dado un nombre de usuario "Laura Sanchez", un email "lauraSanchezmail.com", el cual no se encuentra registrado, y una contraseña "Password123",
Cuando el cliente completa el formulario de registro y lo envía,
Entonces el sistema muestra un mensaje de error indicando que el formato del email es inválido.
````

## ID: Iniciar Sesión 
### Título:  
**como** como usuario registrado
**quiero** iniciar sesión en el sistema
**para** acceder a mis reservas y actividades.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Inicio de sesión exitoso
````
- Dado un email "juanPerez@mail.com", el cual se encuentra registrado, y una contraseña "Password123" que es válida, 
Cuando el cliente intenta iniciar sesión con credenciales válidas, 
Entonces el sistema permite el acceso y muestra la página principal.
````
Escenario 2: Credenciales inválidas
````
- Dado un email "carlosGomez@mail.com", el cual se encuentra registrado, y una contraseña "Password123" que no es válida, 
Cuando el cliente intenta iniciar sesión con credenciales inválidas, 
Entonces el sistema muestra un mensaje de error indicando que las credenciales son incorrectas.
````
Escenario 3: Email no registrado
````
- Dado un email "juanPerez@mail.com", el cual no se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente intenta iniciar sesión con este email, 
Entonces el sistema muestra un mensaje de error indicando que el email no está registrado.
````
Escenario 4: Campos obligatorios vacíos
````
- Dado un email vacio, y una contraseña "Password123",
Cuando el cliente intenta iniciar sesión sin ingresar un email,
Entonces el sistema muestra un mensaje de error indicando que los campos obligatorios están vacíos.
````


## ID: Cerrar Sesión
### Título:
**como** usuario autenticado
**quiero** cerrar sesión en el sistema
**para** proteger mi cuenta y mis datos personales.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Cierre de sesión exitoso
````
- Dado un usuario "Ana Torres" con una sesion activa en el sistema,
Cuando el usuario hace clic en el botón de cerrar sesión,
Entonces el sistema cierra la sesión del usuario y lo redirige a la página de inicio de sesión.
````

## ID: Recuperar Contraseña
### Título:
**como** usuario registrado que ha olvidado su contraseña
**quiero** recuperar mi contraseña
**para** poder acceder nuevamente a mi cuenta.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Solicitud de recuperación de contraseña exitosa
````
- Dado un usuario "Luis Fernandez" que ha olvidado su contraseña,
Cuando el usuario selecciona la opción de "Olvidé mi contraseña" e ingresa su email registrado "luisFernandez@mail.com",
Entonces el sistema envía un correo electrónico con instrucciones para restablecer la contraseña.
````
Escenario 2: Email no registrado
````
- Dado un usuario "Sofia Ramirez" que ha olvidado su contraseña,
Cuando el usuario selecciona la opción de "Olvidé mi contraseña" e ingresa un email no registrado "sofiaRamirez@mail.com",
Entonces el sistema muestra un mensaje de error indicando que el email no está registrado.
````
Escenario 3: Formato de email inválido
````
- Dado un usuario "Miguel Sanchez" que ha olvidado su contraseña,
Cuando el usuario selecciona la opción de "Olvidé mi contraseña" e ingresa un email con formato inválido "miguelSanchezmail.com" 
Entonces el sistema muestra un mensaje de error indicando que el formato del email es inválido.
````

## ID: Modificar Contraseña
### Título:
**como** usuario autenticado
**quiero** modificar mi contraseña
**para** acceder a mi cuenta.

### Reglas de Negocio
* Regla 1: La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una minúscula y un número.

### Criterios de Aceptación:
Escenario 1: Modificación de contraseña exitosa
````
- Dado un usuario "Laura Sanchez" con una sesión activa en el sistema, y una contraseña actual "Password123",
Cuando el usuario accede a la sección de modificar contraseña, ingresa su contraseña actual "Password123" y una nueva contraseña "NewPassword123" que cumple con los requisitos y hace clic en guardar,
Entonces el sistema actualiza la contraseña del usuario y muestra un mensaje de confirmación.
````    
Escenario 2: Contraseña actual incorrecta
````
- Dado un usuario "Carlos Gomez" con una sesión activa en el sistema, y una contraseña actual "Password123",
Cuando el usuario accede a la sección de modificar contraseña, ingresa una contraseña actual incorrecta "PasswordError" y una nueva contraseña "NewPassword123" que cumple con los requisitos y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que la contraseña actual es incorrecta.
````
Escenario 3: Nueva contraseña no cumple requisitos
````
- Dado un usuario "Ana Torres" con una sesión activa en el sistema, y una contraseña actual "Password123",
Cuando el usuario accede a la sección de modificar contraseña, ingresa su contraseña actual "Password123" y una nueva contraseña "password" que no cumple con los requisitos y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que la nueva contraseña no cumple con los requisitos.
````
Escenario 4: Campos obligatorios vacíos
````
- Dado un usuario "Luis Fernandez" con una sesión activa en el sistema, y una contraseña actual "Password123",
Cuando el usuario accede a la sección de modificar contraseña, deja vacíos los campos de contraseña actual y nueva contraseña, y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que los campos obligatorios están vacíos.
````

## ID: Ver Perfil de Usuario
### Título:
**como** usuario autenticado
**quiero** ver mi perfil de usuario
**para** ver mi informacion.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Visualización de perfil exitosa
````
- Dado un usuario "Miguel Sanchez" con una sesión activa en el sistema,
Cuando el usuario accede a la sección de perfil de usuario,
Entonces el sistema muestra la información del perfil del usuario.
````

## ID: Editar Perfil de Usuario
### Título:
**como** usuario autenticado
**quiero** editar mi perfil de usuario
**para** mantener mi información actualizada.

### Reglas de Negocio
* Regla 1: El email debe ser único.

### Criterios de Aceptación:
Escenario 1: Edición de perfil exitosa
````
- Dado un usuario "Sofia Ramirez" con una sesión activa en el sistema, y una información de perfil actual con nombre "Sofia Ramirez" y email "sofia.ramirez@example.com",
Cuando el usuario accede a la sección de editar perfil, ingresa su nombre a "Sofia R. Ramirez" y su email a "sofia.ramirez2@example.com", y hace clic en guardar,
Entonces el sistema actualiza la información del perfil del usuario y muestra un mensaje de confirmación.
````
Escenario 2: Email ya registrado
````
- Dado un usuario "Luis Fernandez" con una sesión activa en el sistema, y una información de perfil actual con nombre "Luis Fernandez" y email "luis.fernandez@example.com",
Cuando el usuario accede a la sección de editar perfil, ingresa un email ya registrado "sofia.ramirez@example.com", y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que el email ya está en uso.
````
Escenario 3: Campos obligatorios vacíos
````
- Dado un usuario "Ana Torres" con una sesión activa en el sistema, y una información de perfil actual con nombre "Ana Torres" y email "ana.torres@example.com",
Cuando el usuario accede a la sección de editar perfil, deja vacíos los campos de nombre y email, y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que los campos obligatorios están vacíos.
````
Escenario 4: Formato de email inválido
````
- Dado un usuario "Carlos Gomez" con una sesión activa en el sistema, y una información de perfil actual con nombre "Carlos Gomez" y email "carlosGomez@mail.com",
Cuando el usuario accede a la sección de editar perfil, ingresa un email con formato inválido "carlosGomezmail.com", y hace clic en guardar,
Entonces el sistema muestra un mensaje de error indicando que el formato del email es inválido.
````

## ID: Consultar mis actividades y clases reservadas
### Título:
**como** usuario autenticado
**quiero** consultar mis actividades y clases reservadas
**para** ver mis próximas reservas y actividades.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Consulta de actividades y clases reservadas exitosa
````
- Dado un usuario "Ana Torres" con una sesión activa en el sistema, y con reservas de actividades y clases próximas,
Cuando el usuario accede a la sección de "Mis Actividades y Clases Reservadas",
Entonces el sistema muestra la lista de sus actividades y clases reservadas próximas.
````
Escenario 2: Sin actividades o clases reservadas
````
- Dado un usuario "Luis Fernandez" con una sesión activa en el sistema, y sin reservas de actividades o clases próximas,
Cuando el usuario accede a la sección de "Mis Actividades y Clases Reservadas",
Entonces el sistema muestra un mensaje indicando que no tiene actividades o clases reservadas próximas.
````

## ID: Consultar turnos de actividades disponibles para reservar
### Título:
**como** usuario autenticado
**quiero** consultar el listado de turnos de actividades disponibles para reservar
**para** reservar una actividad o clase.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Consultar turnos de actividades disponibles para reservar exitosa
````
- Dado un usuario "Carlos Gomez" con una sesión activa en el sistema,
Cuando el usuario accede a la sección de "Actividades Disponibles para Reservar" y selecciona una actividad,
Entonces el sistema muestra el listado de turnos de la actividad seleccionada disponibles para reservar.
````
Escenario 2: Sin actividades disponibles para reservar
````
- Dado un usuario "Sofia Ramirez" con una sesión activa en el sistema,
Cuando el usuario accede a la sección de "Actividades Disponibles para Reservar" y no hay actividades disponibles para reservar,
Entonces el sistema muestra un mensaje indicando que no hay actividades disponibles para reservar.
````
Escenario 3: Sin turnos disponibles para reservar
````
- Dado un usuario "Miguel Sanchez" con una sesión activa en el sistema,
Cuando el usuario accede a la sección de "Actividades Disponibles para Reservar", selecciona una actividad, y no hay turnos disponibles para reservar,
Entonces el sistema muestra un mensaje indicando que no hay turnos disponibles para reservar para la actividad seleccionada.
````

## ID: Cancelar reserva a actividad
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

## ID: Cancelar reserva a clase individual
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

## ID: Entrar en lista de espera
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

## ID: Registrar metodo de pago
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
## ID: Eliminar medios de pago
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
## ID: Cancelar anotación en lista
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

## ID: Registrar empleado

### Título: 
**como** administrador 
**quiero** registrar un empleado en el sistema 
**para** que pueda operar en el establecimiento 

### Reglas de Negocio: 
-    -El correo electronico debe ser unico
-    -El correo electronico sera el nombre de usuario

### Criterios de Aceptación:

Escenario 1: Registro de empleado exitoso
````
-Dado el nombre "Vladimir",apellido "Agreda", que no se encuentra registrado y el correo electronico "emaildevladimir@gmail.com" que no existe en el sistema.
-Cuando se ingresa nombre "Vladimir",apellido "Agreda",correo electronico "emaildevladimir@gmail.com" y se apreta el boton "Registrar empleado"
-Entonces el sistema registra al nuevo empleado en el sistema y envia al correo electronico del empleado un instructivo para la creacion de su contraseña de acceso  
````
Escenario 2: Registro de empleado fallido por correo electronico existente 
````
Dado el nombre "Vladimir",apellido "Agreda" y el correo electronico "emaildevladimir@gmail.com" que se encuentra en el sistema 
Cuando se ingresa el nombre "Vladimir",apellido "Agreda",correo electronico "emaildevladimir@gmail.com" y se apreta el boton "Registrar empleado" 
Entonces el sistema informa "Error de registro.El correo electronico ingresado ya corresponde a un empleado".
````

### ID:Modificar datos de empleado 

### Título : 
**como** administrador 
**quiero** modificar los datos un empleado 
**para** que queden actualizados 

### Reglas de Negocio:

-   -El correo electronico debe ser unico

### Criterios de Aceptación:

Escenario 1: Modificacion exitosa de correo electronico 
````
- Dado el usuario "correodevladimir@gmail.com" que pertenece a un empleado registrado en el sistema y el correo electronico "correodevladimir2@gmail" que no existe en el sistema 
-Cuando el admnistrador selecciona el usuario "correodevladimir@gmail.com",selecciona "Modificar datos",luego selecciona "Correo electronico",ingresa "correodevladimir2@gmail.com" como nuevo correo electronico y presiona "Confirmar" 
-Entonces el sistema registra y actualiza el nuevo cambio,y envia una notificacion al nuevo correo

Escenario 2:Modificacion de datos exitosa 
-Dado el usuario "correodevladimir2@gmail.com" perteneciente a un empleado registrado en el sistema y el nombre "Aguiala"
-Cuando el administrador sleeciona el usuario "correodevladimir2@gmail.com",selecciona "Modificar datos",luego selecciona "Apellido",ingresa "Aguiala" como nuevo apellido y se presiona "Confirmar"
-Entonces el sistema registra el nuevo cambio y actualiza la informacion 

Escenario 3:Modificacion fallida por correo electronico existente 
-Dado el usuario "correodemacarena@gmail.com" que pertenece a un empleado registrado en el sistema y el correo electronico "correodevladimir2@gmail.com" que ya existe en el sistema 
-Cuando el administrador selecciona el usuario "correodemacarena@gmail.com",selecciona "Modificar datos",luego selecciona "Correo electronico", ingresa "correodevladimir2gmail.com" y presiona el boton "Confirmar"
-Entonces el sistema informa "Error de modificacion,el correo ingresado ya existe en el sistema" 

Escenario 4: Modificacion de datos fallida por cancelacion de la operacion 
-Dado el usuario "llll@gmail.com" que pertenece a un empleado registrado en el sistema y el nombre "Kvicha" 
-Cuando el administrador selecciona el usuario "llll@gmail.com",selecciona "Modificar datos",luego selecciona "Nombre",ingresa "Kvicha" como nuevo nombre y apreta en "Cancelar"
-Entonces el sistema informa "Operacion cancelada" 
````
### ID: Dar de baja empleado

### Título:
**Como** administrador 
**quiero** dar de baja un empleado 
**para** que no figure mas en el sistema

### Reglas de Negocio:

- Se aplica un descuento del 20% al monto total para socios abonados que mantengan el beneficio vigente. 

### Criterios de Aceptación:
````
Escenario 1: Baja de empleado exitosa 

- Dado el usuario "jjjj@gmail.com" que pertenece a un empleado registrado en el sistema 
-Cuando el administrador seleccion el usuario "jjjj@gmail.com",selecciona "Dar de baja" y confirma la operacion 
-Entonces el sistema registra la operacion,da de baja al empleado y envia la notificacion a su correo electronico 

Escenario 2: Baja de empleado fallida por cancelacion de operacion 
-Dado el usuario "jjjj@gmail.com" que pertenece a un empleado registrado en el sistema 
-Cuando el administrador seleccion el usuario "jjjj@gmail.com",selecciona "Dar de baja" y cancela la operacion   
-Entonces el sistema informa "Operacion cancelada" 
````