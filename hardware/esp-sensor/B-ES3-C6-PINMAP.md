# B-ES3-C6 pin and connector map

## ESP32-C6 signals

| Function | ESP32-C6 signal / module pin |
|---|---|
| I2C SDA / SCL | GPIO6 / GPIO7, pins 6 / 7 |
| Native USB D- / D+ | GPIO12 / GPIO13, pins 13 / 14 |
| Boot button | GPIO9, pin 15 |
| RS-485 RX / TX / DE | GPIO17 / GPIO16 / GPIO2, pins 24 / 25 / 27 |
| 1-Wire | GPIO23, pin 21 |
| Dry contact 1 / 2 | GPIO18 / GPIO19, pins 16 / 17 |
| Service button | GPIO20, pin 18 |
| Bus diagnostic LED | GPIO22, pin 20 |
| 0-10 V ADC | GPIO0 / ADC1_CH0, pin 8 |
| Status LED | GPIO8, pin 10 |

## User-accessible connections

All field wiring uses 5.00 mm push-in spring terminals. No soldering is
required for installation or RS-485 termination.

| Connector | Pin order |
|---|---|
| J1 IDM | 43 TEMP, 42 +24 V, 41 GND, 40 RH 0-10 V OUT |
| J2 isolated RS-485 | A, B, isolated COM, shield pass-through |
| J3 USB-C | 5 V programming/power and native USB/JTAG |
| J5 1-Wire A | 3.3 V, DQ, GND |
| J6 1-Wire B | 3.3 V, DQ, GND |
| J7 dry contacts | CONTACT 1, COM/GND, CONTACT 2 |
| J8 analog input | 0-10 V IN, GND |

J5 and J6 are electrically parallel points on one 1-Wire bus. SW3 enables the
120 ohm RS-485 termination. SW4 is the service/identify button.

Confirm the IDM terminal assignment for the exact heat-pump/controller model
before installation. B-ES3-C6 remains an engineering sample until its first
assembled units pass the release test plan.

