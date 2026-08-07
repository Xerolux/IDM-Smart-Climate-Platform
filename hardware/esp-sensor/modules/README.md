# Xerolux AIR-SLOT modules

B-ES5-MODULAR uses three electrically identical 2x4, 2.54 mm slots. The base
board is labelled CO2, VOC/NOx and PRESSURE for a clear default arrangement,
but every module works in every slot. Up to three modules may be fitted at the
same time.

## Rotation-safe pinout

| Pins | Signal | Purpose |
|---|---|---|
| 1 and 8 | GND | ground |
| 2 and 7 | SLOT_5V | protected system 5 V |
| 3 and 6 | I2C_SDA | shared I2C data |
| 4 and 5 | I2C_SCL | shared I2C clock |

The symmetric pinout is electrically identical after a 180-degree rotation.
Each module produces its own 3.3 V locally. For the enclosure, insert all
modules with their sensor side toward the broad lid ventilation field; the
electrical protection is not a substitute for correct mechanical orientation.

## Available modules

- AIR-CO2: Sensirion SCD41, address 0x62
- AIR-VOCNOX: Sensirion SGP41, address 0x59
- AIR-PRESSURE: Bosch BMP390, address 0x76

All modules are 25 x 25 mm, four-layer boards. Four layers are intentional:
the four duplicated signal pairs are routed independently without jumpers,
making the connector truly rotation-safe.

The female socket is a JLCPCB wave-solder part. Its stock and minimum purchase
quantity are dynamic; verify C58378 in the assembly viewer before payment.

