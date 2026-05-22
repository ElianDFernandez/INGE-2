# Historias de Usuario - Elian
- RF-01: Registrarse. (elian)
- RF-02: Iniciar sesión. (elian)
- RF-03: Cerrar sesión. (elian)
- RF-04: Recuperar contraseña. (elian)
- RF-05: Modificar contraseña. (elian)
- RF-06: Ver perfil de usuario. (elian)
- RF-07: Editar perfil de usuario. (elian)
- RF-08: Consultar mis actividades y clases reservadas. (elian)
- RF-09: Consultar listado de actividades disponibles para reservar. (elian)
- RF-39: Consultar listado de roles. (elian)
- RF-40: Crear rol.  (elian)
- RF-41: Modificar rol.  (elian)
- RF-42: Eliminar rol.  (elian)
- RF-43: Asignar rol a un empleado.  (elian)
- RF-44: Asignar permisos a un rol.  (elian)



## ID: Registrar Socio
### Título:
**como** cliente 
**quiero** registrarme en el sistema
**para** poder reservar actividades o clases.

### Reglas de Negocio:
- Regla 1: El email debe ser único.
- Regla 2: La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una minúscula y un número.

### Criterios de Aceptación:
Escenario 1: Registro exitoso
````
- Dado un nombre de usuario "Jose Martinez", un email "joseMartinez@mail.com", el cual no se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente completa el formulario de registro y lo envía, 
Entonces el sistema crea una nueva cuenta de socio y muestra un mensaje de confirmación.
````
Escenario 2: Email ya registrado
````
- Dado un nombre de usuario "Maria Lopez", un email "mariaLopez@mail.com", el cual ya se encuentra registrado, y una contraseña "Password123", 
Cuando el cliente completa el formulario de registro y lo envía,
Entonces el sistema muestra un mensaje de error indicando que el email ya está en uso.
````
Escenario 3: Contraseña no cumple requisitos
````
- Dado un nombre de usuario "Carlos Gomez", un email "carlosGomez@mail.com", el cual no se encuentra registrado, y una contraseña "password"
Cuando el cliente completa el formulario de registro y lo envía
Entonces el sistema muestra un mensaje de error indicando que la contraseña no cumple con los requisitos.
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


