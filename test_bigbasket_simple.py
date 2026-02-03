#!/usr/bin/env python3
"""
Test BigBasket with simplified approach
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def test_bigbasket_simple():
    """Test BigBasket with simplified Chrome setup"""
    print("🛒 Testing BigBasket with simplified setup...")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200,800')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')
    
    try:
        print("🔧 Initializing Chrome driver...")
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver initialized")
        
        url = "https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/"
        print(f"🌐 Loading BigBasket URL: {url}")
        
        driver.get(url)
        time.sleep(3)
        print("✅ Page loaded")
        
        # Try to find price with basic selectors
        price_selectors = [
            ".price",
            ".current-price",
            "[class*='price']",
            "[class*='Price']",
            ".ProductPrice",
            ".Pricing___StyledLabel-sc-pldi2d-1",
        ]
        
        price = None
        for selector in price_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and ('₹' in text or 'Rs' in text or any(char.isdigit() for char in text)):
                        print(f"Found text via {selector}: {text}")
                        # Extract price
                        price_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', text.replace('₹', '').replace('Rs', '').replace(',', ''))
                        if price_match:
                            price = float(price_match.group(1))
                            print(f"✅ Found price: ₹{price}")
                            break
                if price:
                    break
            except Exception as e:
                print(f"Error with {selector}: {e}")
                continue
        
        # If still no price, check page source
        if not price:
            print("🔍 Checking page source...")
            page_source = driver.page_source
            price_patterns = [
                r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'Rs\.?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'"price":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                if matches:
                    for p in matches:
                        p = p.replace(',', '')
                        try:
                            price_val = float(p)
                            if 10 < price_val < 50000:
                                price = price_val
                                print(f"✅ Found price in source: ₹{price}")
                                break
                        except:
                            continue
                if price:
                    break
        
        driver.quit()
        
        if price:
            print(f"✅ BigBasket test successful! Price: ₹{price}")
            return True
        else:
            print("❌ BigBasket price not found")
            return False
            
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        print(f"❌ BigBasket test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_bigbasket_simple()
    if success:
        print("\n✅ BigBasket test passed!")
    else:
        print("\n❌ BigBasket test failed!")
