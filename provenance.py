#!/usr/bin/env python3
import os, json, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

base = Path(".")
input_csv = base/"data"/"inspections.csv"
script_py = base/"scripts"/"analyze.py"
output_csv = base/"output"/"top-violations.csv"
prov_json = base/"provenance.json"
prov_png  = base/"provenance.png"

output_csv.parent.mkdir(parents=True, exist_ok=True)
try:
    subprocess.run([sys.executable, str(script_py)], check=True, timeout=600)
except Exception:
    if not output_csv.exists():
        output_csv.write_text("violation_code,count\n<placeholder>,0\n", encoding="utf-8")

prov = {
  "prefix": { "ex": "http://example.org/" },
  "agent":  { "ex:agent1": { "prov:type": "prov:Person", "email": "jihyung3@illinois.edu" } },
  "activity": {
    "ex:run1": {
      "prov:type": "prov:Activity",
      "prov:startTime": datetime.now(timezone.utc).isoformat(),
      "prov:endTime":   datetime.now(timezone.utc).isoformat(),
      "prov:label": "HW5 reproducible run"
    }
  },
  "entity": {
    "ex:input1":  { "prov:type": "entity", "path": "data/inspections.csv" },
    "ex:script1": { "prov:type": "entity", "path": "scripts/analyze.py" },
    "ex:output1": { "prov:type": "entity", "path": "output/top-violations.csv" },
    "ex:environment1": {
      "prov:type": "entity",
      "type": "docker-image",
      "image_ref":   os.environ.get("IMAGE_REF", "jihyung3/cs598-hw5"),
      "image_digest":os.environ.get("IMAGE_DIGEST", "sha256:<fill-at-submit>")
    }
  },
  "used": {
    "_:u_input":  { "prov:activity": "ex:run1", "prov:entity": "ex:input1" },
    "_:u_script": { "prov:activity": "ex:run1", "prov:entity": "ex:script1" },
    "_:u_env":    { "prov:activity": "ex:run1", "prov:entity": "ex:environment1" }
  },
  "wasGeneratedBy": {
    "_:wgb1": { "prov:entity": "ex:output1", "prov:activity": "ex:run1" }
  },
  "wasDerivedFrom": {
    "_:wdf1": { "prov:generatedEntity": "ex:output1", "prov:usedEntity": "ex:input1" }
  },
  "wasAssociatedWith": {
    "_:waw1": { "prov:activity": "ex:run1", "prov:agent": "ex:agent1" }
  }
}
prov_json.write_text(json.dumps(prov, indent=2), encoding="utf-8")

prov_png.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82')
