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

# Make plotly optional
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not installed. Charts will be disabled. Install with: pip install plotly")

from price_tracker_universal import UniversalPriceTracker
import time

def pull_latest_config_from_github():
    """Pull latest config from GitHub API"""
    try:
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            return False, "GitHub token not found"
        
        url = 'https://api.github.com/repos/Karthik-s10/price-tracker/contents/price_tracker_config.json'
        r = requests.get(url, headers={'Authorization': f'token {token}'})
        
        if r.status_code == 200:
            data = r.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            
            # Save to local file
            with open('price_tracker_config.json', 'w') as f:
                f.write(content)
            
            # Reload tracker
            st.cache_resource.clear()
            return True, "Pulled latest config from GitHub"
        else:
            return False, f"Failed to fetch: {r.status_code}"
    except Exception as e:
        return False, str(e)

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

# Initialize tracker
@st.cache_resource
def get_tracker():
    return UniversalPriceTracker()

tracker = get_tracker()

# Sidebar
with st.sidebar:
    st.markdown("## 🎮 Control Panel")
    
    # Pushbullet status
    if tracker.pushbullet_token:
        st.success("✅ Pushbullet Connected")
    else:
        st.warning("⚠️ Pushbullet Not Configured")
        with st.expander("How to setup Pushbullet"):
            st.markdown("""
            1. Install Pushbullet app on phone
            2. Get token from https://www.pushbullet.com/#settings/account
            3. Set environment variable:
            ```bash
            export PUSHBULLET_TOKEN="your-token"
            ```
            """)
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Product", "📈 Price History", "⚙️ Settings"]
    )
    
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
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Check All Prices Now", use_container_width=True):
                with st.spinner("Checking prices..."):
                    tracker.check_all_products()
                st.success("✅ Prices updated!")
                st.rerun()
        
        with col2:
            total_notif = st.toggle("🔔 Global Notifications", value=tracker.notifications_enabled)
            if total_notif != tracker.notifications_enabled:
                tracker.notifications_enabled = total_notif
                tracker.save_config()
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
                            st.caption(f"🎯 Threshold: ₹{threshold:,.2f}")
                        
                        # Last checked
                        last_check = datetime.fromisoformat(latest['timestamp'])
                        st.caption(f"⏰ {last_check.strftime('%d %b, %I:%M %p')}")
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
                        # Pull latest config from GitHub first
                        with st.spinner("🔄 Syncing with GitHub..."):
                            success, message = pull_latest_config_from_github()
                            if success:
                                st.success(message)
                                # Reload tracker after pulling
                                tracker = get_tracker()
                            else:
                                st.warning(f"Could not sync: {message}")
                        
                        tracker.products[idx]['notifications_enabled'] = new_notif
                        tracker.save_config()
                        st.rerun()
                    
                    # Edit button
                    if st.button("✏️ Edit", key=f"edit_{idx}"):
                        st.session_state.editing_product = idx
                        st.session_state.page = "edit"
                        st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        if st.session_state.get(f'confirm_del_{idx}', False):
                            # Pull latest config from GitHub first
                            with st.spinner("🔄 Syncing with GitHub..."):
                                success, message = pull_latest_config_from_github()
                                if success:
                                    st.success(message)
                                    # Reload tracker after pulling
                                    tracker = get_tracker()
                                else:
                                    st.warning(f"Could not sync: {message}")
                            
                            tracker.products.pop(idx)
                            tracker.save_config()
                            st.success("Product deleted!")
                            st.rerun()
                        else:
                            st.session_state[f'confirm_del_{idx}'] = True
                            st.warning("Click again to confirm")
                
                # Price trend indicator
                if len(history) >= 2:
                    prev_price = history[-2]['price']
                    curr_price = history[-1]['price']
                    change = curr_price - prev_price
                    change_pct = (change / prev_price) * 100
                    
                    if change < 0:
                        st.success(f"📉 Price dropped by ₹{abs(change):.2f} ({abs(change_pct):.1f}%)")
                    elif change > 0:
                        st.error(f"📈 Price increased by ₹{change:.2f} ({change_pct:.1f}%)")
                    else:
                        st.info("➡️ Price unchanged")
                
                st.markdown('</div>', unsafe_allow_html=True)

