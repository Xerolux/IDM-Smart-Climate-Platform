#!/usr/bin/env python3
"""Export/import Specctra routing data using KiCad's bundled Python."""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("export", "import"))
    parser.add_argument("board", type=Path)
    parser.add_argument("exchange", type=Path)
    args = parser.parse_args()
    board = pcbnew.LoadBoard(str(args.board))
    if args.mode == "export":
        if not pcbnew.ExportSpecctraDSN(board, str(args.exchange)):
            raise SystemExit("DSN export failed")
        print(f"Exported {args.exchange}")
    else:
        if not pcbnew.ImportSpecctraSES(board, str(args.exchange)):
            raise SystemExit("SES import failed")
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
        pcbnew.SaveBoard(str(args.board), board)
        print(f"Imported {args.exchange}")


if __name__ == "__main__":
    main()
