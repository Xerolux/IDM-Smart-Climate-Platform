#!/usr/bin/env python3
"""Validate B-ES5-MODULAR base, modules, archives and enclosure package."""
import csv, sys, zipfile
from pathlib import Path
def rows(p):
 with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def refs(s):return {x.strip() for x in s.split(',') if x.strip()}
def validate_design(root,stem,bom_lines,placements,critical):
 bom=rows(root/'JLCPCB/JLCPCB_BOM.csv'); cpl=rows(root/'JLCPCB/JLCPCB_CPL.csv'); pos={r['Ref']:r for r in rows(root/f'{stem}-positions.csv')}
 br=set()
 for r in bom: br|=refs(r['Designator']); assert r['JLCPCB Part #'].startswith('C') and 'TBD' not in ','.join(r.values()).upper()
 assert len(bom)==bom_lines and len(cpl)==placements and br=={r['Designator'] for r in cpl}
 for r in cpl:
  s=pos[r['Designator']]; assert (r['Mid X'],r['Mid Y'],r['Rotation'],r['Layer'].lower())==(s['PosX'],s['PosY'],s['Rot'],s['Side'].lower())
 by={r['Designator']:r['JLCPCB Part #'] for r in bom}
 for k,v in critical.items(): assert by[k]==v,(k,by[k])
 drc=(root/'DRC-KICAD10.txt').read_text(); erc=(root/'ERC-KICAD10.txt').read_text()
 assert 'Found 0 DRC violations' in drc and 'Found 0 unconnected pads' in drc and 'Errors 0' in erc
 fab=root/f'{stem}-fabrication.zip'; assert fab.is_file()
 with zipfile.ZipFile(fab) as z:names=z.namelist()
 for suffix in ('F_Cu.gtl','In1_Cu.g1','In2_Cu.g2','B_Cu.gbl','F_Mask.gts','B_Mask.gbs','Edge_Cuts.gm1','PTH.drl'):
  assert any(n.endswith(suffix) for n in names),suffix
 assert (root/f'{stem}-JLCPCB-order-package.zip').is_file()
 return len(names)
def main():
 root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('hardware/esp-sensor/manufacturing/B-ES5-MODULAR')
 n=validate_design(root,'IDM-RoomSensor-ESP-B-ES5-MODULAR',55,84,{'U3':'C5445014','U4':'C5221601','U7':'C2890051','J9,J10,J11':'C225519','C30':'C963255'})
 specs={'CO2':(6,6,'C3659362'),'VOCNOX':(8,9,'C3659325'),'PRESSURE':(6,7,'C5124834')}
 for v,(b,p,sensor) in specs.items():validate_design(root/f'Modules/AIR-{v}',f'AIR-{v}',b,p,{'J1':'C58378','U1':sensor,'U2':'C23380830'})
 for name in ('base.stl','lid.stl','S5-print-plate.stl'):assert any(p.name.endswith(name) for p in (root/'Gehaeuse').iterdir())
 assert (root/'IDM-RoomSensor-B-ES5-MODULAR-KOMPLETTPAKET.zip').is_file()
 print(f'B-ES5-MODULAR package valid: base 55 BOM lines/84 placements, three modules, {n} fabrication files')
if __name__=='__main__':main()
