#!/usr/bin/env python3
"""
Test price scraping with mock HTML
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_mock_price():
    """Test price extraction with mock HTML"""
    print("🛒 Testing with mock HTML...")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=options)
        
        # Create mock HTML with price
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Product</title>
            <meta property="product:price:amount" content="999.00">
        </head>
        <body>
            <h1>Test Product</h1>
            <div class="price">₹999.00</div>
            <span class="current-price">₹999</span>
            <div id="price">₹999.00</div>
        </body>
        </html>
        """
        
        # Load the HTML
        driver.get("data:text/html;charset=utf-8," + mock_html)
        time.sleep(2)
        
        # Test different selectors
        selectors = [
            ".price",
            ".current-price", 
            "#price",
            'meta[property="product:price:amount"]'
        ]
        
        for selector in selectors:
            try:
                if selector.startswith('meta'):
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    content = element.get_attribute('content')
                    print(f"✅ Found via {selector}: {content}")
                else:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    text = element.text.strip()
                    print(f"✅ Found via {selector}: {text}")
            except Exception as e:
                print(f"❌ {selector}: {str(e)}")
        
        driver.quit()
        print("✅ Mock test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Mock test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_mock_price()
