# STREAMLIT WEB DASHBOARD GUIDE 🎨
## Beautiful Web Interface for Your Price Tracker

Now you have a **gorgeous web dashboard** to manage everything!

---

## 🌟 WHAT YOU GET

### Beautiful Web Interface With:
✅ **Dashboard** - See all products at a glance
✅ **Individual ON/OFF** - Toggle notifications per product
✅ **Price Charts** - Visual price history graphs
✅ **Easy Add/Edit** - Add products with a form
✅ **Real-time Updates** - Check prices with one click
✅ **Mobile Friendly** - Works on phone/tablet

---

## 🚀 SETUP OPTIONS

You have **3 ways** to use the Streamlit dashboard:

### Option 1: Local (On Your Computer)
### Option 2: Cloud Free (Streamlit Community Cloud)
### Option 3: Hybrid (Dashboard local + Tracker on GitHub Actions)

Let's go through each!

---

## 📍 OPTION 1: RUN LOCALLY (Easiest to Start)

Perfect for testing and when you have your computer on.

### Step 1: Install Dependencies

```bash
pip install streamlit plotly pandas requests beautifulsoup4 lxml
```

### Step 2: Run the Dashboard

```bash
streamlit run streamlit_app.py
```

### Step 3: Open in Browser

Streamlit automatically opens at: **http://localhost:8501**

### What You Can Do:

1. **Add Products:**
   - Click "➕ Add Product"
   - Paste any product URL
   - Set name and threshold
   - Toggle notifications ON/OFF
   - Click "Add Product"

2. **Manage Products:**
   - See all products on dashboard
   - Toggle individual notifications with switches
   - Edit thresholds anytime
   - Delete products

3. **Check Prices:**
   - Click "🔍 Check All Prices Now"
   - See results in real-time
   - Get notifications if price drops

4. **View History:**
   - Click "📈 Price History"
   - Select product
   - See beautiful charts
   - View detailed table

### Pros:
✅ Instant setup
✅ No deployment needed
✅ Full control
✅ Works offline

### Cons:
❌ Only works when computer is on
❌ Only accessible locally (not from phone if PC is off)

---

## 🌐 OPTION 2: STREAMLIT COMMUNITY CLOUD (100% FREE!)

Deploy your dashboard online - **accessible from anywhere!**

### Setup Steps:

#### 1. Prepare Your Repository

Your GitHub repo should have:
```
your-repo/
├── streamlit_app.py
├── price_tracker_universal.py
├── requirements.txt
├── price_tracker_config.json
└── .streamlit/
    └── secrets.toml
```

#### 2. Create Secrets File

Create `.streamlit/secrets.toml`:
```toml
PUSHBULLET_TOKEN = "o.YourActualTokenHere"
```

Add to `.gitignore`:
```
.streamlit/secrets.toml
```

#### 3. Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with GitHub

3. **New app:**
   - Repository: `your-username/price-tracker`
   - Branch: `main`
   - Main file: `streamlit_app.py`

4. **Advanced Settings:**
   - Click "Advanced settings"
   - Add secret:
     ```
     PUSHBULLET_TOKEN = "o.YourToken"
     ```

5. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes

6. **Your app is live!**
   - URL: `https://your-app-name.streamlit.app`
   - Access from **anywhere**!

### Features:

✅ **Access from phone** - Open URL in browser
✅ **Always online** - No need for PC
✅ **100% FREE** - Unlimited usage
✅ **Auto-updates** - Git push = auto deploy
✅ **Secure** - HTTPS encryption

### Limitations:

⚠️ **Streamlit apps sleep after inactivity**
- Wakes up when you visit (takes 10 seconds)
- Still need GitHub Actions for background checks

---

## 🎯 OPTION 3: HYBRID SETUP (RECOMMENDED!)

**Best of both worlds:**
- GitHub Actions = Background price checking (24/7, free)
- Streamlit Cloud = Web dashboard (accessible anywhere)

### Architecture:

```
GitHub Actions (Cloud)
  ↓
  Checks prices every 20 min
  ↓
  Updates config.json on GitHub
  ↓
  Sends Pushbullet notifications
  
Streamlit Dashboard (Cloud)
  ↓
  Reads config.json from GitHub
  ↓
  Shows prices, charts, history
  ↓
  You manage products from browser
```

