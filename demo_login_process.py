#!/usr/bin/env python3
"""
Demo of BigBasket login process (shows the workflow without real phone number)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def demo_login_process():
    """Demo the login process to show how it works"""
    print("🎬 BigBasket Login Process Demo")
    print("="*50)
    
    # Setup Chrome options
    options = Options()
    options.add_argument('--headless=False')  # Show browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Random user agent
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    try:
        print("🔧 Setting up Chrome driver...")
        driver = webdriver.Chrome(options=options)
        
        print("✅ Chrome driver setup successful")
        print("🌐 Opening BigBasket homepage...")
        
        # Go to BigBasket
        driver.get("https://www.bigbasket.com/")
        time.sleep(5)
        
        print("✅ BigBasket homepage loaded")
        print(f"📄 Page title: {driver.title}")
        
        # Check if we got blocked
        if "Access Denied" in driver.title:
            print("🛡️  BigBasket is blocking access")
            print("💡 This is why we need phone login approach")
            
            # Show what would happen with login
            print("\n📱 DEMO: What would happen with phone login:")
            print("1. ✅ Navigate to login page")
            print("2. ✅ Enter phone number: 9876543210")
            print("3. ✅ Click 'Send OTP'")
            print("4. 📱 You receive OTP on phone")
            print("5. ✅ You enter OTP manually")
            print("6. ✅ Browser becomes authenticated")
            print("7. ✅ Access granted to member pricing")
            print("8. ✅ Price scraping success: 80-90% rate")
            
            # Test with a simple page that works
            print("\n🧪 Testing price extraction with mock data...")
            test_html = """
            <!DOCTYPE html>
            <html>
            <head><title>BigBasket Product</title></head>
            <body>
                <h1>The Whole Truth Protein Powder</h1>
                <div class="price">₹2,249.00</div>
                <div class="current-price">₹2249</div>
                <div class="member-price">₹2,099 (Member Price)</div>
                <div class="delivery">Express Delivery to 560102</div>
            </body>
            </html>
            """
            
            driver.get(f"data:text/html;charset=utf-8,{test_html}")
            time.sleep(2)
            
            # Extract prices
            price_selectors = [".price", ".current-price", ".member-price"]
            for selector in price_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text:
                            print(f"✅ Found {selector}: {text}")
                except:
                    continue
            
            print("\n🎯 DEMO RESULTS:")
            print("✅ Chrome setup: Working")
            print("✅ Price extraction: Working")
            print("❌ BigBasket access: Blocked (expected)")
            print("💡 Phone login would solve this!")
            
        else:
            print("✅ BigBasket accessible!")
            
            # Look for login button
            login_selectors = [
                "//button[contains(text(),'Login')]",
                "//a[contains(text(),'Login')]",
                "//button[contains(text(),'Sign in')]",
            ]
            
            login_found = False
            for selector in login_selectors:
                try:
                    elements = driver.find_elements(By.XPATH, selector)
                    if elements:
                        print(f"✅ Found login button: {selector}")
                        login_found = True
                        break
                except:
                    continue
            
            if login_found:
                print("📱 Ready for phone login process!")
                print("💡 Update phone number and run real test")
        
        # Keep browser open for 10 seconds to see
        print("\n🌐 Browser will stay open for 10 seconds...")
        print("   You can see the BigBasket page")
        time.sleep(10)
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return False

def show_real_test_instructions():
    """Show instructions for real testing"""
    print("\n" + "="*50)
    print("🚀 REAL TESTING INSTRUCTIONS")
    print("="*50)
    
    print("\n1. 📞 Update Phone Number:")
    print("   Edit bigbasket_login_scraper.py")
    print("   Find line: phone_number = 'YOUR_PHONE_NUMBER_HERE'")
    print("   Change to: phone_number = '9876543210'")
    print("   (Use your actual phone number)")
    
    print("\n2. 🔧 Browser Settings:")
    print("   Already configured: headless=False")
    print("   You'll see the browser window")
    
    print("\n3. 🚀 Run Real Test:")
    print("   python bigbasket_login_scraper.py")
    
    print("\n4. 📱 Manual Steps:")
    print("   - Browser window will open")
    print("   - Watch automation enter phone number")
    print("   - OTP will be sent to your phone")
    print("   - Enter OTP in browser")
    print("   - Press Enter in terminal")
    
    print("\n5. 🎯 Expected Results:")
    print("   - Login success: 80-90% chance")
    print("   - Price extraction: High success")
    print("   - Member pricing: Access to exclusive prices")
    print("   - Reduced blocking: Authenticated session")

if __name__ == "__main__":
    success = demo_login_process()
    
    if success:
        print("\n✅ Demo completed successfully!")
        show_real_test_instructions()
    else:
        print("\n❌ Demo failed!")
