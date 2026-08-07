# fake-sensor manufacturing status

The original `IDM-FakeSensor-ESP.kicad_pcb` Rev-A placeholder is **not released
for fabrication**.

The separate `IDM-FakeSensor-ESP-B-ES1.kicad_pcb` is released only as a
fabricable humidity-path engineering sample for current-limited bench testing.
Its controlled fabrication package is in `B-ES1/`. It has zero KiCad 10 ERC and
DRC violations, but it has not passed electrical, EMC, thermal or IDM-system
validation. J1 pin 1 (KTY/TEMP) is deliberately unconnected.
