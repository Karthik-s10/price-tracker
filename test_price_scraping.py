#!/usr/bin/env python3
"""
Test price scraping with a real product
"""

from price_tracker_universal import UniversalPriceTracker

def test_price_scraping():
    """Test price scraping with a sample product"""
    print("🛒 Testing price scraping...")
    
    tracker = UniversalPriceTracker()
    
    # Test with a simpler e-commerce site
    test_products = [
        {
            'name': 'Flipkart Test',
            'url': 'https://www.flipkart.com/apple-iphone-13-128-gb-starlight/p/itm8f4c44b91f32b1'
        },
        {
            'name': 'Simple HTML Test',
            'url': 'https://httpbin.org/html'
        }
    ]
    
    for test_product in test_products:
        print(f"\n🔍 Testing: {test_product['name']}")
        print(f"📍 URL: {test_product['url']}")
        
        result = tracker.check_product_price(test_product)
        
        if result:
            print(f"✅ Price found: ₹{result}")
            return True
        else:
            print("❌ Failed to get price")
    
    return False

if __name__ == "__main__":
    success = test_price_scraping()
    if success:
        print("\n✅ Price scraping test passed!")
    else:
        print("\n❌ All price scraping tests failed!")
