# B-ES4-AIR enclosure – Ultimaker S5

The assembled outside dimensions are 150 x 120 x approximately 26.5 mm. The
base and lid print separately with their open sides facing up; supports are
not required.

## Recommended first article

- UltiMaker S5, AA 0.4 print core
- 0.20 mm layers, four walls, six top/bottom layers
- 25% gyroid infill
- 5 mm brim with 0.1 mm gap
- no supports
- PETG preferred for technical rooms; 200/60-degree PLA is suitable for the
  first fit sample

Import `Xerolux-B-ES4-AIR-S5-AA04-PLA.inst.cfg` into Cura or apply the listed
settings. The combined `idm-roomsensor-b-es4-air_S5-print-plate.stl` occupies
310 x 120 mm before the brim and fits the 330 x 240 mm S5 bed.

The roof provides separate ventilation fields for SHT45, the local reference
sensor and the SCD41/SGP41/BMP390 AIR island. Keep the vents clear and do not
paint or solvent-clean sensor ports. Mount the unit where it sees room air but
not direct sun, supply-air jets or a warm wall cavity.

Use four M3 heat-set inserts and M3 x 25 mm countersunk lid screws. Fix the PCB
to the four standoffs with M2.5 x 6 mm thread-forming screws. Test connector
reach, insert fit and roof clearance on the first print before printing a
batch; adjust SCAD `fit` by 0.1-0.2 mm only if required by the printer.

