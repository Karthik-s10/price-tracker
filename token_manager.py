import os
import sys
import requests
import json
import streamlit as st
from typing import Dict, Tuple, Optional

class TokenManager:
    """Manages and validates tokens across the application"""
    
    def __init__(self):
        self.tokens = {}
        self.validation_results = {}
    
    def get_token(self, token_name: str) -> Optional[str]:
        """Get token from multiple sources with priority"""
        # Priority 1: Streamlit secrets (for deployed app)
        try:
            token = st.secrets[token_name]
            if token:
                return token
        except (KeyError, FileNotFoundError):
            pass
        
        # Priority 2: Environment variables (for GitHub Actions/local)
        token = os.getenv(token_name)
        if token:
            return token
        
        return None
    
    def validate_github_token(self, token: str) -> Tuple[bool, str]:
        """Validate GitHub token"""
        try:
            headers = {'Authorization': f'token {token}'}
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return True, f"Valid (user: {user_data.get('login', 'unknown')})"
            else:
                return False, f"Invalid (status: {response.status_code})"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def validate_pushbullet_token(self, token: str) -> Tuple[bool, str]:
        """Validate Pushbullet token"""
        try:
            headers = {'Access-Token': token}
            response = requests.get('https://api.pushbullet.com/v2/users/me', headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True, "Valid"
            else:
                return False, f"Invalid (status: {response.status_code})"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def validate_all_tokens(self) -> Dict[str, Dict]:
        """Validate all required tokens"""
        results = {}
        
        # GitHub Token (Required)
        gh_token = self.get_token('GH_TOKEN')
        if gh_token:
            is_valid, message = self.validate_github_token(gh_token)
            results['GH_TOKEN'] = {
                'available': True,
                'valid': is_valid,
                'message': message,
                'required': True
            }
        else:
            results['GH_TOKEN'] = {
                'available': False,
                'valid': False,
                'message': 'Missing',
                'required': True
            }
        
        # Pushbullet Token (Optional)
        pb_token = self.get_token('PUSHBULLET_TOKEN')
        if pb_token:
            is_valid, message = self.validate_pushbullet_token(pb_token)
            results['PUSHBULLET_TOKEN'] = {
                'available': True,
                'valid': is_valid,
                'message': message,
                'required': False
            }
        else:
            results['PUSHBULLET_TOKEN'] = {
                'available': False,
                'valid': False,
                'message': 'Missing (optional)',
                'required': False
            }
        
        self.validation_results = results
        return results
    
    def check_required_tokens(self) -> bool:
        """Check if all required tokens are available and valid"""
        results = self.validate_all_tokens()
        
        for token_name, result in results.items():
            if result['required'] and (not result['available'] or not result['valid']):
                return False
        return True
    
    def get_status_summary(self) -> str:
        """Get a human-readable status summary"""
        results = self.validate_all_tokens()
        status_lines = []
        
        for token_name, result in results.items():
            icon = "✅" if result['available'] and result['valid'] else "❌" if result['required'] else "⚠️"
            status = f"{icon} {token_name}: {result['message']}"
            status_lines.append(status)
        
        return "\n".join(status_lines)
    
    def save_validation_log(self, filename: str = "token_validation.json"):
        """Save validation results to file"""
        with open(filename, 'w') as f:
            json.dump(self.validation_results, f, indent=2)

# Global instance
token_manager = TokenManager()

def validate_tokens_for_streamlit():
    """Validate tokens and return results for Streamlit display"""
    results = token_manager.validate_all_tokens()
    
    # Check if any required tokens are missing
    missing_required = [
        name for name, result in results.items() 
        if result['required'] and (not result['available'] or not result['valid'])
    ]
    
    return {
        'results': results,
        'all_valid': len(missing_required) == 0,
        'missing_required': missing_required,
        'summary': token_manager.get_status_summary()
    }

if __name__ == "__main__":
    # Command line validation
    results = token_manager.validate_all_tokens()
    print(token_manager.get_status_summary())
    
    # Exit with error if required tokens are missing
    if not token_manager.check_required_tokens():
        print("\n❌ Required tokens are missing or invalid")
        sys.exit(1)
    else:
        print("\n✅ All required tokens are valid")
