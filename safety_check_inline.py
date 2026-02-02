import json, sys

try:
    with open('price_tracker_config.json', 'r') as f_new, open('price_tracker_config.backup.json', 'r') as f_old:
        new_data = json.load(f_new)
        old_data = json.load(f_old)
        
        # Check 1: Did we lose products?
        if len(new_data['products']) != len(old_data['products']):
            print('SAFETY ERROR: Product count changed during price check. Aborting.')
            sys.exit(1)
        
        # Check 2: Did URLs change?
        for p1, p2 in zip(new_data['products'], old_data['products']):
            if p1['url'] != p2['url']:
                print('SAFETY ERROR: Product URL mismatch. Aborting.')
                sys.exit(1)
                
    print('SAFETY CHECK PASSED: Config integrity verified.')
    
except Exception as e:
    print(f'SAFETY SCRIPT ERROR: {e}')
    sys.exit(1)
