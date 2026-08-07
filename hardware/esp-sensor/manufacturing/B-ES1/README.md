# ESP B-ES1 engineering sample

Fabricable two-layer room-sensor engineering sample with protected 24 V input,
passive KTY81/210 temperature path, local SHT45, ESP32-C3-DevKitM-1, MCP4725 and
OPA197 0-10 V humidity output.

GPIO8 is SDA and GPIO9 is SCL, matching the repository ESPHome configuration.
KiCad 10 ERC and DRC must both remain at zero. Power initially from a
current-limited 24 V bench supply and validate the KTY and humidity outputs on
dummy loads before connecting the four-position terminal to an IDM heat pump.

`JLCPCB/` contains the JLCPCB-formatted BOM and CPL for partial top-side SMT
assembly plus the remaining hand-assembly list and upload instructions.
`IDM-RoomSensor-ESP-B-ES1-JLCPCB-order-package.zip` bundles those files with
the fabrication archive; extract it and upload Gerber ZIP, BOM and CPL separately.
