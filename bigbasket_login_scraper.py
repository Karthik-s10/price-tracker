#!/usr/bin/env python3
"""
BigBasket Scraper with Phone Number Login
Simulates real user login to bypass anti-bot protection
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import random
import re
import json

class BigBasketLoginScraper:
    def __init__(self, phone_number, pincode="560102"):
        self.phone_number = phone_number
        self.pincode = pincode
        self.driver = None
        self.logged_in = False
        
    def setup_driver(self):
        """Setup undetected Chrome driver with stealth"""
        options = uc.ChromeOptions()
        
        # Basic stealth options
        options.add_argument('--headless=False')  # Set to False to see browser
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Advanced anti-detection (simplified)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        try:
            self.driver = uc.Chrome(options=options)
            
            # Apply selenium-stealth
            stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            
            print("✅ Enhanced driver setup successful")
            return True
            
        except Exception as e:
            print(f"❌ Driver setup failed: {str(e)}")
            return False
    
    def human_like_delay(self, min_delay=1, max_delay=3):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_delay, max_delay))
    
    def login_with_phone(self):
        """Login to BigBasket using phone number"""
        try:
            print("🌐 Opening BigBasket login page...")
            self.driver.get("https://www.bigbasket.com/")
            self.human_like_delay(3, 5)
            
            # Look for login button
            login_selectors = [
                "//button[contains(text(),'Login')]",
                "//a[contains(text(),'Login')]",
                "//button[contains(@class,'login')]",
                "//div[contains(@class,'login')]",
                "//span[contains(text(),'Login')]",
                "//button[contains(text(),'Sign in')]",
                "//a[contains(text(),'Sign in')]",
            ]
            
            login_clicked = False
            for selector in login_selectors:
                try:
                    login_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    login_btn.click()
                    login_clicked = True
                    print(f"✅ Clicked login button: {selector}")
                    self.human_like_delay(2, 3)
                    break
                except:
                    continue
            
            if not login_clicked:
                print("❌ Could not find login button")
                return False
            
            # Enter phone number
            phone_input_selectors = [
                "//input[@type='tel']",
                "//input[@name='phone']",
                "//input[@placeholder='phone']",
                "//input[contains(@placeholder,'phone')]",
                "//input[contains(@placeholder,'mobile')]",
                "//input[@id='phone']",
                "//input[contains(@class,'phone')]",
                "//input[@type='number']",
            ]
            
            phone_entered = False
            for selector in phone_input_selectors:
                try:
                    phone_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    phone_input.clear()
                    # Type phone number like a human
                    for digit in self.phone_number:
                        phone_input.send_keys(digit)
                        time.sleep(random.uniform(0.1, 0.3))
                    
                    phone_entered = True
                    print(f"✅ Entered phone number via: {selector}")
                    self.human_like_delay(1, 2)
                    break
                except:
                    continue
            
            if not phone_entered:
                print("❌ Could not find phone input field")
                return False
            
            # Click continue/send OTP button
            otp_selectors = [
                "//button[contains(text(),'Continue')]",
                "//button[contains(text(),'Send OTP')]",
                "//button[contains(text(),'Get OTP')]",
                "//button[contains(text(),'Next')]",
                "//button[contains(text(),'Submit')]",
                "//button[@type='submit']",
                "//button[contains(@class,'submit')]",
            ]
            
            otp_clicked = False
            for selector in otp_selectors:
                try:
                    otp_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    otp_btn.click()
                    otp_clicked = True
                    print(f"✅ Clicked OTP button: {selector}")
                    self.human_like_delay(3, 5)
                    break
                except:
                    continue
            
            if not otp_clicked:
                print("❌ Could not find OTP button")
                return False
            
            print("📱 OTP sent to your phone")
            print("⚠️  You'll need to manually enter the OTP when prompted")
            print("💡 For automation, consider using BigBasket's API or commercial services")
            
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            return False
    
    def wait_for_manual_otp(self):
        """Wait for user to manually enter OTP"""
        print("\n" + "="*50)
        print("📱 MANUAL OTP REQUIRED")
        print("="*50)
        print(f"Phone: {self.phone_number}")
        print("1. Check your phone for OTP")
        print("2. Enter OTP in the browser")
        print("3. Press Enter here when logged in...")
        print("="*50)
        
        input("Press Enter after you've entered the OTP and logged in...")
        
        # Check if login was successful
        try:
            # Look for logged-in indicators
            login_indicators = [
                "//div[contains(@class,'user')]",
                "//span[contains(text(),'My Account')]",
                "//div[contains(text(),'Welcome')]",
                "//button[contains(text(),'Logout')]",
                "//a[contains(text(),'Logout')]",
            ]
            
            for selector in login_indicators:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    self.logged_in = True
                    print(f"✅ Login successful! Found: {selector}")
                    return True
                except:
                    continue
            
            print("❌ Could not confirm login status")
            return False
            
        except Exception as e:
            print(f"❌ Error checking login status: {str(e)}")
            return False
    
    def set_location(self):
        """Set delivery location/pincode"""
        if not self.logged_in:
            print("❌ Not logged in, cannot set location")
            return False
        
        try:
            print(f"🏪 Setting location for pincode: {self.pincode}")
            
            # Look for location settings
            location_selectors = [
                "//button[contains(text(),'Change Location')]",
                "//button[contains(text(),'Select Location')]",
                "//button[contains(text(),'Set Location')]",
                "//div[contains(@class,'location')]",
                "//a[contains(text(),'location')]",
                "//button[contains(@class,'location')]",
            ]
            
            location_clicked = False
            for selector in location_selectors:
                try:
                    location_btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    location_btn.click()
                    location_clicked = True
                    print(f"✅ Clicked location button: {selector}")
                    self.human_like_delay(2, 3)
                    break
                except:
                    continue
            
            if not location_clicked:
                print("⚠️  Could not find location button, trying direct pincode entry")
            
            # Enter pincode
            pincode_selectors = [
                "//input[@id='pincode']",
                "//input[@name='pincode']",
                "//input[@placeholder='pincode']",
                "//input[contains(@placeholder,'Pincode')]",
                "//input[@type='number']",
                "//input[contains(@class,'pincode')]",
            ]
            
            pincode_entered = False
            for selector in pincode_selectors:
                try:
                    pincode_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    pincode_input.clear()
                    pincode_input.send_keys(self.pincode)
                    pincode_entered = True
                    print(f"✅ Entered pincode via: {selector}")
                    self.human_like_delay(1, 2)
                    break
                except:
                    continue
            
            # Submit pincode
            if pincode_entered:
                submit_selectors = [
                    "//button[contains(text(),'Check')]",
                    "//button[contains(text(),'Submit')]",
                    "//button[contains(text(),'Apply')]",
                    "//button[contains(text(),'Continue')]",
                    "//button[@type='submit']",
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        submit_btn.click()
                        print(f"✅ Clicked submit button: {selector}")
                        self.human_like_delay(3, 5)
                        break
                    except:
                        continue
            
            print("✅ Location setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Location setup failed: {str(e)}")
            return False
    
    def scrape_product_price(self, url):
        """Scrape product price after login"""
        if not self.logged_in:
            print("❌ Not logged in, cannot scrape price")
            return None
        
        try:
            print(f"🛒 Scraping product: {url}")
            self.driver.get(url)
            self.human_like_delay(3, 5)
            
            # Find price using multiple methods
            price = self._find_price()
            
            if price:
                print(f"✅ Price found: ₹{price}")
                return price
            else:
                print("❌ Price not found")
                return None
                
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            return None
    
    def _find_price(self):
        """Find price using multiple methods"""
        price_selectors = [
            ".Pricing___StyledLabel-sc-pldi2d-1",
            ".price",
            ".current-price",
            "[data-testid='price']",
            "[class*='Price']",
            "[class*='price']",
            ".ProductPrice",
            ".ProductPriceView",
            ".MuiTypography-root",
            "[class*='MuiTypography']",
        ]
        
        for selector in price_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and ('₹' in text or 'Rs' in text or any(char.isdigit() for char in text)):
                        price = self._extract_price(text)
                        if price:
                            print(f"✅ Found price via {selector}: ₹{price}")
                            return price
            except:
                continue
        
        # Check page source as fallback
        page_source = self.driver.page_source
        price_patterns = [
            r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'Rs\.?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'"price":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
            r'"sellingPrice":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, page_source, re.IGNORECASE)
            if matches:
                for p in matches:
                    p = p.replace(',', '')
                    try:
                        price_val = float(p)
                        if 10 < price_val < 50000:
                            print(f"✅ Found price in source: ₹{price_val}")
                            return price_val
                    except:
                        continue
        
        return None
    
    def _extract_price(self, text):
        """Extract price from text"""
        price_match = re.search(r'(\d+(?:,\d{3})*(?:\.\d{2})?)', text.replace('₹', '').replace('Rs', '').replace(',', ''))
        if price_match:
            return float(price_match.group(1))
        return None
    
    def close(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()

def test_phone_login():
    """Test the phone login approach"""
    print("🧪 Testing BigBasket Phone Login Approach")
    print("="*50)
    
    # Replace with your actual phone number
    phone_number = "YOUR_PHONE_NUMBER_HERE"  # Format: 9876543210
    
    if phone_number == "YOUR_PHONE_NUMBER_HERE":
        print("⚠️  Please update the phone number in the script")
        print("   Edit line 285: phone_number = 'YOUR_ACTUAL_PHONE_NUMBER'")
        return False
    
    scraper = BigBasketLoginScraper(phone_number, pincode="560102")
    
    try:
        # Setup driver
        if not scraper.setup_driver():
            return False
        
        # Login with phone
        if not scraper.login_with_phone():
            return False
        
        # Wait for manual OTP
        if not scraper.wait_for_manual_otp():
            return False
        
        # Set location
        scraper.set_location()
        
        # Test product scraping
        test_url = "https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/"
        price = scraper.scrape_product_price(test_url)
        
        if price:
            print(f"🎉 SUCCESS! Price: ₹{price}")
            return True
        else:
            print("❌ Failed to get price")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        scraper.close()

if __name__ == "__main__":
    test_phone_login()
