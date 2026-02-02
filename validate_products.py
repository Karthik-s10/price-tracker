import json
import sys

try:
    with open('price_tracker_config.json') as f1, open('price_tracker_config.backup.json') as f2:
        new = json.load(f1)
        old = json.load(f2)
        if new['products'] != old['products']:
            print('Error: Product list was modified by price tracker')
            sys.exit(1)
except Exception as e:
    print(f'Validation error: {e}')
    sys.exit(1)
