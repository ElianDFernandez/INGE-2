Consultas 
Con respecto a cancelacion: 
- Si cancelo una clase individual, sin estar inscripto a un turno, cuenta como cancelaciones para la perdida del beneficio del 20% de descuento?
- 

Con respecto a cancelacion de la inscripcion de un turno:
- Si cancelo la inscripcion de un turno, cada clase cuenta como una cancelacion individual? 
- Si soy un socio abonado (inscripto a un turno) y cancelo una clase especifica de ese turno, que logica aplica? 24 horas (no abonado) o 48 horas (abonado)?

Info de correos: 
¿Cual es el tiempo limite para cancelaciones?
Para abonados:
• con 48 horas o mas de anticipacion: genera credito
• con menos de 48 horas: pierde el turno
• con 3 cancelaciones en el mes: pierde el beneficio del 20% de descuento
Para no abonados:
• con 24 horas o mas: se devuelve la sena
• con menos de 24 horas: pierde la sena

### ID: Cancelar inscripción a turno
### Título:
**como** usuario abonado
**quiero** cancelar mi inscripción a un turno
**para** indicar que no asistiré más a sus clases

### Reglas de Negocio:
- al cancelar una inscripción, cada clase del turno se evalúa individualmente: si la clase tiene 48 horas o más de anticipación, se genera un vale por esa clase
- si la clase tiene menos de 48 horas de anticipación, no se genera vale por esa clase
- si el turno no fue abonado (pago no confirmado), no se generan vales al cancelar
- el contador de cancelaciones se incrementa en 1 por cada clase cancelada en el mes, independientemente de si el turno fue abonado o no
- si el contador acumula 3 o más cancelaciones en el mes, el socio pierde el beneficio del 20% de descuento sobre el abono del mes siguiente
- el contador se resetea a 0 al inicio de cada mes; si el socio no alcanza las 3 cancelaciones en el mes siguiente, recupera el descuento

### Criterios de Aceptación:
Escenario 1: Cancelación exitosa con antelación sin pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una inscripción abonada activa a un turno con 2 clases restantes (01/05/2026 y 08/05/2026), y que ambas fechas superan las 48 horas de anticipación respecto al día de hoy 15/04/2026, y que el contador de cancelaciones en el mes es menor que 3,
Cuando se presiona 'Dar de baja' y confirma la operación,
Entonces el sistema cancela la inscripción, genera un vale por cada clase que cumpla la anticipación, informa la cantidad de vales generados, y aumenta en 1 el contador de cancelaciones por cada clase cancelada
````

Escenario 2: Cancelación exitosa con clases mixtas (algunas con antelación, otras sin ella) sin pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una inscripción abonada activa a un turno con 2 clases restantes (16/04/2026 con menos de 48hs y 20/04/2026 con más de 48hs de anticipación respecto al día de hoy 15/04/2026), y que el contador de cancelaciones en el mes es menor que 3,
Cuando se presiona 'Dar de baja' y confirma la operación,
Entonces el sistema cancela la inscripción, genera un vale únicamente por la clase con 48hs o más de anticipación, informa que se generó 1 vale y que la otra clase no genera vale por falta de anticipación, y aumenta en 2 el contador de cancelaciones
````

Escenario 3: Cancelación exitosa sin antelación suficiente en ninguna clase sin pérdida de beneficio
````
- Dado el usuario isacasta@gmail.com que cuenta con una inscripción abonada activa a un turno con 2 clases restantes (ambas con menos de 48hs de anticipación respecto al día de hoy), y que el contador de cancelaciones en el mes es menor que 3,
Cuando se presiona 'Dar de baja' y confirma la operación,
Entonces el sistema cancela la inscripción, no genera vales, informa que las clases no generan vale por falta de anticipación y aumenta en 2 el contador de cancelaciones
````

Escenario 4: Cancelación con antelación y pérdida de beneficio por acumulación
````
- Dado el usuario isacasta@gmail.com que cuenta con una inscripción abonada activa a un turno con 2 clases restantes (ambas con más de 48hs de anticipación), y que tiene 2 cancelaciones previas en el mes,
Cuando se presiona 'Dar de baja' y confirma la operación,
Entonces el sistema cancela la inscripción, genera un vale por cada clase, informa la cantidad de vales generados,y el socio pierde el beneficio del 20% de descuento sobre el abono del mes siguiente.
````

Escenario 5: Cancelación de turno no abonado
````
- Dado el usuario isacasta@gmail.com que cuenta con una inscripción activa a un turno con 2 clases restantes que no fueron abonadas (pago no confirmado),
Cuando se presiona 'Dar de baja' y confirma la operación,
Entonces el sistema cancela la inscripción, no genera vales por no existir pago confirmado, informa que la inscripción fue cancelada, y aumenta el contador de cancelaciones en 2.
````