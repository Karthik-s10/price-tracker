#!/usr/bin/env python3
"""
UNIVERSAL Price Tracker - Works with ANY E-commerce Website
Automatically detects prices from any product page
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
from typing import Optional, Dict, List

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class UniversalPriceTracker:
    def __init__(self, config_file='price_tracker_config.json'):
        self.config_file = config_file
        self.products = []
        self.price_history = {}
        self.notifications_enabled = True
        self.load_config()
        
        self.pushbullet_token = os.getenv('PUSHBULLET_TOKEN', '')
        
        # Common price selectors for e-commerce sites
        self.price_selectors = [
            # Meta tags (most reliable)
            {'type': 'meta', 'attr': 'property', 'value': 'product:price:amount'},
            {'type': 'meta', 'attr': 'property', 'value': 'og:price:amount'},
            {'type': 'meta', 'attr': 'name', 'value': 'price'},
            {'type': 'meta', 'attr': 'property', 'value': 'price'},
            
            # Schema.org structured data
            {'type': 'script', 'attr': 'type', 'value': 'application/ld+json'},
            
            # Common CSS selectors
            {'type': 'css', 'selector': '.price'},
            {'type': 'css', 'selector': '.current-price'},
            {'type': 'css', 'selector': '.sale-price'},
            {'type': 'css', 'selector': '.product-price'},
            {'type': 'css', 'selector': '[data-price]'},
            {'type': 'css', 'selector': '.Price'},
            {'type': 'css', 'selector': '.pricing'},
            {'type': 'css', 'selector': '.amount'},
            {'type': 'css', 'selector': '.value'},
            
            # Amazon specific
            {'type': 'css', 'selector': '.a-price-whole'},
            {'type': 'css', 'selector': '.a-offscreen'},
            
            # Flipkart specific
            {'type': 'css', 'selector': '._30jeq3'},
            
            # BigBasket specific
            {'type': 'css', 'selector': '.Pricing___StyledLabel-sc-pldi2d-1'},
            
            # General patterns
            {'type': 'css', 'selector': '[class*="price"]'},
            {'type': 'css', 'selector': '[id*="price"]'},
            {'type': 'css', 'selector': 'span[class*="Price"]'},
            {'type': 'css', 'selector': 'div[class*="price"]'},
        ]
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.products = config.get('products', [])
                    self.price_history = config.get('price_history', {})
                    self.notifications_enabled = config.get('notifications_enabled', True)
                    if 'pincode' in config:
                        self.pincode = config['pincode']
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            config = {
                'products': self.products,
                'price_history': self.price_history,
                'notifications_enabled': self.notifications_enabled,
                'pincode': getattr(self, 'pincode', '')
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def extract_price_from_text(self, text):
        """Extract numeric price from text"""
        if not text:
            return None
        
        # Remove currency symbols and whitespace
        text = text.strip()
        text = re.sub(r'[₹$€£¥,]', '', text)
        
        # Find price patterns
        patterns = [
            r'(\d+\.?\d*)',  # Basic number
            r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)',  # Price range
            r'(\d+\.?\d*)\s*to\s*(\d+\.?\d*)',  # Price range with "to"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # For ranges, take the lower price
                price = float(match.group(1))
                if price > 0:
                    return price
        
        return None
    
    def scrape_price_universal(self, url):
        """Scrape price using multiple methods"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different methods to find price
            price = None
            currency = '₹'
            
            # Method 1: Meta tags
            for selector in self.price_selectors:
                if selector['type'] == 'meta':
                    meta_tags = soup.find_all('meta')
                    for tag in meta_tags:
                        if tag.get(selector['attr']) == selector['value']:
                            content = tag.get('content', '')
                            price = self.extract_price_from_text(content)
                            if price:
                                break
                if price:
                    break
            
            # Method 2: Schema.org JSON-LD
            if not price:
                scripts = soup.find_all('script', type='application/ld+json')
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, list):
                            data = data[0]
                        
                        # Look for price in various fields
                        price_fields = ['price', 'offers', 'highPrice', 'lowPrice']
                        for field in price_fields:
                            if field in data:
                                if isinstance(data[field], (int, float)):
                                    price = float(data[field])
                                elif isinstance(data[field], dict) and 'price' in data[field]:
                                    price = float(data[field]['price'])
                                elif isinstance(data[field], str):
                                    price = self.extract_price_from_text(data[field])
                                if price:
                                    break
                        
                        # Check in offers array
                        if not price and 'offers' in data:
                            offers = data['offers']
                            if isinstance(offers, list):
                                for offer in offers:
                                    if 'price' in offer:
                                        price = float(offer['price'])
                                        break
                            elif isinstance(offers, dict) and 'price' in offers:
                                price = float(offers['price'])
                        
                        if price:
                            break
                    except:
                        continue
            
            # Method 3: CSS selectors
            if not price:
                for selector in self.price_selectors:
                    if selector['type'] == 'css':
                        elements = soup.select(selector['selector'])
                        for element in elements:
                            text = element.get_text(strip=True)
                            price = self.extract_price_from_text(text)
                            if price:
                                break
                    if price:
                        break
            
            # Method 4: Look for price patterns in all text
            if not price:
                all_text = soup.get_text()
                # Look for price patterns with currency symbols
                price_patterns = [
                    r'₹\s*(\d+\.?\d*)',
                    r'Rs\.?\s*(\d+\.?\d*)',
                    r'(\d+\.?\d*)\s*₹',
                    r'(\d+\.?\d*)\s*Rs\.?',
                ]
                
                for pattern in price_patterns:
                    matches = re.findall(pattern, all_text, re.IGNORECASE)
                    if matches:
                        prices = [float(p) for p in matches if float(p) > 0]
                        if prices:
                            # Take the most reasonable price (not too high or too low)
                            prices = [p for p in prices if 1 < p < 100000]
                            if prices:
                                price = min(prices)  # Take lowest reasonable price
                                break
            
            if price:
                return {'price': price, 'currency': currency, 'available': True}
            else:
                return {'error': 'Price not found', 'available': False}
                
        except Exception as e:
            return {'error': str(e), 'available': False}
    
    def scrape_bigbasket_with_pincode(self, url, pincode):
        """Scrape BigBasket with pincode using Selenium"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Use chromium-browser for GitHub Actions
        options.binary_location = '/usr/bin/chromium-browser'
        
        try:
            driver = webdriver.Chrome(options=options)
            
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Try to find and click location/change button
            location_selectors = [
                "//button[contains(text(),'Change')]",
                "//button[contains(text(),'Select Location')]",
                "//div[contains(text(),'Change')]",
                "//span[contains(text(),'Change')]",
                "//a[contains(text(),'Change')]",
                "//button[contains(@class,'location')]",
                "//div[contains(@class,'location')]"
            ]
            
            location_clicked = False
            for selector in location_selectors:
                try:
                    location_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    location_btn.click()
                    location_clicked = True
                    break
                except:
                    continue
            
            if not location_clicked:
                # Try to find pincode input directly
                pass
            
            # Look for pincode input
            pincode_selectors = [
                "//input[@id='pincode']",
                "//input[@name='pincode']",
                "//input[@placeholder='pincode']",
                "//input[contains(@placeholder,'Pincode')]",
                "//input[contains(@placeholder,'PIN')]",
                "//input[@type='number']",
                "//input[contains(@class,'pincode')]"
            ]
            
            pincode_entered = False
            for selector in pincode_selectors:
                try:
                    pincode_input = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    pincode_input.clear()
                    pincode_input.send_keys(pincode)
                    pincode_entered = True
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
                    "//input[@type='submit']"
                ]
                
                for selector in submit_selectors:
                    try:
                        submit_btn = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        submit_btn.click()
                        break
                    except:
                        continue
            
            # Wait for price to update
            time.sleep(5)
            
            # Try to find price
            price_selectors = [
                ".Pricing___StyledLabel-sc-pldi2d-1",
                "[class*='Price']",
                "[class*='price']",
                ".price",
                ".current-price",
                ".product-price"
            ]
            
            price = None
            for selector in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text
                    price = self.extract_price_from_text(price_text)
                    if price:
                        break
                except:
                    continue
            
            if not price:
                # Try to get price from page source
                page_source = driver.page_source
                price = self.extract_price_from_text(page_source)
            
            driver.quit()
            
            if price:
                return {'price': price, 'currency': '₹', 'available': True}
            else:
                return {'error': 'Price not found after pincode update', 'available': False}
                
        except Exception as e:
            try:
                driver.quit()
            except:
                pass
            return {'error': f'Selenium error: {str(e)}', 'available': False}
    
    def scrape_with_selenium(self, url):
        """Scrape price using Selenium for any website"""
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Try to initialize driver
            print("🔧 Initializing Chrome driver...")
            driver = webdriver.Chrome(options=options)
            
            # Hide webdriver signature
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set realistic user agent
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            print(f"🌐 Loading URL: {url}")
            driver.get(url)
            
            # Wait for page to load
            time.sleep(5)
            print("✅ Page loaded")
            
            # Try to find price using multiple selectors
            price = None
            currency = '₹'
            
            # Method 1: Try all price selectors
            print("🔍 Searching for price using CSS selectors...")
            for selector in self.price_selectors:
                if selector['type'] == 'css':
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector['selector'])
                        for element in elements:
                            text = element.text.strip()
                            price = self.extract_price_from_text(text)
                            if price:
                                print(f"✅ Found price via selector: {selector['selector']} - ₹{price}")
                                break
                        if price:
                            break
                    except Exception as e:
                        continue
                elif selector['type'] == 'meta':
                    try:
                        meta_tags = driver.find_elements(By.TAG_NAME, 'meta')
                        for tag in meta_tags:
                            if tag.get_attribute(selector['attr']) == selector['value']:
                                content = tag.get_attribute('content', '')
                                price = self.extract_price_from_text(content)
                                if price:
                                    print(f"✅ Found price via meta: {selector['value']} - ₹{price}")
                                    break
                        if price:
                            break
                    except:
                        continue
            
            # Method 2: Look for price in page source
            if not price:
                print("🔍 Searching for price in page source...")
                page_source = driver.page_source
                # Look for price patterns with currency symbols
                price_patterns = [
                    r'₹\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                    r'Rs\.?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                    r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*₹',
                    r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*Rs\.?',
                    r'"price":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
                    r'"currentPrice":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
                    r'"salePrice":\s*"?(\d+(?:,\d{3})*(?:\.\d{2})?)"?',
                    r'data-asin-price="([^"]+)"',
                    r'data-price="([^"]+)"',
                    r'priceWhole["\s:]+["\s]*(\d+(?:,\d{3})*)',
                    r'priceFraction["\s:]+["\s]*(\d+)',
                ]
                
                for pattern in price_patterns:
                    matches = re.findall(pattern, page_source, re.IGNORECASE)
                    if matches:
                        prices = []
                        for p in matches:
                            # Clean up the price string
                            p = p.replace(',', '')
                            try:
                                price_val = float(p)
                                if 1 < price_val < 100000:  # Reasonable price range
                                    prices.append(price_val)
                            except:
                                continue
                        
                        if prices:
                            price = min(prices)  # Take lowest reasonable price
                            print(f"✅ Found price via pattern matching: ₹{price}")
                            break
            
            # Method 3: Try common price element IDs and classes
            if not price:
                print("🔍 Searching for price using common selectors...")
                common_selectors = [
                    "#price",
                    "#productPrice",
                    "#salePrice",
                    "#currentPrice",
                    ".price",
                    ".product-price",
                    ".sale-price",
                    ".current-price",
                    "[data-price]",
                    "[data-testid*='price']",
                    "[class*='Price']",
                    "[class*='price']",
                    "span[class*='price']",
                    "div[class*='price']",
                    "h1[class*='price']",
                    "h2[class*='price']",
                    "h3[class*='price']",
                    ".a-price-whole",
                    ".a-price-fraction",
                    ".a-offscreen",
                    "[id*='price']",
                    "[aria-label*='price']",
                ]
                
                for selector in common_selectors:
                    try:
                        element = driver.find_element(By.CSS_SELECTOR, selector)
                        text = element.text.strip()
                        price = self.extract_price_from_text(text)
                        if price:
                            print(f"✅ Found price via common selector: {selector} - ₹{price}")
                            break
                    except:
                        continue
            
            driver.quit()
            
            if price:
                return {'price': price, 'currency': currency, 'available': True}
            else:
                return {'error': 'Price not found with Selenium', 'available': False}
                
        except Exception as e:
            try:
                driver.quit()
            except:
                pass
            error_msg = f'Selenium scraping error: {str(e)}'
            print(f"❌ {error_msg}")
            return {'error': error_msg, 'available': False}
    
    def check_product_price(self, product):
        """Check price for a single product using Selenium"""
        url = product['url']
        name = product['name']
        
        print(f"\n🔍 Checking: {name}")
        print(f"📍 URL: {url}")
        
        # Always use Selenium for consistency in GitHub Actions
        if 'bigbasket.com' in url.lower() and hasattr(self, 'pincode') and self.pincode:
            print(f"🏪 BigBasket detected, using pincode: {self.pincode}")
            result = self.scrape_bigbasket_with_pincode(url, self.pincode)
        else:
            print(f"🌐 Using Selenium for price extraction")
            result = self.scrape_with_selenium(url)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return None
        else:
            price = result['price']
            print(f"💰 Price: ₹{price}")
            return price
    
    def send_notification(self, message: str, title: str = "Price Alert"):
        """Send notification via Pushbullet"""
        if not self.notifications_enabled:
            print(f"\n🔕 Notifications OFF - Alert suppressed")
            return
        
        if not self.pushbullet_token:
            print(f"\n📱 NOTIFICATION (Pushbullet not configured):")
            print(f"   {title}")
            print(f"   {message}\n")
            return
        
        try:
            url = 'https://api.pushbullet.com/v2/pushes'
            headers = {
                'Access-Token': self.pushbullet_token,
                'Content-Type': 'application/json'
            }
            data = {
                'type': 'note',
                'title': title,
                'body': message
            }
            
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"\n📱 Pushbullet notification sent!")
            else:
                print(f"\n❌ Pushbullet error: {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Notification error: {e}")
    
    def check_all_prices(self):
        """Check prices for all products"""
        print(f"\n{'='*70}")
        print(f"🛒 PRICE TRACKER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        print(f"\n📊 Configuration:")
        print(f"   Products: {len(self.products)}")
        print(f"   Pushbullet: {'✅' if self.pushbullet_token else '❌'}")
        print(f"   Notifications: {'🔔 ON' if self.notifications_enabled else '🔕 OFF'}")
        print(f"   Pincode: {getattr(self, 'pincode', 'Not set')}")
        
        if not self.products:
            print("\n⚠️  No products in config file!")
            return
        
        price_changes = []
        
        for product in self.products:
            price = self.check_product_price(product)
            
            if price:
                product['current_price'] = price
                product['last_checked'] = datetime.now().isoformat()
                
                # Update price history
                if product['name'] not in self.price_history:
                    self.price_history[product['name']] = []
                
                self.price_history[product['name']].append({
                    'price': price,
                    'date': datetime.now().isoformat()
                })
                
                # Check for price changes
                target_price = product.get('target_price')
                if target_price and price <= target_price:
                    message = f"🎯 Target Price Alert!\n\n{product['name']}\nCurrent: ₹{price}\nTarget: ₹{target_price}\n\n{product['url']}"
                    self.send_notification(message, f"Target Price Reached: {product['name']}")
                    price_changes.append(f"🎯 {product['name']}: ₹{price} (Target: ₹{target_price})")
                
                # Check for significant price drops
                if len(self.price_history[product['name']]) > 1:
                    prev_price = self.price_history[product['name']][-2]['price']
                    if price < prev_price:
                        drop_percent = ((prev_price - price) / prev_price) * 100
                        if drop_percent >= 5:  # 5% or more drop
                            message = f"📉 Price Drop Alert!\n\n{product['name']}\nPrevious: ₹{prev_price}\nCurrent: ₹{price}\nDrop: {drop_percent:.1f}%\n\n{product['url']}"
                            self.send_notification(message, f"Price Drop: {product['name']}")
                            price_changes.append(f"📉 {product['name']}: ₹{price} (↓{drop_percent:.1f}%)")
        
        # Save updated configuration
        self.save_config()
        
        # Summary
        print(f"\n{'='*70}")
        if price_changes:
            print(f"🔔 ALERTS: {len(price_changes)} price changes detected!")
            for change in price_changes:
                print(f"   {change}")
        else:
            print(f"✅ No significant price changes detected")
        print(f"{'='*70}\n")

def main():
    tracker = UniversalPriceTracker()
    tracker.check_all_prices()

if __name__ == "__main__":
    main()
