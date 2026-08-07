# Classic B-ES1 engineering sample

Fabricable two-layer room-sensor engineering sample with protected 24 V input,
passive KTY81/210 temperature path, SHT45, ATtiny1616, MCP4725 and OPA197
0-10 V humidity output.

KiCad 10 ERC and DRC must both remain at zero. Passing those checks proves file
consistency and geometry only. Power initially from a current-limited 24 V bench
supply and validate the KTY and humidity outputs on dummy loads before connecting
the four-position terminal to an IDM heat pump.

The ATtiny1616 requires application firmware through J2 (UPDI). Firmware release
and real-IDM validation are separate from PCB fabrication readiness.
