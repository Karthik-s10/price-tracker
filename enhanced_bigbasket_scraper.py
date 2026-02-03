#!/usr/bin/env python3
"""
Enhanced BigBasket Scraper with Advanced Anti-Detection Techniques
Based on 2024 research for bypassing modern bot detection
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import random
import re

class EnhancedBigBasketScraper:
    def __init__(self, pincode="560102"):
        self.pincode = pincode
        self.driver = None
        
    def setup_driver(self):
        """Setup undetected Chrome driver with stealth"""
        options = uc.ChromeOptions()
        
        # Basic stealth options
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Advanced anti-detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        try:
            # Use undetected chromedriver
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
    
    def scrape_bigbasket_product(self, url):
        """Scrape BigBasket product with enhanced techniques"""
        if not self.setup_driver():
            return None
        
        try:
            print(f"🌐 Loading BigBasket product: {url}")
            self.driver.get(url)
            self.human_like_delay(3, 5)
            
            # First try to find price without location
            price = self._find_price()
            
            # If no price, try to set location
            if not price:
                print("🏪 Setting location for pincode:", self.pincode)
                if self._set_location():
                    self.human_like_delay(3, 5)
                    price = self._find_price()
            
            self.driver.quit()
            return price
            
        except Exception as e:
            try:
                self.driver.quit()
            except:
                pass
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
    
    def _set_location(self):
        """Set location with pincode"""
        location_selectors = [
            "//button[contains(text(),'Change')]",
            "//button[contains(text(),'Select Location')]",
            "//button[contains(@class,'location')]",
            "//div[contains(@class,'location')]",
        ]
        
        for selector in location_selectors:
            try:
                location_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                location_btn.click()
                self.human_like_delay(1, 2)
                
                # Enter pincode
                pincode_input = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='number'] | //input[contains(@placeholder,'pincode')]"))
                )
                pincode_input.clear()
                pincode_input.send_keys(self.pincode)
                self.human_like_delay(0.5, 1)
                
                # Submit
                submit_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Check') or contains(text(),'Submit') or contains(text(),'Apply')]"))
                )
                submit_btn.click()
                self.human_like_delay(2, 3)
                
                print("✅ Location set successfully")
                return True
                
            except:
                continue
        
        return False

def test_enhanced_scraper():
    """Test the enhanced scraper"""
    print("🧪 Testing Enhanced BigBasket Scraper")
    print("="*50)
    
    scraper = EnhancedBigBasketScraper(pincode="560102")
    
    test_url = "https://www.bigbasket.com/pd/40326186/the-whole-truth-cold-coffee-pro-whey-protein-powder-1-kg/"
    
    price = scraper.scrape_bigbasket_product(test_url)
    
    if price:
        print(f"✅ SUCCESS! Price found: ₹{price}")
        return True
    else:
        print("❌ FAILED! Could not retrieve price")
        return False

if __name__ == "__main__":
    test_enhanced_scraper()
