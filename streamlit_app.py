#!/usr/bin/env python3
"""
Streamlit Web Interface for Price Tracker
Beautiful UI to manage products, view history, and control notifications
"""

import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import requests
import base64
import time

# Make plotly optional
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from price_tracker_universal import UniversalPriceTracker
from token_manager import validate_tokens_for_streamlit

# --- HELPER FUNCTIONS ---

def pull_latest_config_from_github():
    """Pull latest config from GitHub API"""
    try:
        # Use enhanced token detection (same as token_manager)
        token = None
        try:
            token = st.secrets["GH_TOKEN"]
        except (KeyError, FileNotFoundError):
            pass
        
        if not token:
            token = os.getenv('GH_TOKEN')
        
        if not token:
            print("Warning: GH_TOKEN not found. Skipping pull.")
            return False, "GitHub token not found"
        
        url = 'https://api.github.com/repos/Karthik-s10/price-tracker/contents/price_tracker_config.json'
        r = requests.get(url, headers={'Authorization': f'token {token}'})
        
        if r.status_code == 200:
            data = r.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            
            # Save to local file
            with open('price_tracker_config.json', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Reload tracker
            st.cache_resource.clear()
            return True, "Pulled latest config from GitHub"
        else:
            return False, f"Failed to fetch: {r.status_code}"
    except Exception as e:
        return False, str(e)

def push_config_to_github(message="Update config from Streamlit"):
    """Push local config file to GitHub to save changes permanently"""
    try:
        # Use enhanced token detection (same as token_manager)
        token = None
        try:
            token = st.secrets["GH_TOKEN"]
        except (KeyError, FileNotFoundError):
            pass
        
        if not token:
            token = os.getenv('GH_TOKEN')
        
        if not token:
            print("Warning: GH_TOKEN not found. Skipping push.")
            return False, "GH_TOKEN missing"
        
        # Read local file
        with open('price_tracker_config.json', 'r', encoding='utf-8') as f:
            content = f.read()
            
        url = 'https://api.github.com/repos/Karthik-s10/price-tracker/contents/price_tracker_config.json'
        headers = {'Authorization': f'token {token}'}
        
        # Get current SHA (Required to update file)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return False, f"GitHub Error: {r.status_code}"
            
        sha = r.json()['sha']
        
        # Push update
        data = {
            'message': message,
            'content': base64.b64encode(content.encode()).decode(),
            'sha': sha
        }
        
        r = requests.put(url, json=data, headers=headers)
        if r.status_code == 200:
            return True, "✅ Changes saved to GitHub!"
        else:
            return False, f"❌ Push failed: {r.status_code}"
            
    except Exception as e:
        return False, str(e)

@st.cache_resource
def get_tracker():
    # FIX: Initialize without arguments to match your price_tracker_universal.py
    return UniversalPriceTracker()

def main():
    # Page config
    st.set_page_config(
        page_title="Price Tracker Dashboard",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 1rem 0;
        }
        .product-card {
            background: #f7fafc;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv is optional

    # Initialize tracker
    tracker = get_tracker()

    # Sidebar
    with st.sidebar:
        st.markdown("## 🎮 Control Panel")
        
        st.markdown("### 🔌 System Health")
        
        # 1. GitHub Token Check (Real API Test)
        token = None
        try:
            token = st.secrets["GH_TOKEN"]
        except (KeyError, FileNotFoundError):
            pass
        
        if not token:
            token = os.getenv('GH_TOKEN')
            
        if token:
            try:
                r = requests.get('https://api.github.com/user', headers={'Authorization': f'token {token}'})
                if r.status_code == 200:
                    st.success(f"✅ GitHub: Active ({r.json()['login']})")
                else:
                    st.error(f"❌ GitHub: Invalid Token ({r.status_code})")
            except:
                 st.error("❌ GitHub: Connection Failed")
        else:
             st.warning("⚠️ GitHub: Token Missing (Check Secrets)")

        # 2. Pushbullet Token Check (Real API Test)
        pb_token = None
        try:
            pb_token = st.secrets["PUSHBULLET_TOKEN"]
        except (KeyError, FileNotFoundError):
            pass
        
        if not pb_token:
            pb_token = os.getenv("PUSHBULLET_TOKEN")

        if pb_token:
            try:
                r = requests.get('https://api.pushbullet.com/v2/users/me', headers={'Access-Token': pb_token})
                if r.status_code == 200:
                    st.success(f"✅ Pushbullet: Active")
                else:
                    st.error(f"❌ Pushbullet: Invalid Token (401)")
            except:
                st.error("❌ Pushbullet: Connection Failed")
        else:
            st.info("ℹ️ Pushbullet: Not Configured (Optional)")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["📊 Dashboard", "➕ Add Product", "📈 Price History", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Pincode Input
        st.markdown("### 📍 Delivery Pincode")
        # Handle pincode safely whether it exists in tracker or not
        current_pincode = getattr(tracker, 'pincode', '')
        pincode = st.text_input("Enter your pincode", value=current_pincode or "", max_chars=6, key="pincode_input")
        
        # Update pincode if changed
        if pincode and pincode != current_pincode:
            tracker.pincode = pincode
            if hasattr(tracker, 'save_config'):
                tracker.save_config()
            # Push changes to GitHub
            with st.spinner("Saving pincode to GitHub..."):
                success, msg = push_config_to_github(f"Update pincode to {pincode}")
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Products", len(tracker.products))
        
        active_notifications = sum(1 for p in tracker.products if p.get('notifications_enabled', True))
        st.metric("Active Alerts", active_notifications)
        
        if st.button("🔄 Refresh Data"):
            st.cache_resource.clear()
            st.rerun()

    # Main content
    if page == "📊 Dashboard":
        st.markdown('<h1 class="main-header">🛒 Price Tracker Dashboard</h1>', unsafe_allow_html=True)
        
        if not tracker.products:
            st.info("👋 Welcome! Add your first product to start tracking prices.")
            st.markdown("Click **➕ Add Product** in the sidebar to get started.")
        else:
            # Pincode status
            if not getattr(tracker, 'pincode', None):
                st.warning("⚠️ Please set your delivery pincode in the sidebar for accurate pricing")
            else:
                st.info(f"📍 Prices will be shown for pincode: **{tracker.pincode}**")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔍 Check All Prices Now", use_container_width=True):
                    with st.spinner("Checking prices..."):
                        tracker.check_all_products()
                        # Push updated prices to GitHub
                        push_config_to_github("Updated prices via Dashboard")
                    st.success("✅ Prices updated & Saved!")
                    st.rerun()
            
            with col2:
                # Handle notifications safely
                current_notif = getattr(tracker, 'notifications_enabled', True)
                total_notif = st.toggle("🔔 Global Notifications", value=current_notif)
                if total_notif != current_notif:
                    tracker.notifications_enabled = total_notif
                    if hasattr(tracker, 'save_config'):
                        tracker.save_config()
                    push_config_to_github(f"Global notifications set to {total_notif}")
                    st.rerun()
            
            # Products list
            st.markdown("### 📦 Your Products")
            
            for idx, product in enumerate(tracker.products):
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"### {product['name']}")
                        st.caption(f"🔗 {product['url'][:60]}...")
                    
                    with col2:
                        # Get latest price
                        history = tracker.price_history.get(product['url'], [])
                        if history:
                            latest = history[-1]
                            current_price = latest['price']
                            threshold = product.get('threshold', 0)
                            
                            # Price display with color coding
                            if current_price < threshold:
                                st.markdown(f"### 💚 ₹{current_price:,.2f}")
                                st.caption(f"🎯 Below threshold (₹{threshold:,.2f})")
                            else:
                                st.markdown(f"### ₹{current_price:,.2f}")
                                st.caption(f"🎯 Threshold: ₹{threshold:,.2f})")
                            
                            # Last checked
                            try:
                                last_check = datetime.fromisoformat(latest['timestamp'])
                                st.caption(f"⏰ {last_check.strftime('%d %b, %I:%M %p')}")
                            except:
                                st.caption("⏰ Just now")
                        else:
                            st.info("Not checked yet")
                    
                    with col3:
                        # Individual notification toggle
                        notif_enabled = product.get('notifications_enabled', True)
                        new_notif = st.toggle(
                            "🔔 Alerts",
                            value=notif_enabled,
                            key=f"notif_{idx}"
                        )
                        
                        if new_notif != notif_enabled:
                            tracker.products[idx]['notifications_enabled'] = new_notif
                            tracker.save_config()
                            push_config_to_github(f"Toggle notification for {product['name']}")
                            st.rerun()
                    
                    # Delete button (FIXED: Now pushes to GitHub)
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        if st.session_state.get(f'confirm_del_{idx}', False):
                            # Pull latest config first to avoid conflicts
                            with st.spinner("🔄 Syncing..."):
                                pull_latest_config_from_github()
                                tracker = get_tracker() # Reload
                                
                                # Remove product
                                try:
                                    tracker.products.pop(idx)
                                    tracker.save_config()
                                    
                                    # Push changes to GitHub (CRITICAL FIX)
                                    success, msg = push_config_to_github(f"Deleted product: {product['name']}")
                                    
                                    if success:
                                        st.success("✅ Product deleted and synced to GitHub!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Deleted locally but GitHub sync failed: {msg}")
                                except IndexError:
                                    st.error("Error: Product list changed. Please refresh.")
                        else:
                            st.session_state[f'confirm_del_{idx}'] = True
                            st.warning("Click again to confirm")
                
                # Price trend indicator
                if len(history) >= 2:
                    prev_price = history[-2]['price']
                    curr_price = history[-1]['price']
                    change = curr_price - prev_price
                    change_pct = (change / prev_price) * 100 if prev_price else 0
                    
                    if change < 0:
                        st.success(f"📉 Price dropped by ₹{abs(change):.2f} ({abs(change_pct):.1f}%)")
                    elif change > 0:
                        st.error(f"📈 Price increased by ₹{change:.2f} ({change_pct:.1f}%)")
                    else:
                        st.info("➡️ Price unchanged")
                
                st.markdown('</div>', unsafe_allow_html=True)

    elif page == "➕ Add Product":
        st.markdown('<h1 class="main-header">➕ Add New Product</h1>', unsafe_allow_html=True)
        
        with st.form("add_product_form"):
            st.markdown("### Product Details")
            url = st.text_input("🔗 Product URL")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("📦 Product Name")
            with col2:
                threshold = st.number_input("💰 Price Threshold (₹)", min_value=0, value=2500)
            
            submitted = st.form_submit_button("✅ Add Product", use_container_width=True)
            
            if submitted:
                if not url or not name:
                    st.error("❌ Please enter URL and Name")
                else:
                    with st.spinner("🔄 Syncing with GitHub..."):
                        pull_latest_config_from_github()
                        tracker = get_tracker()
                    
                    new_product = {
                        'url': url,
                        'name': name,
                        'threshold': threshold,
                        'platform': 'auto',
                        'notifications_enabled': True,
                        'added_date': datetime.now().isoformat()
                    }
                    
                    tracker.products.append(new_product)
                    tracker.save_config()
                    
                    # Push to GitHub using helper
                    with st.spinner("💾 Saving to GitHub..."):
                        success, msg = push_config_to_github(f"Added product: {name}")
                        
                    if success:
                        st.success(f"✅ Added {name} and synced to GitHub!")
                        st.balloons()
                        # Initial price check
                        with st.spinner("🔍 Checking initial price..."):
                            tracker.scrape_price_universal(url)
                            # Push the price result too
                            push_config_to_github("Initial price check")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to sync: {msg}")

    elif page == "📈 Price History":
        st.markdown('<h1 class="main-header">📈 Price History</h1>', unsafe_allow_html=True)
        # (Keeping existing Price History logic, just ensuring it loads correctly)
        if not tracker.products:
            st.info("No products tracked yet.")
        else:
            product_names = [p['name'] for p in tracker.products]
            selected_product = st.selectbox("Select Product", product_names)
            try:
                product = next(p for p in tracker.products if p['name'] == selected_product)
                history = tracker.price_history.get(product['url'], [])
                
                if history:
                    df = pd.DataFrame(history)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    st.line_chart(df.set_index('timestamp')['price'])
                    st.dataframe(df)
                    st.info("No price history available for this product.")
            except StopIteration:
                st.error("Product not found.")

    elif page == "⚙️ Settings":
        st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
        
        # Global settings
        st.markdown("### 🌐 Global Settings")
        
        with st.form("global_settings"):
            global_notif = st.toggle(
                "🔔 Enable all notifications",
                value=getattr(tracker, 'notifications_enabled', True),
                help="Master switch for all notifications"
            )
            
            st.markdown("---")
            st.markdown("### 📍 Location Settings")
            
            # Get current pincode from config
            current_pincode = getattr(tracker, 'pincode', '560102')
            
            new_pincode = st.text_input(
                "📍 Pincode for price checking",
                value=current_pincode,
                max_chars=6,
                help="Enter your 6-digit pincode to get accurate local prices for quick commerce apps (Zepto, Blinkit, BigBasket)",
                placeholder="e.g., 560102"
            )
            
            # Validate pincode format
            if new_pincode and (not new_pincode.isdigit() or len(new_pincode) != 6):
                st.error("⚠️ Please enter a valid 6-digit pincode")
            
            st.markdown("---")
            st.markdown("### 📱 Pushbullet Configuration")
            
            if hasattr(tracker, 'pushbullet_token') and tracker.pushbullet_token:
                st.success("✅ Pushbullet is configured")
                st.code(f"Token: {tracker.pushbullet_token[:20]}...")
            else:
                st.warning("⚠️ Pushbullet not configured")
                st.markdown("""
                To receive notifications on your phone:
                
                1. Install Pushbullet app
                   - Android: [Play Store](https://play.google.com/store/apps/details?id=com.pushbullet.android)
                   - iOS: [App Store](https://apps.apple.com/app/pushbullet/id810352052)
                
                2. Get your Access Token:
                   - Go to https://www.pushbullet.com/#settings/account
                   - Click "Create Access Token"
                   - Copy the token
                
                3. Set environment variable:
                ```bash
                export PUSHBULLET_TOKEN="your-token-here"
                ```
                
                4. Restart the Streamlit app
                """)
            
            if st.form_submit_button("💾 Save Settings"):
                # Validate pincode before saving
                if new_pincode and (not new_pincode.isdigit() or len(new_pincode) != 6):
                    st.error("⚠️ Please fix the pincode format before saving")
                else:
                    tracker.notifications_enabled = global_notif
                    
                    # Update pincode in config
                    if hasattr(tracker, 'pincode') or new_pincode:
                        tracker.pincode = new_pincode
                    
                    if hasattr(tracker, 'save_config'):
                        tracker.save_config()
                    st.success("✅ Settings saved!")
                    st.rerun()
        
        st.markdown("---")
        
        # Bulk actions
        st.markdown("### 🔧 Bulk Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔔 Enable All Product Notifications", use_container_width=True):
                for product in tracker.products:
                    product['notifications_enabled'] = True
                if hasattr(tracker, 'save_config'):
                    tracker.save_config()
                    push_config_to_github("Enabled all notifications")
                st.success("✅ All notifications enabled!")
                st.rerun()
        
        with col2:
            if st.button("🔕 Disable All Product Notifications", use_container_width=True):
                for product in tracker.products:
                    product['notifications_enabled'] = False
                if hasattr(tracker, 'save_config'):
                    tracker.save_config()
                    push_config_to_github("Disabled all notifications")
                st.success("✅ All notifications disabled!")
                st.rerun()
        
        st.markdown("---")
        
        # Export/Import
        st.markdown("### 💾 Backup & Restore")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Configuration", use_container_width=True):
                config = {
                    'products': tracker.products,
                    'price_history': tracker.price_history,
                    'notifications_enabled': getattr(tracker, 'notifications_enabled', True),
                    'pincode': getattr(tracker, 'pincode', '560102')
                }
                st.download_button(
                    label="⬇️ Download Config File",
                    data=json.dumps(config, indent=2),
                    file_name="price_tracker_backup.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            uploaded_file = st.file_uploader("📤 Import Configuration", type=['json'])
            if uploaded_file is not None:
                try:
                    config = json.load(uploaded_file)
                    tracker.products = config.get('products', [])
                    tracker.price_history = config.get('price_history', {})
                    tracker.notifications_enabled = config.get('notifications_enabled', True)
                    if 'pincode' in config:
                        tracker.pincode = config['pincode']
                    if hasattr(tracker, 'save_config'):
                        tracker.save_config()
                        push_config_to_github("Imported configuration")
                    st.success("✅ Configuration imported and synced to GitHub!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error importing: {e}")
        
        st.markdown("---")
        
        # Current configuration display
        st.markdown("### 📊 Current Configuration")
        st.json({
            "Pincode": getattr(tracker, 'pincode', 'Not Set'),
            "Notifications": getattr(tracker, 'notifications_enabled', True),
            "Product Count": len(tracker.products),
            "Pushbullet": "Configured" if (hasattr(tracker, 'pushbullet_token') and tracker.pushbullet_token) else "Not Configured"
        })
        
        if st.button("💾 Force Save to GitHub", use_container_width=True):
             success, msg = push_config_to_github("Manual force save")
             if success: 
                 st.success(msg)
             else: 
                 st.error(msg)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #718096; padding: 2rem;'>
        <p>🛒 Price Tracker Dashboard | Made with ❤️ using Streamlit</p>
        <p>Track prices from Amazon, Flipkart, Myntra, Nykaa, BigBasket, Zepto & more!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()