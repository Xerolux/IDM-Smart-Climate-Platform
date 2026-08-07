#!/usr/bin/env python3
"""Generate engineering and JLCPCB BOM/CPL files for AIR-SLOT modules."""

from __future__ import annotations
import argparse, csv, zipfile
from pathlib import Path

COMMON = {
 "J1": ("Made in China","2.54mm 2x4 female socket","AIR-SLOT female socket, vertical","THT P2.54mm 2x04","C58378"),
 "U2": ("TECH PUBLIC","AP2112K-3.3TRG1","3.3 V 600 mA LDO","SOT-23-5","C23380830"),
}
PARTS = {
 "CO2": {"U1":("Sensirion","SCD41-D-R1","photoacoustic CO2 sensor","SCD4x 10.1x10.1 mm","C3659362"),
         "C1":("Murata","GRM21BR71A106KE51L","10 uF 10 V X7R","0805","C86038"),
         "C2":("TDK","C2012X5R1A226MT0J0E","22 uF 10 V X5R","0805","C361180"),
         "C3":("Murata","GRM188R71H104KA93D","100 nF 50 V X7R","0603","C77055")},
 "VOCNOX": {"U1":("Sensirion","SGP41-D-R4","VOC and NOx index sensor","DFN-6 2.4x2.4 mm","C3659325"),
            "R1":("Yageo","RC0603FR-0710RL","10 ohm 1%","0603","C109318"),
            "C1,C2":("Samsung","CL21B105KBFNNNE","1 uF 50 V X7R","0805","C28323"),
            "C3":("Murata","GRM188R71H104KA93D","100 nF 50 V X7R","0603","C77055"),
            "C4":("Murata","GRM21BR71A106KE51L","10 uF 10 V X7R","0805","C86038"),
            "C5":("TDK","C2012X5R1A226MT0J0E","22 uF 10 V X5R","0805","C361180")},
 "PRESSURE": {"U1":("Bosch Sensortec","BMP390","barometric pressure sensor","LGA-10 2x2 mm","C5124834"),
              "C1,C2":("Murata","GRM188R71H104KA93D","100 nF 50 V X7R","0603","C77055"),
              "C3":("Murata","GRM21BR71A106KE51L","10 uF 10 V X7R","0805","C86038"),
              "C4":("TDK","C2012X5R1A226MT0J0E","22 uF 10 V X5R","0805","C361180")},
}

def split(s): return [x.strip() for x in s.split(',')]
def write(path,fields,rows):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('positions',type=Path); ap.add_argument('release',type=Path); ap.add_argument('--variant',choices=PARTS,required=True)
 a=ap.parse_args()
 with a.positions.open(newline='',encoding='utf-8-sig') as f: pos={r['Ref']:r for r in csv.DictReader(f)}
 groups={**COMMON,**PARTS[a.variant]}; full=[]; bom=[]; cpl=[]
 for refs,data in groups.items():
  maker,mpn,desc,fp,lcsc=data; rr=split(refs)
  full.append({'Designator':refs,'Quantity':len(rr),'Manufacturer':maker,'Manufacturer Part Number':mpn,'Description':desc,'Footprint':fp,'LCSC Part Number':lcsc,'Assembly':'JLCPCB Standard PCBA'})
  bom.append({'Comment':mpn,'Designator':refs,'Footprint':fp,'JLCPCB Part #':lcsc})
  for ref in rr:
   r=pos[ref]; cpl.append({'Designator':ref,'Mid X':r['PosX'],'Mid Y':r['PosY'],'Rotation':r['Rot'],'Layer':r['Side'].title()})
 stem=f'AIR-{a.variant}'
 write(a.release/f'{stem}-BOM.csv',['Designator','Quantity','Manufacturer','Manufacturer Part Number','Description','Footprint','LCSC Part Number','Assembly'],full)
 write(a.release/'JLCPCB/JLCPCB_BOM.csv',['Comment','Designator','Footprint','JLCPCB Part #'],bom)
 write(a.release/'JLCPCB/JLCPCB_CPL.csv',['Designator','Mid X','Mid Y','Rotation','Layer'],cpl)
 gerbers=a.release/'gerbers'; fabrication=a.release/f'{stem}-fabrication.zip'
 if gerbers.is_dir():
  with zipfile.ZipFile(fabrication,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for path in sorted(gerbers.iterdir()):
    if path.is_file(): z.write(path,path.name)
 package=a.release/f'{stem}-JLCPCB-order-package.zip'
 files=[fabrication,a.release/'JLCPCB/JLCPCB_BOM.csv',a.release/'JLCPCB/JLCPCB_CPL.csv',a.release/f'{stem}-BOM.csv',a.release/f'{stem}-schematic.pdf',a.release/f'{stem}-top.png',a.release/'README.md']
 if all(p.is_file() for p in files):
  with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for path in files: z.write(path,path.relative_to(a.release).as_posix())
 print(f'{stem}: {len(full)} BOM lines, {len(cpl)} placements')
if __name__=='__main__': main()
