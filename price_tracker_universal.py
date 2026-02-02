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
            
            # Common class names
            {'type': 'class', 'value': 'price'},
            {'type': 'class', 'value': 'product-price'},
            {'type': 'class', 'value': 'selling-price'},
            {'type': 'class', 'value': 'discounted-price'},
            {'type': 'class', 'value': 'sale-price'},
            {'type': 'class', 'value': 'final-price'},
            {'type': 'class', 'value': 'current-price'},
            {'type': 'class', 'value': 'offer-price'},
            
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
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.products = data.get('products', [])
                self.price_history = data.get('price_history', {})
                self.notifications_enabled = data.get('notifications_enabled', True)
        else:
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        data = {
            'products': self.products,
            'price_history': self.price_history,
            'notifications_enabled': self.notifications_enabled
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
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
    
    def scrape_price_universal(self, url: str) -> Dict:
        """Universal price scraper - works with any e-commerce site"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
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
    
    tracker = UniversalPriceTracker()
    
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
