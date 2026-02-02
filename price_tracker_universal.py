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

class UniversalPriceTracker:
    def __init__(self, config_file='price_tracker_config.json', pushbullet_token=None):
        self.config_file = os.path.expanduser(config_file)  # Allow ~/ paths
        self.products = []
        self.price_history = {}
        self.notifications_enabled = True
        self.pincode = None
        self.pushbullet_token = pushbullet_token or os.getenv('PUSHBULLET_TOKEN', '')
        # Load Cookies for Amazon/Flipkart (Crucial for correct pincode pricing)
        self.cookies = os.getenv('ECOMMERCE_COOKIES', '')
        
        # Create config directory if it doesn't exist
        config_dir = os.path.dirname(os.path.abspath(self.config_file))
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            
        # Set restrictive permissions on config directory
        if os.name != 'nt':  # Skip on Windows
            try:
                os.chmod(config_dir, 0o700)
            except Exception as e:
                print(f"Warning: Could not set permissions on {config_dir}: {e}")
        
        self.load_config()
        
        # Common price selectors for e-commerce sites
        self.price_selectors = [
            # Meta tags (most reliable)
            {'type': 'meta', 'attr': 'property', 'value': 'product:price:amount'},
            {'type': 'meta', 'attr': 'property', 'value': 'og:price:amount'},
            {'type': 'meta', 'attr': 'name', 'value': 'price'},
            
            # Common class names
            {'type': 'class', 'value': 'price'},
            {'type': 'class', 'value': 'product-price'},
            {'type': 'class', 'value': 'selling-price'},
            {'type': 'class', 'value': 'discounted-price'},
            {'type': 'class', 'value': 'sale-price'},
            {'type': 'class', 'value': 'final-price'},
            {'type': 'class', 'value': 'current-price'},
            {'type': 'class', 'value': 'offer-price'},
            {'type': 'class', 'value': 'a-price-whole'}, # Amazon specific
            
            # ID selectors
            {'type': 'id', 'value': 'price'},
            {'type': 'id', 'value': 'product-price'},
            
            # Data attributes
            {'type': 'data', 'attr': 'data-price'},
            {'type': 'data', 'attr': 'data-product-price'},
        ]
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.products = data.get('products', [])
                self.price_history = data.get('price_history', {})
                self.notifications_enabled = data.get('notifications_enabled', True)
                self.pincode = data.get('pincode')  # Load saved pincode
        else:
            self.save_config()
    
    def save_config(self):
        """Save configuration to file with secure permissions"""
        data = {
            'products': self.products,
            'price_history': self.price_history,
            'notifications_enabled': self.notifications_enabled,
            'pincode': self.pincode
        }
        
        # Create a temporary file first
        temp_file = f"{self.config_file}.tmp"
        
        try:
            # Write to temporary file
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # On Unix-like systems, set restrictive permissions (0o600 = owner read/write only)
            if os.name != 'nt':  # Skip on Windows
                os.chmod(temp_file, 0o600)
                
            # Replace the old file with the new one
            if os.path.exists(self.config_file):
                os.replace(temp_file, self.config_file)
            else:
                os.rename(temp_file, self.config_file)
                
        except Exception as e:
            # Clean up temp file if something went wrong
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise Exception(f"Failed to save config: {str(e)}")
    
    def extract_price_from_text(self, text: str) -> Optional[float]:
        """Extract price from text string"""
        # Remove common currency symbols and text
        text = text.replace('₹', '').replace('Rs', '').replace('INR', '')
        text = text.replace('$', '').replace('USD', '')
        text = text.replace(',', '')  # Remove thousands separator
        
        # Find all numbers (including decimals)
        matches = re.findall(r'\d+\.?\d*', text)
        
        if matches:
            # Return the first number found
            try:
                return float(matches[0])
            except:
                return None
        return None
    
    def _extract_bigbasket_price(self, url: str, headers: dict) -> Optional[float]:
        """Extract price from BigBasket with pincode support"""
        try:
            # Extract product ID from URL
            product_id = None
            if '/p/' in url:
                product_id = url.split('/p/')[-1].split('/')[0].split('?')[0]
            
            if not product_id:
                return None
                
            # Use BigBasket's API to get pincode-specific pricing
            api_url = f'https://www.bigbasket.com/product/v-0.0.3/price/{product_id}/?pincode={self.pincode}'
            
            api_headers = headers.copy()
            api_headers.update({
                'X-CSRFToken': 'null',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': url
            })
            
            response = requests.get(api_url, headers=api_headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract price from API response
            if 'discounted_price' in data and data['discounted_price'] > 0:
                return float(data['discounted_price'])
            elif 'mrp' in data and data['mrp'] > 0:
                return float(data['mrp'])
                
        except Exception as e:
            print(f"Error fetching BigBasket price: {str(e)}")
            
        return None

    def _extract_zepto_price(self, url: str, headers: dict) -> Optional[float]:
        """Extract price from Zepto with pincode support"""
        try:
            # Extract product slug from URL
            slug = url.strip('/').split('/')[-1].split('?')[0]
            
            # First, get store ID for the pincode
            location_url = f'https://www.zeptonow.com/api/oms/v1/location/check-pincode?pincode={self.pincode}'
            location_headers = headers.copy()
            location_headers.update({
                'X-Zepto-Platform': 'web',
                'X-Zepto-Device-Id': 'web',
                'X-Zepto-Platform-Version': '1.0.0'
            })
            
            # Get location details
            location_resp = requests.get(location_url, headers=location_headers, timeout=10)
            location_resp.raise_for_status()
            location_data = location_resp.json()
            
            if not location_data.get('success', False):
                print("Zepto not available in this pincode")
                return None
                
            # Get product details
            product_url = f'https://www.zeptonow.com/api/oms/v1/products/{slug}?pincode={self.pincode}'
            product_resp = requests.get(product_url, headers=location_headers, timeout=10)
            product_resp.raise_for_status()
            product_data = product_resp.json()
            
            # Extract price
            if product_data.get('success', False) and 'data' in product_data:
                price = product_data['data'].get('price', {}).get('price')
                if price:
                    return float(price)
                    
        except Exception as e:
            print(f"Error fetching Zepto price: {str(e)}")
            
        return None

    def _extract_blinkit_price(self, url: str, headers: dict) -> Optional[float]:
        """Extract price from Blinkit with pincode support"""
        try:
            # Extract product ID from URL
            product_id = url.strip('/').split('/')[-1].split('?')[0]
            
            # First, get store ID for the pincode
            location_url = f'https://blinkit.com/api/v1/serviceability?pincode={self.pincode}'
            
            location_resp = requests.get(location_url, headers=headers, timeout=10)
            location_resp.raise_for_status()
            location_data = location_resp.json()
            
            store_id = location_data.get('data', {}).get('store_id')
            if not store_id:
                print("Blinkit not available in this pincode")
                return None
                
            # Get product details
            product_url = f'https://blinkit.com/api/v1/products/{product_id}?store_id={store_id}'
            product_resp = requests.get(product_url, headers=headers, timeout=10)
            product_resp.raise_for_status()
            product_data = product_resp.json()
            
            # Extract price
            if product_data.get('success', False) and 'data' in product_data:
                price = product_data['data'].get('price')
                if price:
                    return float(price)
                    
        except Exception as e:
            print(f"Error fetching Blinkit price: {str(e)}")
            
        return None

    def scrape_price_universal(self, url: str) -> Dict:
        """Universal price scraper - works with any e-commerce site"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/'
        }
        
        # INJECT USER COOKIES (Crucial for Amazon/Flipkart Pincode detection)
        if self.cookies:
            headers['Cookie'] = self.cookies
        
        # Check for pincode-requiring sites first
        if self.pincode:
            if 'bigbasket.com' in url:
                price = self._extract_bigbasket_price(url, headers)
                if price is not None:
                    return {'price': price, 'currency': 'INR', 'method': 'bigbasket_api'}
            
            elif 'zeptonow.com' in url:
                price = self._extract_zepto_price(url, headers)
                if price is not None:
                    return {'price': price, 'currency': 'INR', 'method': 'zepto_api'}
            
            elif 'blinkit.com' in url:
                price = self._extract_blinkit_price(url, headers)
                if price is not None:
                    return {'price': price, 'currency': 'INR', 'method': 'blinkit_api'}
        
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            price = None
            method_used = None
            
            # Method 1: Try meta tags first (most reliable)
            for selector in [s for s in self.price_selectors if s['type'] == 'meta']:
                meta = soup.find('meta', {selector['attr']: selector['value']})
                if meta and meta.get('content'):
                    price = self.extract_price_from_text(meta['content'])
                    if price:
                        method_used = f"meta[{selector['value']}]"
                        break
            
            # Method 2: Try JSON-LD structured data
            if not price:
                scripts = soup.find_all('script', {'type': 'application/ld+json'})
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        # Handle both single object and list
                        if isinstance(data, list):
                            data = data[0] if data else {}
                        
                        # Check for price in offers
                        if 'offers' in data:
                            offers = data['offers']
                            if isinstance(offers, dict):
                                price_text = offers.get('price', '')
                            elif isinstance(offers, list) and offers:
                                price_text = offers[0].get('price', '')
                            else:
                                price_text = ''
                            
                            price = self.extract_price_from_text(str(price_text))
                            if price:
                                method_used = "JSON-LD"
                                break
                    except:
                        continue
            
            # Method 3: Try common class selectors
            if not price:
                for selector in [s for s in self.price_selectors if s['type'] == 'class']:
                    # Try exact class match
                    elements = soup.find_all(class_=selector['value'])
                    for elem in elements:
                        text = elem.get_text().strip()
                        price = self.extract_price_from_text(text)
                        if price:
                            method_used = f"class='{selector['value']}'"
                            break
                    
                    # Try partial class match (class contains)
                    if not price:
                        elements = soup.find_all(class_=lambda x: x and selector['value'] in x.lower())
                        for elem in elements:
                            text = elem.get_text().strip()
                            price = self.extract_price_from_text(text)
                            if price:
                                method_used = f"class*='{selector['value']}'"
                                break
                    
                    if price:
                        break
            
            # Method 4: Try ID selectors
            if not price:
                for selector in [s for s in self.price_selectors if s['type'] == 'id']:
                    elem = soup.find(id=selector['value'])
                    if elem:
                        text = elem.get_text().strip()
                        price = self.extract_price_from_text(text)
                        if price:
                            method_used = f"id='{selector['value']}'"
                            break
            
            # Method 5: Try data attributes
            if not price:
                for selector in [s for s in self.price_selectors if s['type'] == 'data']:
                    elem = soup.find(attrs={selector['attr']: True})
                    if elem:
                        price_text = elem.get(selector['attr'], '')
                        price = self.extract_price_from_text(str(price_text))
                        if price:
                            method_used = f"{selector['attr']}"
                            break
            
            # Method 6: Aggressive search - find all elements with currency symbols
            if not price:
                # Look for ₹, Rs, or number patterns
                all_text = soup.find_all(string=re.compile(r'[₹Rs]\s*\d+|INR\s*\d+|\d+\.\d{2}'))
                for text in all_text:
                    price = self.extract_price_from_text(text)
                    if price and price > 10:  # Reasonable price filter
                        method_used = "currency_pattern"
                        break
            
            if price:
                return {
                    'price': price,
                    'currency': '₹',
                    'available': True,
                    'timestamp': datetime.now().isoformat(),
                    'method': method_used
                }
            else:
                return {
                    'error': 'Price not found with any method',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def check_product_price(self, product: Dict) -> Optional[float]:
        """Check price for a single product"""
        print(f"\n🔍 Checking: {product['name']}")
        print(f"   URL: {product['url'][:60]}...")
        
        # Check if notifications are enabled for THIS specific product
        product_notifications = product.get('notifications_enabled', True)
        print(f"   🔔 Notifications: {'ON' if product_notifications else 'OFF'}")
        
        result = self.scrape_price_universal(product['url'])
        
        if 'error' in result:
            print(f"   ⚠️  Error: {result['error']}")
            return None
        
        price = result['price']
        method = result.get('method', 'unknown')
        print(f"   💰 Current Price: ₹{price}")
        print(f"   🎯 Your Threshold: ₹{product.get('threshold', 0)}")
        print(f"   🔧 Detection method: {method}")
        
        # Store in history
        product_id = product['url']
        if product_id not in self.price_history:
            self.price_history[product_id] = []
        
        self.price_history[product_id].append({
            'price': price,
            'timestamp': result['timestamp'],
            'method': method
        })
        
        # Keep only last 100 entries per product
        if len(self.price_history[product_id]) > 100:
            self.price_history[product_id] = self.price_history[product_id][-100:]
        
        # Smart notification logic
        threshold = product.get('threshold', 0)
        if threshold > 0 and price < threshold:
            should_notify = False
            notification_reason = ""
            
            # Get previous prices
            history = self.price_history[product_id]
            if len(history) >= 2:
                prev_price = history[-2]['price']
                
                # Scenario 1: First time dropping below threshold
                if prev_price >= threshold:
                    should_notify = True
                    notification_reason = "FIRST DROP BELOW THRESHOLD"
                    print(f"   🚨 ALERT: Price just dropped below threshold!")
                
                # Scenario 2: ANY price drop below threshold
                elif prev_price < threshold and price < prev_price:
                    should_notify = True
                    price_drop = prev_price - price
                    price_drop_pct = (price_drop / prev_price) * 100
                
            else:
                # First check ever
                should_notify = True
                notification_reason = "INITIAL CHECK - BELOW THRESHOLD"
                print(f"   🚨 ALERT: First check shows price below threshold!")
            
            # Send notification if needed
            if should_notify and product_notifications and self.notifications_enabled:
                savings = threshold - price
                message = (
                    f"🎉 PRICE DROP ALERT!\n\n"
                    f"{product['name']}\n"
                    f"Current: ₹{price}\n"
                    f"Threshold: ₹{threshold}\n"
                    f"Savings: ₹{savings:.2f}\n"
                    f"Reason: {notification_reason}\n\n"
                    f"Buy now: {product['url']}"
                )
                self.send_notification(message, f"Price Alert: {product['name']}")
            elif not should_notify:
                print(f"   🔕 No notification: Price still low but no significant change")
            elif not product_notifications or not self.notifications_enabled:
                print(f"   🔕 Price below threshold but notifications OFF")
        elif price < threshold:
            print(f"   ✅ Price is below threshold (₹{threshold})")
        else:
            print(f"   ℹ️  Price above threshold (₹{threshold})")
        
        self.save_config()
        return price
    
    def check_all_products(self):
        """Check prices for all products"""
        print(f"\n{'='*70}")
        print(f"🛒 Price Check Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        print(f"📦 Products to check: {len(self.products)}")
        print(f"🔔 Notifications: {'ON' if self.notifications_enabled else 'OFF'}")
        
        if not self.products:
            print("\n⚠️  No products configured!")
            return
        
        for i, product in enumerate(self.products, 1):
            print(f"\n--- Product {i}/{len(self.products)} ---")
            self.check_product_price(product)
            
            # Be polite - don't hammer servers
            if i < len(self.products):
                import time
                time.sleep(3)
        
        print(f"\n{'='*70}")
        print(f"✅ Price Check Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
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
                print(f"   ✅ Notification sent to phone!")
            else:
                print(f"   ⚠️  Failed to send: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Notification error: {e}")


def main():
    """Main function for cloud execution"""
    print("\n" + "="*70)
    print("🌐 UNIVERSAL PRICE TRACKER")
    print("="*70)
    
    # Load environment from .env if it exists
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize with environment variables
    tracker = UniversalPriceTracker(
        config_file=os.getenv('CONFIG_FILE', 'price_tracker_config.json'),
        pushbullet_token=os.getenv('PUSHBULLET_TOKEN', '')
    )
    
    print(f"\n📊 Configuration:")
    print(f"   Products: {len(tracker.products)}")
    print(f"   Pushbullet: {'✅' if tracker.pushbullet_token else '❌'}")
    print(f"   Notifications: {'🔔 ON' if tracker.notifications_enabled else '🔕 OFF'}")
    
    if not tracker.pushbullet_token:
        print("\n⚠️  Set PUSHBULLET_TOKEN environment variable for phone notifications")
    
    if not tracker.products:
        print("\n⚠️  No products in config file!")
        print("   Add products to price_tracker_config.json")
        return
    
    tracker.check_all_products()


if __name__ == '__main__':
    main()