### Setup:

1. **Deploy GitHub Actions** (from FREE_GITHUB_ACTIONS_GUIDE.md)
   - Checks prices automatically
   - Runs 24/7 for free

2. **Deploy Streamlit Dashboard** (see Option 2 above)
   - Manage products via web
   - View history and charts
   - Access from anywhere

3. **How They Work Together:**
   - Both read/write same `price_tracker_config.json`
   - GitHub Actions does automatic checks
   - Streamlit provides user interface
   - Perfect combo! 🎉

### Why This Is Best:

✅ **24/7 tracking** (GitHub Actions)
✅ **Web dashboard** (Streamlit)
✅ **100% FREE** (both platforms)
✅ **Access anywhere** (phone, laptop, tablet)
✅ **No PC needed** (all in cloud)

---

## 🎮 USING THE DASHBOARD

### 📊 Dashboard Page

**What You See:**
- All tracked products in cards
- Current prices with color coding
- Individual notification toggles
- Quick actions (Edit, Delete)
- Price trend indicators

**Actions:**
- **Check All Prices Now** - Manual price check
- **Global Notifications** - Master switch
- **Toggle per product** - Individual control

### ➕ Add Product Page

**Form Fields:**
1. **Product URL** - Paste from any site
2. **Product Name** - Your label
3. **Price Threshold** - Alert when below this
4. **Notifications** - ON/OFF for this product

**What Happens:**
- URL is validated
- Price detection tested
- Product saved instantly
- Shows success/error message

### 📈 Price History Page

**Features:**
- Interactive price chart (Plotly)
- Statistics (min, max, avg, current)
- Threshold line on chart
- Detailed history table
- Export data

**Chart Interactions:**
- Zoom in/out
- Pan
- Hover for details
- Download as PNG

### ⚙️ Settings Page

**Global Settings:**
- Master notification toggle
- Pushbullet status

**Bulk Actions:**
- Enable all notifications
- Disable all notifications

**Backup/Restore:**
- Export configuration
- Import from backup

---

## 📱 MOBILE EXPERIENCE

The dashboard is **fully mobile-responsive**!

### On Your Phone:

1. **Open browser** (Chrome, Safari, etc.)
2. **Go to** your Streamlit app URL
3. **Add to Home Screen** for quick access
4. **Use like an app!**

### Mobile Features:

✅ Touch-friendly buttons
✅ Swipe through products
✅ Toggle switches work perfectly
✅ Charts are interactive
✅ Forms are easy to fill

---

## 🔔 INDIVIDUAL NOTIFICATIONS EXPLAINED

### How It Works:

Each product has **its own notification toggle**:

```json
{
  "url": "https://amazon.in/product1",
  "name": "Product 1",
  "threshold": 2500,
  "notifications_enabled": true  ← Individual setting
}
```

### Toggle States:

**Global ON + Product ON** = ✅ Notifications sent
**Global ON + Product OFF** = 🔕 No notifications for this product
**Global OFF + Product ON** = 🔕 No notifications (global override)
**Global OFF + Product OFF** = 🔕 No notifications

### Use Cases:

**Scenario 1: Watching Closely**
- Product: iPhone
- Notifications: ✅ ON
- Get instant alerts

**Scenario 2: Just Tracking**
- Product: Coffee beans
- Notifications: 🔕 OFF
- Track price but no alerts

**Scenario 3: Temporary Disable**
- Product: Laptop
- Notifications: 🔕 OFF (already bought it)
- Keep tracking for future reference

### How to Toggle:

**In Streamlit:**
1. Go to Dashboard
2. Find product card
3. Click the toggle switch
4. Instant save!

**In Config File:**
```json
"notifications_enabled": false  // Change to true/false
```

---

## 🎨 DASHBOARD FEATURES IN DETAIL

### Color-Coded Prices:

- **Green (💚)** - Below threshold (good deal!)
- **Black** - Above threshold (waiting)
- **Red arrow (📉)** - Price dropped
- **Green arrow (📈)** - Price increased

### Product Cards Show:

- Product name
- Current price
- Threshold
- Last checked time
- Notification status
- Price trend
- Quick actions

### Charts Show:

- Price over time (line graph)
- Threshold line (red dashed)
- Min/max markers
- Hover tooltips
- Zoom controls

---

## 💾 BACKUP & RESTORE

