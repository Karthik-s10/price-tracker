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
import time

# Make plotly optional
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from price_tracker_universal import UniversalPriceTracker

# --- HELPER FUNCTIONS ---

@st.cache_resource
def get_tracker():
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
    </style>
    """, unsafe_allow_html=True)

    # Initialize tracker
    tracker = get_tracker()

    # Sidebar
    st.sidebar.markdown("## 🎮 Control Panel")
    
    # Pushbullet status
    if hasattr(tracker, 'pushbullet_token') and tracker.pushbullet_token:
        st.sidebar.success("📱 Pushbullet: Connected")
    else:
        st.sidebar.info("📱 Pushbullet: Not Configured")

    # Navigation
    page = st.sidebar.selectbox("Navigate", [
        "📊 Dashboard", 
        "➕ Add Product", 
        "📈 Price History", 
        "⚙️ Settings"
    ])

    # Dashboard
    if page == "📊 Dashboard":
        st.markdown('<h1 class="main-header">🛒 Price Tracker</h1>', unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Products", len(tracker.products))
        with col2:
            st.metric("Notifications", "🔔 ON" if tracker.notifications_enabled else "🔕 OFF")
        with col3:
            if hasattr(tracker, 'pincode') and tracker.pincode:
                st.metric("Location", tracker.pincode)
            else:
                st.metric("Location", "Not Set")

        # Products list
        st.markdown("### 📦 Products")
        
        if not tracker.products:
            st.info("No products added yet. Go to 'Add Product' to get started!")
        else:
            for product in tracker.products:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{product['name']}**")
                        st.markdown(f"[View Product]({product['url']})")
                    with col2:
                        if product['current_price']:
                            st.success(f"₹{product['current_price']}")
                        else:
                            st.warning("Not checked")
                    with col3:
                        if st.button("🗑️", key=f"delete_{product['name']}"):
                            tracker.products.remove(product)
                            tracker.save_config()
                            st.rerun()
                    st.markdown("---")

    # Add Product
    elif page == "➕ Add Product":
        st.markdown('<h1 class="main-header">➕ Add Product</h1>', unsafe_allow_html=True)
        
        with st.form("add_product"):
            name = st.text_input("Product Name")
            url = st.text_input("Product URL")
            
            if st.form_submit_button("Add Product"):
                if name and url:
                    product = {
                        'name': name,
                        'url': url,
                        'target_price': None,
                        'current_price': None,
                        'last_checked': None
                    }
                    tracker.products.append(product)
                    tracker.save_config()
                    st.success(f"✅ Added {name}")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

    # Price History
    elif page == "📈 Price History":
        st.markdown('<h1 class="main-header">📈 Price History</h1>', unsafe_allow_html=True)
        
        if not tracker.products:
            st.info("No products to show history for")
        else:
            product_names = [p['name'] for p in tracker.products]
            selected = st.selectbox("Select Product", product_names)
            
            if selected:
                history = tracker.price_history.get(selected, [])
                if history:
                    df = pd.DataFrame(history)
                    df['date'] = pd.to_datetime(df['date'])
                    
                    if PLOTLY_AVAILABLE:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df['date'], 
                            y=df['price'],
                            mode='lines+markers',
                            name=selected
                        ))
                        fig.update_layout(title=f"Price History: {selected}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.line_chart(df.set_index('date')['price'])
                else:
                    st.info("No price history available")

    # Settings
    elif page == "⚙️ Settings":
        st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
        
        # Notifications
        st.markdown("### 🔔 Notifications")
        notifications = st.checkbox("Enable Notifications", value=tracker.notifications_enabled)
        if notifications != tracker.notifications_enabled:
            tracker.notifications_enabled = notifications
            tracker.save_config()
        
        # Location
        st.markdown("### 📍 Location")
        pincode = st.text_input("Pincode", value=getattr(tracker, 'pincode', ''))
        if st.button("Save Pincode"):
            tracker.pincode = pincode
            tracker.save_config()
            st.success("Pincode saved!")
        
        # Pushbullet
        st.markdown("### 📱 Pushbullet")
        st.info("Configure Pushbullet token in environment variables or Streamlit secrets")
        
        # Export/Import
        st.markdown("### 💾 Backup & Restore")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Config"):
                config = {
                    'products': tracker.products,
                    'price_history': tracker.price_history,
                    'notifications_enabled': tracker.notifications_enabled,
                    'pincode': getattr(tracker, 'pincode', '')
                }
                st.download_json(config, "price_tracker_config.json")
        
        with col2:
            uploaded_file = st.file_uploader("📤 Import Config", type="json")
            if uploaded_file:
                try:
                    config = json.load(uploaded_file)
                    tracker.products = config.get('products', [])
                    tracker.price_history = config.get('price_history', {})
                    tracker.notifications_enabled = config.get('notifications_enabled', True)
                    if 'pincode' in config:
                        tracker.pincode = config['pincode']
                    tracker.save_config()
                    st.success("✅ Configuration imported!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error importing: {e}")

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #666;">Price Tracker Dashboard • Made with ❤️</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
