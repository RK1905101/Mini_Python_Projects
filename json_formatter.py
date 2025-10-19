# filename: json_formatter.py
# Run: python json_formatter.py '{"name":"Ravi","age":22}'

import json, sys

if len(sys.argv) != 2:
    print("Usage: python json_formatter.py '<json_string>'")
    sys.exit(1)

try:
    obj = json.loads(sys.argv[1])
    print(json.dumps(obj, indent=4, sort_keys=True))
except json.JSONDecodeError as e:
    print("Invalid JSON:", e)
