import argparse
import json
from capture import capture
from merge import merge
from writeXLSX import writeXLSX

parser = argparse.ArgumentParser(description="genshin-gacha-export")
parser.add_argument("-o", type=str, default="gachaData.json")
parser.add_argument("-m", "--merge", type=str, default=None)
parser.add_argument("-e", "--export", type=str, default="gachaExport.xlsx")
args = parser.parse_args()
if args.m:
    with open(args.m, "r", encoding="utf-8") as f:
        localdata = json.load(f)
else:
    localdata = []
gachadata = merge(capture(), localdata)
with open(args.o, "w", encoding="utf-8") as f:
    json.dump(gachadata, f, ensure_ascii=False, sort_keys=False, indent=4)
writeXLSX(gachadata, args.e)
