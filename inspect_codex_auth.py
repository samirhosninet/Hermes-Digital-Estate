import json
import os

path = '/mnt/c/Users/seo/.codex/auth.json'
try:
    with open(path, 'r') as f:
        data = json.load(f)
        print(f"Keys: {list(data.keys())}")
        for k, v in data.items():
            if isinstance(v, dict):
                print(f"Sub-keys for {k}: {list(v.keys())}")
except Exception as e:
    print(f"Error: {e}")
