@startuml
skinparam classAttributeIconSize 0

abstract class Usuario {
  - email: String
  - contrasena: String
  - nombre: String
  - apellido: String
  + iniciarSesion(): void
  + cerrarSesion(): void
  + recuperarContrasena(): void
  + verPerfil(): void
  + editarPerfil(): void
}

class Socio {
  - estado: EstadoSocio
  - creditoDisponible: Float
  + registrarse(): void
  + consultarActividades(): List<Actividad>
  + consultarReservas(): List<Reserva>
  + inscribirseATurno(turno: Turno): Reserva
  + reservarClaseIndividual(turno: Turno): Reserva
  + cancelarReserva(reserva: Reserva): void
}

class Empleado {
  + registrarAsistenciaManual(reserva: Reserva): Asistencia
  + registrarCobroManual(reserva: Reserva, monto: Float): Pago
}

class Administrador {
  + registrarEmpleado(empleado: Empleado): void
  + modificarEmpleado(empleado: Empleado): void
  + darDeBajaEmpleado(empleado: Empleado): void
  + asignarActividad(empleado: Empleado, actividad: Actividad): void
  + eliminarActividadAsignada(empleado: Empleado, actividad: Actividad): void
}

class Actividad {
  - idActividad: Integer
  - nombre: String
  - descripcion: String
  - cupoMaximo: Integer
  + crear(): void
  + modificar(): void
  + eliminar(): void
}

class Turno {
  - idTurno: Integer
  - dia: String
  - horarioInicio: Time
  - horarioFin: Time
  + crear(): void
  + modificar(): void
  + consultar(): void
  + eliminar(): void
}

class Reserva {
  - idReserva: Integer
  - fechaOperacion: Date
  - tipo: TipoReserva
  - estado: EstadoReserva
  + confirmar(): void
  + cancelar(): void
}

class Pago {
  - idPago: Integer
  - monto: Float
  - fecha: DateTime
  - metodo: TipoPago
}

class Asistencia {
  - idAsistencia: Integer
  - fechaHora: DateTime
  - metodo: MetodoAsistencia
}

' Relaciones de Herencia
Usuario <|-- Socio
Usuario <|-- Empleado
Usuario <|-- Administrador

' Relaciones de Asociación y Composición
Actividad "1" *-- "0..*" Turno : contiene >
Empleado "0..*" -- "0..*" Actividad : gestiona >
Socio "1" -- "0..*" Reserva : realiza >
Reserva "0..*" -- "1" Turno : asignada a >
Reserva "1" -- "0..1" Pago : requiere >
Reserva "1" -- "0..1" Asistencia : registra >

@enduml