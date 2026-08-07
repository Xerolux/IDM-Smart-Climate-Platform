# B-ES4-AIR release verification

## Automated CAD checks (2026-08-07)

- [x] KiCad 10 ERC: 0 errors (`ERC-KICAD10.txt`)
- [x] KiCad 10 DRC: 0 errors and 0 unconnected pads (`DRC-KICAD10.txt`)
- [x] extended DRC contains only silkscreen/text warnings
- [x] four copper layers and closed 130 x 100 mm outline
- [x] schematic/PCB parity: 300 connected reference/pin/net tuples matched
- [x] BOM/CPL reference parity: 94 of 94 placements
- [x] Gerbers include F.Cu, In1.Cu, In2.Cu, B.Cu, masks, silkscreens,
  Edge.Cuts, PTH and NPTH drill files
- [x] base, lid and S5 plate are manifold STL meshes
- [x] 310 x 120 mm plate plus 5 mm brim fits Ultimaker S5
- [x] ESPHome configuration validates with ESPHome 2026.7.4

## Physical first-article release (must still be completed)

- [ ] inspect assembly and sensor-port contamination under magnification
- [ ] USB-only / 24-V-only / dual-source power test with current limit
- [ ] verify 24V_PROT, SYS_5V, +3V3 and AIR_3V3 rails and ripple
- [ ] flash and run a 24-hour sensor plausibility/logging test
- [ ] compare temperature, RH, CO2 and pressure against references
- [ ] exercise VOC/NOx conditioning and verify no enclosure self-heating bias
- [ ] calibrate 0-10-V output and input at 0/5/10 V
- [ ] test 1-Wire with four probes and hot-plug/disconnect cases
- [ ] test both contacts and isolated RS-485 with SW3 off/on
- [ ] verify dual-power backfeed/thermal behavior
- [ ] verify all enclosure openings, screws, inserts and field terminals
- [ ] sign off before HVAC connection or a production lot
