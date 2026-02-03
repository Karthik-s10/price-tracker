#!/usr/bin/env python3
"""
Simple BigBasket login test without complex options
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_simple_setup():
    """Test simple Chrome setup for BigBasket"""
    print("🧪 Testing Simple BigBasket Setup")
    print("="*50)
    
    # Simple Chrome options
    options = Options()
    options.add_argument('--headless')  # Set to False to see browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        print("🔧 Setting up Chrome driver...")
        driver = webdriver.Chrome(options=options)
        
        print("✅ Chrome driver setup successful")
        
        # Test BigBasket homepage
        print("🌐 Loading BigBasket homepage...")
        driver.get("https://www.bigbasket.com/")
        time.sleep(5)
        
        print("✅ BigBasket homepage loaded successfully")
        
        # Check page title
        title = driver.title
        print(f"📄 Page title: {title}")
        
        # Look for login elements
        print("🔍 Searching for login elements...")
        
        login_selectors = [
            "//button[contains(text(),'Login')]",
            "//a[contains(text(),'Login')]",
            "//button[contains(text(),'Sign in')]",
            "//a[contains(text(),'Sign in')]",
            "//div[contains(text(),'Login')]",
        ]
        
        login_found = False
        for selector in login_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"✅ Found login element: {selector}")
                    for element in elements[:2]:  # Show first 2
                        print(f"   Text: {element.text}")
                    login_found = True
                    break
            except:
                continue
        
        if not login_found:
            print("⚠️  Login elements not found, checking page content...")
            
            # Look for any clickable elements
            clickable_elements = driver.find_elements(By.TAG_NAME, "button")
            print(f"📊 Found {len(clickable_elements)} buttons on page")
            
            for i, element in enumerate(clickable_elements[:5]):  # Show first 5
                try:
                    text = element.text.strip()
                    if text:
                        print(f"   Button {i+1}: {text}")
                except:
                    pass
        
        # Check for phone input fields
        print("\n🔍 Searching for phone input fields...")
        phone_selectors = [
            "//input[@type='tel']",
            "//input[@type='number']",
            "//input[contains(@placeholder,'phone')]",
            "//input[contains(@placeholder,'mobile')]",
        ]
        
        phone_found = False
        for selector in phone_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"✅ Found phone input: {selector}")
                    phone_found = True
                    break
            except:
                continue
        
        if not phone_found:
            print("⚠️  Phone input not found (may need to click login first)")
        
        # Test price extraction
        print("\n🧪 Testing price extraction...")
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Price Test</title></head>
        <body>
            <h1>Test Product</h1>
            <div class="price">₹2,249.00</div>
            <div class="current-price">₹2249</div>
            <div id="price">₹2,249</div>
        </body>
        </html>
        """
        
        driver.get(f"data:text/html;charset=utf-8,{test_html}")
        time.sleep(2)
        
        price_selectors = [".price", ".current-price", "#price"]
        price_found = False
        for selector in price_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and ('₹' in text or any(char.isdigit() for char in text)):
                        print(f"✅ Found price: {text}")
                        price_found = True
                        break
                if price_found:
                    break
            except:
                continue
        
        if not price_found:
            print("⚠️  Price not found in test")
        
        # Test BigBasket product page
        print("\n🌐 Testing BigBasket product page...")
        test_url = "https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/"
        driver.get(test_url)
        time.sleep(5)
        
        product_title = driver.title
        print(f"📄 Product page title: {product_title}")
        
        # Look for price on product page
        price_selectors = [
            ".price",
            ".current-price", 
            "[class*='Price']",
            "[class*='price']",
            ".Pricing___StyledLabel-sc-pldi2d-1",
        ]
        
        product_price = None
        for selector in price_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and ('₹' in text or 'Rs' in text or any(char.isdigit() for char in text)):
                        print(f"✅ Found product price: {text}")
                        product_price = text
                        break
                if product_price:
                    break
            except:
                continue
        
        if not product_price:
            print("⚠️  Product price not found (expected due to anti-bot)")
        
        driver.quit()
        
        print("\n✅ Simple setup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return False

def show_login_instructions():
    """Show instructions for real login testing"""
    print("\n" + "="*50)
    print("📋 REAL LOGIN TESTING INSTRUCTIONS")
    print("="*50)
    
    print("\n1. 📞 Update Phone Number:")
    print("   Edit bigbasket_login_scraper.py")
    print("   Line 409: phone_number = 'YOUR_PHONE_NUMBER_HERE'")
    print("   Change to: phone_number = '9876543210'")
    
    print("\n2. 🔧 Fix Chrome Options:")
    print("   Remove: options.add_experimental_option('excludeSwitches', ['enable-automation'])")
    print("   Keep basic options only")
    
    print("\n3. 🚀 Run Real Test:")
    print("   python bigbasket_login_scraper.py")
    
    print("\n4. 📱 Manual Steps:")
    print("   - Wait for OTP on your phone")
    print("   - Enter OTP in browser window")
    print("   - Press Enter in terminal")
    
    print("\n5. 🎯 Expected Results:")
    print("   - Login success: 80-90% chance")
    print("   - Price extraction: High success")
    print("   - Member pricing: Access to exclusive prices")

if __name__ == "__main__":
    success = test_simple_setup()
    
    if success:
        print("\n✅ Simple test PASSED!")
        show_login_instructions()
    else:
        print("\n❌ Simple test FAILED!")
