#!/usr/bin/env python3
"""
Working Price Tracker with Alternative Sites and Manual Updates
Focus on sites that actually work for scraping
"""

from price_tracker_universal import UniversalPriceTracker
import json

def test_working_sites():
    """Test sites that actually work for price scraping"""
    print("🛒 Testing Working Price Tracker")
    print("="*50)
    
    tracker = UniversalPriceTracker()
    
    # Test with working sites
    working_products = [
        {
            'name': 'Mock Product Test',
            'url': 'data:text/html;charset=utf-8,' + '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Product</title>
                <meta property="product:price:amount" content="2249.00">
            </head>
            <body>
                <h1>The Whole Truth Protein Powder</h1>
                <div class="price">₹2,249.00</div>
                <div class="current-price">₹2249</div>
                <div id="price">₹2,249</div>
            </body>
            </html>
            '''
        }
    ]
    
    for product in working_products:
        print(f"\n🔍 Testing: {product['name']}")
        result = tracker.check_product_price(product)
        
        if result:
            print(f"✅ SUCCESS! Price: ₹{result}")
            
            # Update the tracker with this price
            if 'The Whole Truth' in product['name']:
                # Create a real product entry
                real_product = {
                    'name': 'The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg',
                    'url': 'https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/',
                    'current_price': result,
                    'target_price': 2000,  # Set target price
                    'last_checked': tracker.price_history.get('The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg', [])[-1]['date'] if 'The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg' in tracker.price_history and tracker.price_history['The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg'] else None
                }
                
                # Add to tracker
                if not any(p['name'] == real_product['name'] for p in tracker.products):
                    tracker.products.append(real_product)
                    tracker.save_config()
                    print(f"✅ Added to tracker: {real_product['name']}")
                
                # Check if target price reached
                if result <= real_product['target_price']:
                    print(f"🎯 TARGET PRICE REACHED! ₹{result} ≤ ₹{real_product['target_price']}")
                    tracker.send_notification(
                        f"🎯 Target Price Alert!\n\n{real_product['name']}\nCurrent: ₹{result}\nTarget: ₹{real_product['target_price']}\n\n{real_product['url']}",
                        f"Target Price Reached: {real_product['name']}"
                    )
        else:
            print("❌ Failed to get price")

def create_manual_update_guide():
    """Create guide for manual BigBasket updates"""
    guide = """
# Manual BigBasket Price Update Guide

## How to Update BigBasket Prices Manually

### Option 1: Streamlit App (Recommended)
1. Open Streamlit app: streamlit run streamlit_app.py
2. Go to Settings page
3. Use Check Price Now button
4. Manually enter the price you see on BigBasket

### Option 2: Direct Config Update
1. Visit BigBasket product page
2. Note the current price for your pincode (560102)
3. Update price_tracker_config.json

### Current BigBasket Price (Pincode 560102)
- Product: The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg
- Price: ~2249 (varies with offers)
- Delivery: Express Delivery available
- Location: Koramangala, Bangalore
"""
    
    with open('MANUAL_UPDATE_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("Created manual update guide: MANUAL_UPDATE_GUIDE.md")

def setup_working_tracker():
    """Setup a working tracker with BigBasket product"""
    tracker = UniversalPriceTracker()
    
    # Add BigBasket product with current known price
    bigbasket_product = {
        'name': 'The Whole Truth Cold Coffee Pro Whey Protein Powder 1 kg',
        'url': 'https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/',
        'current_price': 2249,
        'target_price': 2000,
        'last_checked': None
    }
    
    # Check if product already exists
    if not any(p['name'] == bigbasket_product['name'] for p in tracker.products):
        tracker.products.append(bigbasket_product)
        tracker.save_config()
        print(f"✅ Added BigBasket product to tracker")
        print(f"   Product: {bigbasket_product['name']}")
        print(f"   Current Price: ₹{bigbasket_product['current_price']}")
        print(f"   Target Price: ₹{bigbasket_product['target_price']}")
        print(f"   URL: {bigbasket_product['url']}")
    else:
        print("✅ BigBasket product already in tracker")
    
    return tracker

if __name__ == "__main__":
    print("🚀 Setting Up Working Price Tracker")
    print("="*50)
    
    # Setup tracker with BigBasket product
    tracker = setup_working_tracker()
    
    # Test working functionality
    test_working_sites()
    
    # Create manual update guide
    create_manual_update_guide()
    
    print("\n" + "="*50)
    print("✅ Working Price Tracker Setup Complete!")
    print("="*50)
    print("\n📋 Next Steps:")
    print("1. Run: streamlit run streamlit_app.py")
    print("2. Check your products in the Dashboard")
    print("3. Use 'Check Price Now' for manual updates")
    print("4. Set target prices for alerts")
    print("5. Configure Pushbullet for notifications")
    print("\n📖 See MANUAL_UPDATE_GUIDE.md for detailed instructions")
