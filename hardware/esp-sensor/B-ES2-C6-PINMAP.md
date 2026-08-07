# B-ES2-C6 pin and connector map

## ESP32-C6 signals

| Function | ESP32-C6 signal |
|---|---:|
| I2C SDA (SHT45, MCP4725) | GPIO6 |
| I2C SCL (SHT45, MCP4725) | GPIO7 |
| Native USB D- / D+ | GPIO12 / GPIO13 |
| Boot button | GPIO9 |
| RS-485 RX / TX / DE | GPIO17 / GPIO16 / GPIO2 |
| Expansion bus | GPIO21, GPIO4, GPIO5 |
| Status LED | GPIO8 |
| Reset button | EN |

## External connections

| Connector | Pin/function |
|---|---|
| J1 IDM | 43 KTY temperature, 42 +24 V, 41 GND/KTY return, 40 humidity 0-10 V |
| J2 RS-485 | A, B, isolated COM, shield/chassis pass-through |
| J3 USB-C | 5 V programming/power and native USB/JTAG |
| J4 expansion | 3.3 V, GND, GPIO/I2C expansion signals |

Confirm the IDM terminal assignment in the service documentation for the exact
heat-pump/controller model before installation.

## Allowed supply combinations

| USB-C | 24 V at J1 | Result |
|---|---|---|
| off | off | board off |
| on | off | programming and logic available; 0-10 V not guaranteed |
| off | on | normal field operation |
| on | on | allowed; D2/D3 isolate the two 5 V sources from each other |
