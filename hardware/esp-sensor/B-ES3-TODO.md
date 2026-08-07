# B-ES3 hardware TODO

This file collects approved requirements for the next room-sensor PCB revision.
It does not change the released B-ES2-C6 JLCPCB order package.

## Approved: field-ready 1-Wire connection

- Add one 1-Wire bus for two to four externally connected DS18B20 sensors.
- Provide two parallel, clearly labelled, pluggable or screw terminal blocks.
- Each terminal exposes `3V3`, `1-WIRE` and `GND`; users must not need to
  solder wires, headers or components to use the feature.
- Use normal three-wire powered operation. Do not make parasite-power wiring
  the documented/default installation method.
- Fit the data pull-up on the PCB; start with 4.7 kohm and validate the value
  with the intended cable type, length and maximum sensor count.
- Add connector-side ESD/transient protection and a small series resistor
  chosen during signal-integrity testing.
- Keep the existing ESP32-C6 `ONEWIRE` GPIO assignment unless validation shows
  a boot, strapping or peripheral conflict.
- Label terminal pin order and polarity on silkscreen and in the pin map.
- Add firmware discovery by the sensors' unique 64-bit addresses, configurable
  names, disconnect detection and a stale/fault state.
- Bench-test one, two and four sensors, cable faults, hot-plugging and the
  maximum documented cable length before releasing manufacturing files.

## General connector rule

All functions intended for installers or end users must use labelled,
finger-accessible plug-in or screw terminals. Solder pads and pin headers may
remain test/development points only and must not be required for normal use.

