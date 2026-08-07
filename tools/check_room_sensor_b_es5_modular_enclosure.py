#!/usr/bin/env python3
"""Validate B-ES5-MODULAR enclosure meshes and Ultimaker S5 bed fit."""
from collections import Counter
from pathlib import Path
import re, struct

ENC=Path(__file__).resolve().parents[1]/'hardware/esp-sensor/enclosure'
def triangles(path):
 data=path.read_bytes()
 if data[:5].lower()==b'solid':
  v=[tuple(map(float,m)) for m in re.findall(rb'vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)',data)]
  return [tuple(v[i:i+3]) for i in range(0,len(v),3)]
 n=struct.unpack_from('<I',data,80)[0]; out=[]
 for i in range(n):
  q=struct.unpack_from('<9f',data,84+i*50+12); out.append(tuple(tuple(q[j:j+3]) for j in range(0,9,3)))
 return out
def check(name,lo,hi):
 ts=triangles(ENC/name); pts=[p for t in ts for p in t]
 got=tuple(min(p[i] for p in pts) for i in range(3))+tuple(max(p[i] for p in pts) for i in range(3))
 for a,e in zip(got,lo+hi): assert abs(a-e)<.011,(name,got)
 edges=Counter()
 for t in ts:
  q=[tuple(round(x,5) for x in p) for p in t]
  for a,b in ((0,1),(1,2),(2,0)): edges[tuple(sorted((q[a],q[b])))]+=1
 assert all(n==2 for n in edges.values()),f'{name}: non-manifold edges'
 print(f'PASS {name}: {len(ts)} triangles, manifold')
if __name__=='__main__':
 check('idm-roomsensor-b-es5-modular_base.stl',(0,0,0),(150,120,11))
 check('idm-roomsensor-b-es5-modular_lid.stl',(0,0,0),(150,120,22.95))
 check('idm-roomsensor-b-es5-modular_S5-print-plate.stl',(-155,-60,0),(155,60,22.95))
 assert 310+10<=330 and 120+10<=240
 print('PASS Ultimaker S5: 310x120 mm plus 5 mm brim')
