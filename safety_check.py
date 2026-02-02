import json
import sys

try:
    with open('price_tracker_config.json', 'r') as f1, open('price_tracker_config.backup.json', 'r') as f2:
        new_data = json.load(f1)
        old_data = json.load(f2)
        
        # Check if product count changed
        if len(new_data['products']) != len(old_data['products']):
            print('SAFETY ERROR: Product count changed. Aborting push.')
            sys.exit(1)
            
        # Check if URLs changed (order matters)
        for p1, p2 in zip(new_data['products'], old_data['products']):
            if p1['url'] != p2['url']:
                print('SAFETY ERROR: Product URLs changed. Aborting push.')
                sys.exit(1)
except Exception as e:
    print(f'SAFETY CHECK FAILED: {e}')
    sys.exit(1)
