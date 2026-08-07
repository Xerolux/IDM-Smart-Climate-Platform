#!/usr/bin/env python3
"""Apply uncluttered production silkscreen to an already routed AIR module."""
import argparse
from pathlib import Path
import pcbnew
def mm(v):return pcbnew.FromMM(v)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--variant',required=True,choices=('CO2','VOCNOX','PRESSURE'));a=ap.parse_args();b=pcbnew.LoadBoard(str(a.board))
 for fp in b.GetFootprints():fp.Reference().SetVisible(False);fp.Value().SetVisible(False)
 for item in list(b.GetDrawings()):
  if isinstance(item,pcbnew.PCB_TEXT) and ('XEROLUX AIR-SLOT' in item.GetText() or item.GetText() in ('CO2 / SCD41','VOC-NOx / SGP41','PRESSURE / BMP390')):b.RemoveNative(item)
 names={'CO2':'CO2 / SCD41 | XEROLUX','VOCNOX':'VOC-NOx / SGP41 | XEROLUX','PRESSURE':'PRESSURE / BMP390 | XEROLUX'}
 t=pcbnew.PCB_TEXT(b);t.SetText(names[a.variant]);t.SetPosition(pcbnew.VECTOR2I(mm(12.5),mm(1)));t.SetLayer(pcbnew.F_SilkS);t.SetTextSize(pcbnew.VECTOR2I(mm(.55),mm(.55)));t.SetTextThickness(mm(.1));b.Add(t)
 pcbnew.SaveBoard(str(a.board),b)
if __name__=='__main__':main()
