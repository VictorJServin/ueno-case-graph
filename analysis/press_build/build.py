import sys, json, glob, os, importlib
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import lib
for f in sorted(glob.glob(os.path.join(here, "b[0-9][0-9]_*.py"))):
    importlib.import_module(os.path.basename(f)[:-3])
out = os.path.join(here, "..", "..", "data", "raw")
for k, rows in lib.ROWS.items():
    with open(os.path.join(out, f"press.{k}.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(k, len(rows))
