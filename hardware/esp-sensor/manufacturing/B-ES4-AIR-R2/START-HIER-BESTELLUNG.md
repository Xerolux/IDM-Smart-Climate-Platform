# Start hier – B-ES4-AIR-R2 bestellen

Order five engineering samples first.

1. Upload the fabrication ZIP to JLCPCB and select 4 layers, 1.6 mm FR-4.
2. Enable Standard PCBA, top-side SMT and THT/wave soldering.
3. Upload the BOM and CPL from the `JLCPCB` folder.
4. Confirm the exact parts and orientation in the placement viewer.
5. Use the stocked parts U3=C5366877 (ESP32-C6-WROOM-1-N8) and
   U10=C779278 (BMP388). No pre-order is required for these two rows.
6. J5/J6/J7/J9 use the footprint-compatible 3-way screw terminal C5188435.
   Do not select the unavailable C7471335. Enable THT/wave soldering.
7. Print the base and lid using the supplied Ultimaker S5 files.
8. Bench-test USB power, 6/12/24/32 VDC power, simultaneous USB+DC, all three
   LEDs, relay COM/NO/NC, sensors, RS-485, 0-10 V, contacts and 1-Wire.
9. Do not connect to HVAC equipment or order a larger batch until the first
   articles pass `RELEASE-VERIFICATION.md`.
