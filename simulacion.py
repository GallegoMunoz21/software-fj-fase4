# =============================================================================
#  simulacion.py
#  Simula al menos 10 operaciones completas (válidas e inválidas) para
#  demostrar que el sistema sigue funcionando ante errores y que todos los
#  fallos quedan registrados en el archivo de logs.
# =============================================================================

from modelos.cliente import Cliente
from modelos.servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada
from modelos.reserva import Reserva
from excepciones import SoftwareFJError
from utils.logger import obtener_logger

log = obtener_logger()


def _titulo(texto):
    print("\n" + "=" * 68)
    print(texto)
    print("=" * 68)


def ejecutar_simulacion():
    """Corre las 10 operaciones. El programa nunca se detiene por un error."""
    clientes = []     # lista interna de clientes (sin base de datos)
    servicios = []    # lista interna de servicios
    reservas = []     # lista interna de reservas

    log.info("===== INICIO DE LA SIMULACIÓN =====")

    # ---------------------------------------------------------------------
    _titulo("BLOQUE 1 - REGISTRO DE CLIENTES (válidos e inválidos)")

    # Operación 1: cliente válido
    try:
        c1 = Cliente(101, "Andres Gallego", "andres@softwarefj.com")
        clientes.append(c1)
        print("OP1  OK  ->", c1.obtener_resumen())
    except SoftwareFJError as e:
        print("OP1  ERROR ->", e)

    # Operación 2: email inválido
    try:
        c2 = Cliente(102, "Laura Mesa", "laura-correo-malo")
        clientes.append(c2)
        print("OP2  OK  ->", c2.obtener_resumen())
    except SoftwareFJError as e:
        log.warning(f"OP2 cliente inválido: {e}")
        print("OP2  ERROR (esperado) ->", e)

    # Operación 3: nombre vacío
    try:
        c3 = Cliente(103, "   ", "vacio@softwarefj.com")
        clientes.append(c3)
        print("OP3  OK  ->", c3.obtener_resumen())
    except SoftwareFJError as e:
        log.warning(f"OP3 cliente inválido: {e}")
        print("OP3  ERROR (esperado) ->", e)

    # Operación 4: segundo cliente válido
    try:
        c4 = Cliente(104, "Carlos Ruiz", "carlos@softwarefj.com")
        clientes.append(c4)
        print("OP4  OK  ->", c4.obtener_resumen())
    except SoftwareFJError as e:
        print("OP4  ERROR ->", e)

    # ---------------------------------------------------------------------
    _titulo("BLOQUE 2 - CREACIÓN DE SERVICIOS (correcta e incorrecta)")

    # Operación 5: servicios válidos
    sala = ReservaSala(201, "Sala Ejecutiva")
    equipos = AlquilerEquipos(202, "Portátiles Dell")
    asesoria = AsesoriaEspecializada(203, "Consultoría Cloud")
    servicios.extend([sala, equipos, asesoria])
    for s in servicios:
        print("OP5  OK  ->", s.describir())

    # Operación 6: servicio no disponible (para forzar un fallo más adelante)
    sala_mantenimiento = ReservaSala(204, "Sala en Mantenimiento", disponible=False)
    servicios.append(sala_mantenimiento)
    print("OP6  OK  -> creado servicio no disponible:", sala_mantenimiento.nombre)

    # ---------------------------------------------------------------------
    _titulo("BLOQUE 3 - RESERVAS (exitosas y fallidas)")

    # Operación 7: reserva de sala exitosa
    try:
        r1 = Reserva(301, c1, sala, duracion=3, horas=3)
        r1.confirmar()
        r1.procesar()
        reservas.append(r1)
        print("OP7  OK  ->", r1)
    except SoftwareFJError as e:
        print("OP7  ERROR ->", e)

    # Operación 8: alquiler de equipos exitoso (con descuento)
    try:
        r2 = Reserva(302, c4, equipos, duracion=5, cantidad=4, dias=5, descuento=0.10)
        r2.confirmar()
        r2.procesar()
        reservas.append(r2)
        print("OP8  OK  ->", r2)
    except SoftwareFJError as e:
        print("OP8  ERROR ->", e)

    # Operación 9: reserva sobre servicio NO disponible (falla controlada)
    try:
        r3 = Reserva(303, c1, sala_mantenimiento, duracion=2, horas=2)
        r3.confirmar()   # aquí se lanza ServicioNoDisponibleError
        r3.procesar()
        reservas.append(r3)
        print("OP9  OK  ->", r3)
    except SoftwareFJError as e:
        print("OP9  ERROR (esperado) ->", e)

    # Operación 10: asesoría con nivel inválido (parámetro incorrecto)
    try:
        r4 = Reserva(304, c4, asesoria, duracion=1, nivel="experto")
        r4.confirmar()
        r4.procesar()   # falla al validar el nivel
        reservas.append(r4)
        print("OP10 OK  ->", r4)
    except SoftwareFJError as e:
        print("OP10 ERROR (esperado) ->", e)

    # Operación 11 (extra): cancelación de una reserva
    try:
        r5 = Reserva(305, c1, asesoria, duracion=1, nivel="avanzado")
        r5.confirmar()
        r5.cancelar()
        reservas.append(r5)
        print("OP11 OK  ->", r5)
    except SoftwareFJError as e:
        print("OP11 ERROR ->", e)

    # ---------------------------------------------------------------------
    _titulo("RESUMEN FINAL")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados:    {len(servicios)}")
    print(f"Reservas gestionadas: {len(reservas)}")
    print("\nEl sistema terminó SIN interrumpirse pese a los errores.")
    print("Revisa el detalle en: logs/sistema.log")

    log.info("===== FIN DE LA SIMULACIÓN =====")