### Export Configuration:

1. Go to **Settings** page
2. Click **"Export Configuration"**
3. Download JSON file
4. Save somewhere safe

### Import Configuration:

1. Go to **Settings** page
2. Click **"Choose File"** under Import
3. Select your backup JSON
4. Configuration restored!

### What's Backed Up:

- All products with settings
- Price history
- Notification preferences

---

## 🔄 AUTO-SYNC WITH GITHUB ACTIONS

If using hybrid setup:

### How Sync Works:

1. **GitHub Actions** runs every 20 min
2. Checks prices
3. Updates `price_tracker_config.json` on GitHub
4. **Streamlit dashboard** reads latest from GitHub
5. You see updated prices!

### Manual Refresh:

Click **"🔄 Refresh Data"** in sidebar to force reload.

---

## 🚨 TROUBLESHOOTING

### Dashboard Won't Load

**Solution:**
```bash
streamlit run streamlit_app.py
```
Check terminal for errors.

### Prices Not Updating

**Solution:**
1. Click "Check All Prices Now"
2. Or wait for GitHub Actions run
3. Click "Refresh Data" in sidebar

### Can't Toggle Notifications

**Solution:**
- Check if you have write permissions
- Ensure config file isn't read-only

### Charts Not Showing

**Solution:**
```bash
pip install plotly pandas
```

---

## 💡 PRO TIPS

### Tip 1: Pin to Home Screen (Mobile)
- Open dashboard in mobile browser
- Tap "Share" → "Add to Home Screen"
- Access like a native app!

### Tip 2: Use Multiple Devices
- Dashboard URL works everywhere
- Manage from laptop, check from phone

### Tip 3: Set Smart Thresholds
- 10-15% below current = realistic
- 30-40% below = wait for sales
- Check price history for guidance

### Tip 4: Organize Products
- Use emojis in names: 📱 Phone, 👕 Shirt
- Easier to scan dashboard

### Tip 5: Export Regularly
- Backup config weekly
- Prevents data loss

---

## 🎯 EXAMPLE WORKFLOWS

### Workflow 1: Daily Deal Hunter

1. **Morning:** Open dashboard on phone
2. **See:** 3 products below threshold
3. **Click:** Product card → View details
4. **Buy:** Best deal first!

### Workflow 2: Big Purchase Planning

1. **Add:** Expensive item (₹50,000 laptop)
2. **Set:** Threshold ₹45,000 (10% off)
3. **Wait:** Track for 2-3 weeks
4. **Get notified:** When sale starts
5. **Buy:** At best price!

### Workflow 3: Grocery Restocking

1. **Add:** Regular groceries
2. **Set:** Threshold = usual price
3. **Disable:** Notifications for non-urgent items
4. **Enable:** For items running low
5. **Stock up:** When prices drop

---

## 📊 DASHBOARD METRICS

You can track:

- **Total products** tracked
- **Active alerts** (notifications ON)
- **Price drops** detected
- **Savings** accumulated
- **Check frequency** (via history)

---

## ✅ QUICK START CHECKLIST

- [ ] Install dependencies
- [ ] Run Streamlit locally
- [ ] Add first product
- [ ] Test price detection
- [ ] Toggle notifications
- [ ] Check price history
- [ ] (Optional) Deploy to cloud
- [ ] (Optional) Setup hybrid mode

---

## 🎉 SUMMARY

### What You Now Have:

✅ **Beautiful web dashboard**
✅ **Individual product controls**
✅ **Price history charts**
✅ **Mobile-friendly interface**
✅ **Easy product management**
✅ **Works with ANY website**
✅ **100% FREE (cloud option)**

### Three Ways to Use:

1. **Local** - Run on your computer
2. **Cloud** - Deploy to Streamlit Cloud
3. **Hybrid** - Best of both!

**Choose what works best for you! 🚀**

---

## 📞 GETTING HELP

### Common Issues:

1. **Check requirements.txt** - All deps installed?
2. **Check Python version** - 3.8+ required
3. **Check permissions** - Can write to config file?
4. **Check logs** - Terminal shows errors

### Resources:

- Streamlit docs: https://docs.streamlit.io
- This guide: Read thoroughly!
- Config file: Check for errors

**You're all set! Enjoy your beautiful price tracker dashboard! 🎊**
