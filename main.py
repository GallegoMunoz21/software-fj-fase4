# =============================================================================
#  main.py
#  Punto de entrada del sistema Software FJ.
#
#  Ejecuta la simulación de operaciones. Toda la gestión se hace en memoria
#  (objetos y listas), sin bases de datos, y los eventos y errores quedan
#  registrados en logs/sistema.log.
#
#  Ejecutar con:  python main.py
# =============================================================================

from simulacion import ejecutar_simulacion


def main():
    print("SOFTWARE FJ - Sistema Integral de Clientes, Servicios y Reservas")
    ejecutar_simulacion()


if __name__ == "__main__":
    main()
