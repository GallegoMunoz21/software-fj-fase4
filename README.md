# Software FJ - Sistema Integral de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 - Prácticas simuladas** del curso Programación (213023) - UNAD.
Sistema orientado a objetos **sin base de datos**, con manejo robusto de excepciones
y registro de eventos en archivo de logs.

## Principios de POO aplicados
- **Abstracción:** clases abstractas `EntidadBase` y `Servicio`.
- **Herencia:** `Cliente` y `Servicio` heredan de `EntidadBase`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** cada servicio sobrescribe `calcular_costo()`, `describir()` y `validar_parametros()`.
- **Encapsulación:** atributos protegidos con `properties` y validaciones en la clase `Cliente`.
- **Sobrecarga:** `calcular_costo()` con parámetros opcionales (impuesto, descuento).

## Manejo de excepciones
- Excepciones personalizadas (`excepciones.py`).
- Bloques `try/except`, `try/except/else`, `try/except/finally`.
- Encadenamiento de excepciones con `raise ... from ...`.
- Registro de errores y eventos en `logs/sistema.log`.

## Estructura
```
software_fj/
├── main.py              # Punto de entrada
├── simulacion.py        # 10+ operaciones (válidas e inválidas)
├── excepciones.py       # Excepciones personalizadas
├── utils/
│   └── logger.py        # Registro en archivo
├── modelos/
│   ├── entidad_base.py  # Clase abstracta base
│   ├── cliente.py       # Cliente + validaciones
│   ├── servicios.py     # Servicio (abstracta) + 3 servicios
│   └── reserva.py       # Reserva
└── logs/
    └── sistema.log      # Se genera al ejecutar
```

## Ejecución
```bash
python main.py
```

## Autor
Andres Felipe Gallego Muñoz
