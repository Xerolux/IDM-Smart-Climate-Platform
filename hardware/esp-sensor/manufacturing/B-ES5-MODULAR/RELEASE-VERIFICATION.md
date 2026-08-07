# B-ES5-MODULAR release verification

## Automated CAD checks

- [x] base and all modules: KiCad 10 ERC 0 errors
- [x] base and all modules: KiCad 10 DRC 0 errors, 0 unconnected pads
- [x] schematic/PCB parity passed for all four designs
- [x] base 130 x 100 mm, modules 25 x 25 mm
- [x] Gerber and separate PTH/NPTH drill outputs generated
- [x] JLCPCB BOM/CPL generated for base and every module
- [x] enclosure base/lid/S5 plate generated and mesh-checked
- [x] 310 x 120 mm plate plus 5 mm brim fits Ultimaker S5

## Physical first-article checks still required

- [ ] inspect soldering, polarity and sensor-port cleanliness
- [ ] USB-only, 24-V-only and simultaneous-power test with current limit
- [ ] measure 24V_PROT, SYS_5V and +3V3 rails/ripple
- [ ] flash ESP32-C6-N16 and run a 24-hour base-board test
- [ ] insert each module alone, rotated both ways, while power is off
- [ ] verify all three modules together and scan 0x44/0x59/0x62/0x76
- [ ] compare temperature, RH, CO2 and pressure against references
- [ ] test VOC/NOx conditioning and enclosure self-heating bias
- [ ] calibrate 0-10 V input/output at 0/5/10 V
- [ ] test four DS18B20 probes, contacts and isolated RS-485
- [ ] verify module retention, ventilation, screws and terminal access
- [ ] sign off before HVAC connection or a production lot

