#!/usr/bin/env python3
"""
Test Selenium setup
"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_selenium():
    """Test basic Selenium functionality"""
    print("🔧 Testing Selenium setup...")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    
    try:
        print("🌐 Initializing Chrome driver...")
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver initialized successfully")
        
        print("🌐 Loading test page...")
        driver.get("https://httpbin.org/html")
        print("✅ Page loaded successfully")
        
        print("🔍 Looking for page content...")
        content = driver.find_element(By.TAG_NAME, "h1").text
        print(f"✅ Found content: {content}")
        
        driver.quit()
        print("✅ Selenium test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Selenium test failed: {str(e)}")
        try:
            driver.quit()
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_selenium()
    sys.exit(0 if success else 1)
