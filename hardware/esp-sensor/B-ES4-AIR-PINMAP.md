# B-ES4-AIR Ultimate pin and connector map

Physical product marking: **by Xerolux · xerolux.de · REV B-ES4-AIR · 2026**.
No third-party brand is printed on PCB or enclosure.

## ESP32-C6-N16 signals

| Function | GPIO |
|---|---:|
| I2C SDA / SCL | GPIO6 / GPIO7 |
| Native USB D- / D+ | GPIO12 / GPIO13 |
| Boot / reset | GPIO9 / EN |
| RS-485 RX / TX / DE | GPIO17 / GPIO16 / GPIO2 |
| 1-Wire bus | GPIO23 |
| Dry contact 1 / 2 | GPIO18 / GPIO19 |
| Service button / bus LED / status LED | GPIO20 / GPIO22 / GPIO8 |
| Protected 0-10 V ADC input | GPIO0 / ADC1_CH0 |

All onboard air sensors share I2C: SHT45 temperature/humidity, SCD41 CO2,
SGP41 VOC/NOx and BMP390 barometric pressure. U11 supplies a dedicated
AIR_3V3 rail; C30 buffers the SCD41 current peaks.

## User-accessible connections

| Connector | Pin order / purpose |
|---|---|
| J1 legacy climate interface | 43 TEMP, 42 +24 V, 41 GND, 40 RH 0-10 V OUT |
| J2 isolated RS-485 | A, B, isolated COM, shield pass-through |
| J3 USB-C | 5 V power, programming and USB/JTAG |
| J5 1-Wire A | 3.3 V, DQ, GND |
| J6 1-Wire B | 3.3 V, DQ, GND |
| J7 dry contacts | CONTACT 1, COM/GND, CONTACT 2 |
| J8 analog input | 0-10 V IN, GND |
| J4 internal expansion | 3.3 V, GND, SDA, SCL, 1-Wire, GPIO4, GPIO5, SYS_5V |

J5 and J6 are parallel connection points on one 1-Wire bus and support two to
four DS18B20 probes in total. SW3 enables 120-ohm RS-485 termination. SW4 is
the service/identify button.

The board can be powered from 24 V at J1 or 5 V through USB-C. Schottky power
ORing permits both to remain connected. Validate this first with a current-
limited supply; USB-C is not a 24-V output.

