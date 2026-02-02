#!/usr/bin/env python3
"""
Quick test script to verify token configuration
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_github_token():
    """Test GitHub token"""
    token = os.getenv('GH_TOKEN')
    if not token:
        print("❌ GH_TOKEN not found in environment")
        return False
    
    print(f"🔍 Testing GH_TOKEN...")
    try:
        headers = {'Authorization': f'token {token}'}
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GH_TOKEN valid (user: {user_data.get('login', 'unknown')})")
            return True
        else:
            print(f"❌ GH_TOKEN invalid (status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing GH_TOKEN: {e}")
        return False

def test_pushbullet_token():
    """Test Pushbullet token"""
    token = os.getenv('PUSHBULLET_TOKEN')
    if not token:
        print("⚠️  PUSHBULLET_TOKEN not found (optional)")
        return True  # Optional, so return True
    
    print(f"🔍 Testing PUSHBULLET_TOKEN...")
    try:
        headers = {'Access-Token': token}
        response = requests.get('https://api.pushbullet.com/v2/users/me', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ PUSHBULLET_TOKEN valid")
            return True
        else:
            print(f"❌ PUSHBULLET_TOKEN invalid (status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing PUSHBULLET_TOKEN: {e}")
        return False

if __name__ == "__main__":
    print("🔑 Testing Token Configuration")
    print("=" * 40)
    
    github_ok = test_github_token()
    pushbullet_ok = test_pushbullet_token()
    
    print("\n" + "=" * 40)
    if github_ok:
        print("✅ All required tokens are working!")
    else:
        print("❌ Please fix GH_TOKEN to use GitHub features")
    
    if not pushbullet_ok:
        print("⚠️  Pushbullet notifications won't work (optional)")
