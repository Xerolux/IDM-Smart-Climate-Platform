# B-ES3-C6 enclosure validation for UltiMaker S5

Status: CAD, mesh and Cura slice checked. A physical first article with the
assembled PCB is still required before series printing.

## Mechanical fit

| Check | Result |
| --- | --- |
| PCB | 130 x 80 mm PCB positioned at x/y 10 mm in the 150 x 100 mm case |
| PCB holes | All four 3.2 mm KiCad holes map to dedicated M2.5 supports |
| Side clearance | At least 6.1 mm between PCB edge and the inner locating liner |
| PCB height | PCB top at 7.4 mm from the base underside |
| Roof clearance | 16.7 mm above the PCB surface |
| Tallest checked terminal | MX205R-5.0 body envelope 14.4 mm |
| Terminal-to-roof margin | Approximately 2.3 mm |
| User connections | J1/J2/J5-J8 have push-in access; J3 USB-C and J4 click connector have side openings |
| Controls | Tool access for reset, boot and service; access for RS-485 termination switch |
| Sensing | Separate ventilation fields above SHT45 and the local temperature sensor |
| Fastening | Four M3 countersunk lid screws with heat-set inserts; four M2.5 PCB screws |

The terminal envelope in the OpenSCAD assembly preview uses the manufacturer's
14.4 mm dimension. Connector openings are deliberately larger than the nominal
body envelopes to tolerate normal FDM and PCB-placement variation.

## UltiMaker S5 slice

| Parameter | Prepared value |
| --- | --- |
| Printer | UltiMaker S5, 330 x 240 x 300 mm build volume |
| Print core | AA 0.4 |
| Material in supplied G-code | UltiMaker PLA, 2.85 mm |
| Part layout | 310 x 100 x 17.95 mm; centered on the bed |
| Edge margin | 10 mm in X before brim; 70 mm in Y |
| Layer/walls | 0.20 mm, 4 walls, 6 top, 6 bottom |
| Infill/support | 25% gyroid, no support |
| Adhesion | 5 mm brim, 0.1 mm gap |
| Temperatures | 200 degrees C nozzle, 60 degrees C bed |
| Cura estimate | 15 h 09 min, approximately 154 g PLA |

The individual base, lid and combined S5-plate STL files are closed, manifold
triangle meshes. The G-code contains 90 layers and no support toolpaths.

## First-article acceptance

Before printing a batch, print one set and check: all six terminal levers and
wire entries are reachable, USB-C inserts without case load, the lid closes
without pressing components, all buttons and the termination switch can be
operated, insert installation does not split a boss, and the SHT45 responds
without excessive enclosure-induced thermal lag.

Do not reuse the supplied PLA G-code for PETG, ASA, another nozzle or another
printer. Re-slice the combined STL with the matching Cura material profile.