## ID: Cerrar Sesión
### Título:
**como** usuario autenticado
**quiero** cerrar sesión en el sistema
**para** proteger mi cuenta y mis datos personales.

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Cierre de sesión exitoso
````
- Dado que un usuario con mail "ana.torres@example.com" tiene una sesión activa en el sistema,
cuando hace clic en el botón de cerrar sesión,
entonces el sistema cierra la sesión y lo redirige a la página de inicio de sesión.
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
- Dado que un usuario con mail "luisfernandez@mail.com" ha olvidado su contraseña,
cuando selecciona la opción "Olvidé mi contraseña" e ingresa su email registrado,
entonces el sistema envía un correo electrónico con instrucciones para restablecer la contraseña.
````
Escenario 2: Email no registrado
````
- Dado que un usuario con mail "sofiaramirez@mail.com" ha olvidado su contraseña,
cuando selecciona la opción "Olvidé mi contraseña" e ingresa un email no registrado,
entonces el sistema muestra un mensaje de error indicando que el email no está registrado.
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
- Dado que un usuario con mail "laura.sanchez@example.com" tiene sesión activa y su contraseña actual es "Password123",
cuando accede a la sección de modificar contraseña, ingresa la contraseña actual y una nueva contraseña válida "NewPassword123" y guarda,
entonces el sistema actualiza la contraseña y muestra un mensaje de confirmación.
````
Escenario 2: Contraseña actual incorrecta
````
- Dado que un usuario con mail "carlosgomez@mail.com" tiene sesión activa y su contraseña actual es "Password123",
cuando accede a la sección de modificar contraseña, ingresa una contraseña actual incorrecta "PasswordError" y una nueva contraseña válida "NewPassword123" y guarda,
entonces el sistema muestra un mensaje de error indicando que la contraseña actual es incorrecta.
````
Escenario 3: Nueva contraseña no cumple requisitos
````
- Dado que un usuario con mail "ana.torres@example.com" tiene sesión activa y su contraseña actual es "Password123",
cuando accede a la sección de modificar contraseña, ingresa la contraseña actual y una nueva contraseña inválida "password" y guarda,
entonces el sistema muestra un mensaje de error indicando que la nueva contraseña no cumple con los requisitos.
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
- Dado que un usuario con mail "miguel.sanchez@example.com" tiene sesión activa,
cuando accede a la sección de perfil de usuario,
entonces el sistema muestra la información del perfil del usuario.
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
- Dado que un usuario con mail "sofia.ramirez@example.com" tiene sesión activa y su nombre de usuario actual es "Sofia Ramirez",
cuando accede a editar perfil, ingresa nombre "Sofia R. Ramirez" y email "sofia.ramirez2@example.com" y guarda,
entonces el sistema actualiza la información y muestra un mensaje de confirmación.
````
Escenario 2: Email ya registrado
````
- Dado que un usuario con mail "luis.fernandez@example.com" tiene sesión activa y su nombre de usuario actual es "Luis Fernandez",  y un email ya registrado "sofia.ramirez@example.com"  
cuando accede a editar perfil, ingresa el email "sofia.ramirez@example.com" y guarda,  
entonces el sistema muestra un mensaje de error indicando que el email ya está en uso.
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
- Dado que un usuario con mail "ana.torres@example.com" tiene sesión activa y reservas próximas de actividades y clases,
cuando accede a la sección de "Mis Actividades y Clases Reservadas",
entonces el sistema muestra la lista de actividades y clases reservadas próximas.
````
Escenario 2: Sin actividades o clases reservadas
````
- Dado que un usuario con mail "luisfernandez@mail.com" tiene sesión activa y no tiene reservas próximas de actividades o clases,
cuando accede a la sección de "Mis Actividades y Clases Reservadas",
entonces el sistema muestra un mensaje indicando que no tiene actividades o clases reservadas próximas.
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
- Dado que un usuario con mail "carlosgomez@mail.com" tiene sesión activa,
cuando accede a la sección de "Actividades Disponibles para Reservar" y selecciona una actividad,
entonces el sistema muestra el listado de turnos de la actividad seleccionada disponibles para reservar.
````
Escenario 2: Sin actividades disponibles para reservar
````
- Dado que un usuario con mail "sofia.ramirez@example.com" tiene sesión activa,
cuando accede a la sección de "Actividades Disponibles para Reservar" y no hay actividades disponibles,
entonces el sistema muestra un mensaje indicando que no hay actividades disponibles para reservar.
````
Escenario 3: Sin turnos disponibles para reservar
````
Dado que un usuario accede a la sección de "Actividades Disponibles para Reservar", selecciona una actividad y no hay turnos disponibles,
cuando intenta reservar,
entonces el sistema muestra un mensaje indicando que no hay turnos disponibles para la actividad seleccionada.
````

## ID: Consultar actividades asignadas a un empleado
### Título:
**como** administrador
**quiero** consultar el listado de actividades asignadas a un empleado
**para** consultar sus responsabilidades

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Consulta exitosa de actividades
````
- Dado un usuario con permisos de administrador, y un correo "luis.fernandez@mail.com" que corresponde a un empleado con actividades asignadas,
Cuando presiona "ver actividades asingadas",
Entonces el sistema muestra el listado de acitivades asignadas al empleado.
````

Escenario 2: Consulta sin actividades asignadas
````
- Dado un usuario con permisos de administrador, y un correo "ana.torres@example.com" que corresponde a un emplado sin activades asignadas,
Cuando presionar "ver actividades asingadas" sobre el empleado,
Entonces el sistema muestra un mensaje indicando que no hay actividades asignadas para el empleado.
````

## ID: Asignar actividad a un empleado
### Título:
**como** administrador
**quiero** asignar una actividad a un empleado
**para** darle la responsabilidad de gestionarla

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Asignacion de actividad exitosa
````
- Dado un usuario con permisos de administrador, y un correo "luis.fernandez@mail.com" que corresponde a un empleado,
Cuando presiona "editar actividades" sobre el empleado, presiona una actividad y guarda
Entonces el sistema asigna la actividad al empleado.
````

## ID: Eliminar actividad asignada a un empleado
### Título:
**como** administrador
**quiero** eliminar una actividad a un empleado
**para** quitarles la responsabilidad de gestionarla

### Reglas de Negocio

### Criterios de Aceptación:
Escenario 1: Eliminacion de actividad exitosa
````
- Dado un usuario con permisos de administrador, y un correo "luis.fernandez@mail.com" que corresponde a un empleado con la actividad "futbol" asignada
Cuando presiona "editar actividades" sobre el empleado, presiona la actividad "futbol" y guarda
Entonces el sistema revoca la actividad presionada del empleado.
````