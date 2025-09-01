# main.py
import json, sys
from core.normalizer import normalize
p = sys.argv[1] if len(sys.argv)>1 else 'logs/demo_bruteforce.json'
raw = json.load(open(p))
evt = normalize(raw)
print("Normalized event:", evt)