elif page == "➕ Add Product":
    st.markdown('<h1 class="main-header">➕ Add New Product</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Track any product from **any e-commerce website**! Just paste the product URL below.
    
    ✅ Amazon | ✅ Flipkart | ✅ Myntra | ✅ Nykaa | ✅ BigBasket | ✅ Zepto | ✅ Any other site!
    """)
    
    with st.form("add_product_form"):
        st.markdown("### Product Details")
        
        url = st.text_input(
            "🔗 Product URL",
            placeholder="https://www.amazon.in/dp/B08CFSZLQ4/ or any other product link",
            help="Paste the complete URL of the product page"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "📦 Product Name",
                placeholder="e.g., Fire TV Stick, Nike Shoes, etc.",
                help="Give it a memorable name"
            )
        
        with col2:
            threshold = st.number_input(
                "💰 Price Threshold (₹)",
                min_value=0,
                value=2500,
                step=100,
                help="Get notified when price drops below this"
            )
        
        notifications_enabled = st.checkbox(
            "🔔 Enable notifications for this product",
            value=True,
            help="You can toggle this anytime from the dashboard"
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("✅ Add Product", use_container_width=True)
        
        if submitted:
            if not url:
                st.error("❌ Please enter a product URL")
            elif not name:
                st.error("❌ Please enter a product name")
            else:
                # Pull latest config from GitHub first
                with st.spinner("🔄 Syncing with GitHub..."):
                    success, message = pull_latest_config_from_github()
                    if success:
                        st.success(message)
                        # Reload tracker after pulling
                        tracker = get_tracker()
                    else:
                        st.warning(f"Could not sync: {message}")
                
                # Add product
                new_product = {
                    'url': url,
                    'name': name,
                    'threshold': threshold,
                    'platform': 'auto',
                    'notifications_enabled': notifications_enabled,
                    'added_date': datetime.now().isoformat()
                }
                
                tracker.products.append(new_product)
                tracker.save_config()
                # Get config content
                with open('price_tracker_config.json', 'r') as f:
                    content = f.read()
                
                # Push to GitHub via API
                try:
                    token = os.getenv('GITHUB_TOKEN')
                    if not token:
                        st.warning("⚠️ GITHUB_TOKEN not found in environment variables")
                        raise Exception("GitHub token missing")
                    
                    url = 'https://api.github.com/repos/Karthik-s10/price-tracker/contents/price_tracker_config.json'
                    
                    # Get current file SHA
                    r = requests.get(url, headers={'Authorization': f'token {token}'})
                    if r.status_code != 200:
                        st.error(f"❌ Failed to get current file: {r.status_code} - {r.text}")
                        raise Exception(f"GitHub API error: {r.status_code}")
                    
                    sha = r.json()['sha']
                    
                    # Update file
                    data = {
                        'message': 'Update from dashboard',
                        'content': base64.b64encode(content.encode()).decode(),
                        'sha': sha
                    }
                    r = requests.put(url, json=data, headers={'Authorization': f'token {token}'})
                    if r.status_code == 200:
                        st.success("✅ Synced to GitHub!")
                    else:
                        st.error(f"❌ Failed to update GitHub: {r.status_code} - {r.text}")
                        raise Exception(f"GitHub update failed: {r.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ GitHub sync failed: {str(e)}")
                    st.info("💡 You may need to add products manually via GitHub for now")
                
                st.success(f"✅ Added: {name}")
                st.balloons()
                
                # Test the price detection
                with st.spinner("🔍 Testing price detection..."):
                    result = tracker.scrape_price_universal(url)
                    
                    if 'error' in result:
                        st.warning(f"⚠️ Could not detect price: {result['error']}")
                        st.info("The product is saved. Price will be checked in the next scheduled run.")
                    else:
                        st.success(f"✅ Price detected: ₹{result['price']} using {result.get('method', 'unknown')} method")
                
                time.sleep(2)
                st.rerun()

elif page == "📈 Price History":
    st.markdown('<h1 class="main-header">📈 Price History</h1>', unsafe_allow_html=True)
    
    if not tracker.products:
        st.info("No products tracked yet. Add some products first!")
    else:
        # Product selector
        product_names = [p['name'] for p in tracker.products]
        selected_product = st.selectbox("Select Product", product_names)
        
        # Find selected product
        product = next(p for p in tracker.products if p['name'] == selected_product)
        history = tracker.price_history.get(product['url'], [])
        
        if not history:
            st.info(f"No price history for {selected_product} yet. Check prices to start tracking!")
        else:
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            prices = [h['price'] for h in history]
            current_price = prices[-1]
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            with col1:
                st.metric("Current Price", f"₹{current_price:,.2f}")
            
            with col2:
                st.metric("Lowest Price", f"₹{min_price:,.2f}", 
                         delta=f"-₹{current_price - min_price:.2f}" if current_price > min_price else "Best price!")
            
            with col3:
                st.metric("Highest Price", f"₹{max_price:,.2f}")
            
            with col4:
                st.metric("Average Price", f"₹{avg_price:,.2f}")
            
            # Price chart
            st.markdown("### 📊 Price Trend")
            
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if PLOTLY_AVAILABLE:
                fig = go.Figure()
                
                # Price line
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df['price'],
                    mode='lines+markers',
                    name='Price',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8)
                ))
                
                # Threshold line
                threshold = product.get('threshold', 0)
                if threshold > 0:
                    fig.add_hline(
                        y=threshold,
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"Your Threshold: ₹{threshold}",
                        annotation_position="right"
                    )
                
                fig.update_layout(
                    title="Price Over Time",
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Fallback: Simple line chart using Streamlit's built-in
                st.line_chart(df.set_index('timestamp')['price'])
                st.caption("Install plotly for interactive charts: pip install plotly")
            
            # Price history table
            st.markdown("### 📋 Detailed History")
            
            display_df = df.copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d %b %Y, %I:%M %p')
            display_df['price'] = display_df['price'].apply(lambda x: f"₹{x:,.2f}")
            display_df = display_df.rename(columns={
                'timestamp': 'Date & Time',
                'price': 'Price',
                'method': 'Detection Method'
            })
            
            st.dataframe(
                display_df[['Date & Time', 'Price', 'Detection Method']].iloc[::-1],
                use_container_width=True,
                hide_index=True
            )

elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    # Global settings
    st.markdown("### 🌐 Global Settings")
    
    with st.form("global_settings"):
        global_notif = st.toggle(
            "🔔 Enable all notifications",
            value=tracker.notifications_enabled,
            help="Master switch for all notifications"
        )
        
        st.markdown("---")
        st.markdown("### 📱 Pushbullet Configuration")
        
        if tracker.pushbullet_token:
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
            tracker.notifications_enabled = global_notif
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
            tracker.save_config()
            st.success("✅ All notifications enabled!")
            st.rerun()
    
    with col2:
        if st.button("🔕 Disable All Product Notifications", use_container_width=True):
            for product in tracker.products:
                product['notifications_enabled'] = False
            tracker.save_config()
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
                'notifications_enabled': tracker.notifications_enabled
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
                tracker.save_config()
                st.success("✅ Configuration imported!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error importing: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2rem;'>
    <p>🛒 Price Tracker Dashboard | Made with ❤️ using Streamlit</p>
    <p>Track prices from Amazon, Flipkart, Myntra, Nykaa, BigBasket, Zepto & more!</p>
</div>
""", unsafe_allow_html=True)
