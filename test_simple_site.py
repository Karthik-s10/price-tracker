#!/usr/bin/env python3
"""
Test with a simpler site that has visible prices
"""

from price_tracker_universal import UniversalPriceTracker

def test_simple_site():
    """Test with a site that has prices"""
    print("🛒 Testing with simple site...")
    
    tracker = UniversalPriceTracker()
    
    # Test with a mock e-commerce page
    test_product = {
        'name': 'Mock E-commerce Test',
        'url': 'data:text/html;charset=utf-8,' + '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Product Page</title>
            <meta property="product:price:amount" content="1299.00">
            <meta property="og:price:amount" content="1299">
        </head>
        <body>
            <h1>Test Product</h1>
            <div class="price">₹1,299.00</div>
            <span class="current-price">₹1299</span>
            <div id="price">₹1,299</div>
            <div class="product-price">Rs. 1299</div>
            <div data-price="1299">Price: ₹1299</div>
        </body>
        </html>
        '''
    }
    
    print(f"\n🔍 Testing: {test_product['name']}")
    print(f"📍 URL: {test_product['url'][:50]}...")
    
    result = tracker.check_product_price(test_product)
    
    if result:
        print(f"✅ Price found: ₹{result}")
        return True
    else:
        print("❌ Failed to get price")
        return False

if __name__ == "__main__":
    success = test_simple_site()
    if success:
        print("\n✅ Simple site test passed!")
    else:
        print("\n❌ Simple site test failed!")
