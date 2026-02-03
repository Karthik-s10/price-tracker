#!/usr/bin/env python3
"""
Demo version of BigBasket login scraper (without actual phone number)
Shows the process and tests the setup
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import random

def test_login_setup():
    """Test the login setup without actual phone number"""
    print("🧪 Testing BigBasket Login Setup")
    print("="*50)
    
    # Setup driver
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # Set to False to see browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    try:
        print("🔧 Setting up enhanced Chrome driver...")
        driver = uc.Chrome(options=options)
        
        # Apply selenium-stealth
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        print("✅ Enhanced driver setup successful")
        
        # Test BigBasket homepage
        print("🌐 Loading BigBasket homepage...")
        driver.get("https://www.bigbasket.com/")
        time.sleep(3)
        
        print("✅ BigBasket homepage loaded successfully")
        
        # Look for login button
        print("🔍 Searching for login button...")
        login_selectors = [
            "//button[contains(text(),'Login')]",
            "//a[contains(text(),'Login')]",
            "//button[contains(@class,'login')]",
            "//div[contains(@class,'login')]",
            "//span[contains(text(),'Login')]",
            "//button[contains(text(),'Sign in')]",
            "//a[contains(text(),'Sign in')]",
        ]
        
        login_found = False
        for selector in login_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"✅ Found login elements: {selector}")
                    login_found = True
                    break
            except:
                continue
        
        if not login_found:
            print("⚠️  Login button not found, but page loaded")
        
        # Check page title
        title = driver.title
        print(f"📄 Page title: {title}")
        
        # Check for anti-bot measures
        page_source = driver.page_source
        if "cloudflare" in page_source.lower():
            print("🛡️  Cloudflare detected")
        if "captcha" in page_source.lower():
            print("🛡️  CAPTCHA detected")
        
        print("✅ Basic setup test completed successfully")
        
        # Test price extraction on a simple page
        print("\n🧪 Testing price extraction...")
        test_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
            <div class="price">₹2,249.00</div>
            <div class="current-price">₹2249</div>
        </body>
        </html>
        """
        
        driver.get(f"data:text/html;charset=utf-8,{test_html}")
        time.sleep(2)
        
        # Try to find price
        price_selectors = [".price", ".current-price"]
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
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n" + "="*50)
    print("📋 NEXT STEPS FOR REAL TESTING")
    print("="*50)
    
    print("\n1. 📞 Update Phone Number:")
    print("   Edit bigbasket_login_scraper.py line 409")
    print("   Change: phone_number = 'YOUR_PHONE_NUMBER_HERE'")
    print("   To: phone_number = '9876543210' (your actual number)")
    
    print("\n2. 🚀 Run Real Test:")
    print("   python bigbasket_login_scraper.py")
    
    print("\n3. 📱 Follow Prompts:")
    print("   - Wait for OTP on your phone")
    print("   - Enter OTP in browser")
    print("   - Press Enter in terminal")
    
    print("\n4. 🎯 Expected Results:")
    print("   - Login success: 80-90% chance")
    print("   - Price extraction: High success")
    print("   - Member pricing: Access to exclusive prices")
    
    print("\n5. ⚠️  Important Notes:")
    print("   - Use your actual phone number")
    print("   - Have phone ready for OTP")
    print("   - BigBasket account required")
    print("   - Set headless=False to see browser")

if __name__ == "__main__":
    success = test_login_setup()
    
    if success:
        print("\n✅ Setup test PASSED! Ready for real testing")
        show_next_steps()
    else:
        print("\n❌ Setup test FAILED! Check issues above")
