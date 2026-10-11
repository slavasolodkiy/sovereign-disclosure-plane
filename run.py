import argparse, json
from pathlib import Path
from disclosure_plane import Ledger, evaluate

parser = argparse.ArgumentParser()
parser.add_argument("request", type=Path)
args = parser.parse_args()
request = json.loads(args.request.read_text(encoding="utf-8"))
ledger = Ledger()
result = evaluate(request, ledger)
print(json.dumps(result, indent=2))
print("ledger_valid:", ledger.verify())
