import os
import sys
import json

def validate_tokens():
    """Validate required tokens are available"""
    
    required_tokens = {
        'GH_TOKEN': 'GitHub token for API operations',
        'PUSHBULLET_TOKEN': 'Pushbullet token for notifications (optional)'
    }
    
    missing_tokens = []
    available_tokens = {}
    
    for token_name, description in required_tokens.items():
        token_value = os.getenv(token_name)
        if token_value:
            available_tokens[token_name] = {
                'value': token_value[:10] + '...' if len(token_value) > 10 else token_value,
                'description': description,
                'status': 'available'
            }
            print(f"✅ {token_name}: Available")
        else:
            missing_tokens.append(token_name)
            if token_name == 'PUSHBULLET_TOKEN':
                print(f"⚠️  {token_name}: Missing (optional - notifications disabled)")
            else:
                print(f"❌ {token_name}: Missing (required)")
    
    # Exit with error if required tokens are missing
    if 'GH_TOKEN' in missing_tokens:
        print("\n❌ ERROR: GH_TOKEN is required for GitHub operations")
        sys.exit(1)
    
    # Test GitHub token validity
    print("\n🔍 Testing GitHub token...")
    try:
        import requests
        headers = {'Authorization': f'token {os.getenv("GH_TOKEN")}'}
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub token valid (user: {user_data.get('login', 'unknown')})")
        else:
            print(f"❌ GitHub token invalid (status: {response.status_code})")
            sys.exit(1)
    except Exception as e:
        print(f"⚠️  Could not validate GitHub token: {e}")
        print("   Continuing anyway...")
    
    # Test Pushbullet token if available
    if 'PUSHBULLET_TOKEN' not in missing_tokens:
        print("\n🔍 Testing Pushbullet token...")
        try:
            headers = {'Access-Token': os.getenv('PUSHBULLET_TOKEN')}
            response = requests.get('https://api.pushbullet.com/v2/users/me', headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Pushbullet token valid")
            else:
                print(f"⚠️  Pushbullet token may be invalid (status: {response.status_code})")
        except Exception as e:
            print(f"⚠️  Could not validate Pushbullet token: {e}")
    
    print("\n✅ Token validation complete")
    return True

if __name__ == "__main__":
    validate_tokens()
