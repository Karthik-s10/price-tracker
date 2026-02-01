import json
import os

# Define the config structure
config = {
    "products": [],
    "price_history": {},
    "notifications_enabled": True
}

# Write the config file with explicit UTF-8 encoding
with open('price_tracker_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4, ensure_ascii=False)

print("Created a new price_tracker_config.json with proper encoding")
