# 🚀 COMPLETE SETUP GUIDE - STEP BY STEP
## From Zero to Running in 15 Minutes!

Follow these exact steps. I'll guide you through everything!

---

## 📋 WHAT YOU NEED

- ✅ Computer (Windows, Mac, or Linux)
- ✅ Internet connection
- ✅ Files you downloaded (all the .py and .md files)
- ✅ 15 minutes of time

---

## 🎯 SETUP PATH - CHOOSE ONE

### **Path A: Local Setup** (Start here - easiest!)
- Run on your computer
- Takes 10 minutes
- Perfect for testing
- → Go to PART 1

### **Path B: Cloud Setup** (After testing locally)
- Runs 24/7 for free
- Accessible from anywhere
- Takes 20 minutes
- → Go to PART 2

**I recommend: Start with Path A, then do Path B later!**

---

# PART 1: LOCAL SETUP (10 MINUTES)

## STEP 1: Install Python (5 minutes)

### Windows:

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click **"Download Python 3.12.x"** (big yellow button)
   - Save the file

2. **Install Python:**
   - Double-click the downloaded file
   - ⚠️ **CRITICAL:** Check ✅ **"Add Python to PATH"**
   - Click **"Install Now"**
   - Wait 2-3 minutes
   - Click **"Close"**

3. **Verify Installation:**
   - Press `Win + R`
   - Type `cmd` and press Enter
   - Type: `python --version`
   - Press Enter
   - Should show: `Python 3.12.x`

### Mac:

1. **Open Terminal:**
   - Press `Cmd + Space`
   - Type "Terminal"
   - Press Enter

2. **Check if Python is installed:**
   ```bash
   python3 --version
   ```

3. **If not installed, install Homebrew first:**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

4. **Then install Python:**
   ```bash
   brew install python
   ```

### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip -y
python3 --version
```

✅ **Python installed!**

---

## STEP 2: Organize Your Files (2 minutes)

1. **Create a folder:**
   - **Windows:** Create folder `C:\PriceTracker`
   - **Mac/Linux:** Create folder `/home/yourusername/PriceTracker`

2. **Move all downloaded files to this folder:**
   ```
   PriceTracker/
   ├── streamlit_app.py
   ├── price_tracker_universal.py
   ├── requirements.txt
   ├── price_tracker_config.example.json
   ├── price-tracker.yml
   └── All the .md guides
   ```

3. **Create your config file:**
   - Copy `price_tracker_config.example.json`
   - Rename copy to `price_tracker_config.json`
   - OR create new file `price_tracker_config.json` with this content:

```json
{
  "products": [],
  "price_history": {},
  "notifications_enabled": true
}
```

✅ **Files organized!**

---

## STEP 3: Install Dependencies (2 minutes)

### Open Terminal/Command Prompt:

**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter
- Navigate to your folder:
  ```cmd
  cd C:\PriceTracker
  ```

**Mac/Linux:**
- Open Terminal
- Navigate to your folder:
  ```bash
  cd ~/PriceTracker
  ```

### Install all required packages:

**Windows:**
```cmd
pip install streamlit plotly pandas requests beautifulsoup4 lxml
```

**Mac/Linux:**
```bash
pip3 install streamlit plotly pandas requests beautifulsoup4 lxml
```

This will take 2-3 minutes. You'll see a lot of text scrolling.

When done, you should see: `Successfully installed ...`

✅ **Dependencies installed!**

---

## STEP 4: Setup Pushbullet (3 minutes)

### A. Install Pushbullet App on Phone:

**Android:**
1. Open Google Play Store
2. Search "Pushbullet"
3. Install "Pushbullet - SMS on PC"
4. Open app
5. Sign in with Google

**iPhone:**
1. Open App Store
2. Search "Pushbullet"
3. Install "Pushbullet"
4. Open app
5. Sign in with Google

### B. Get Your Access Token:

1. **On your computer**, go to: https://www.pushbullet.com

2. **Sign in** with the SAME Google account

3. **Get token:**
   - Click your profile picture (top right)
   - Click **"Settings"**
   - Click **"Account"** tab
   - Scroll to **"Access Tokens"**
   - Click **"Create Access Token"**
   - **COPY the token** (looks like: `o.aBcDeFgH1234567890XyZ`)

### C. Set Environment Variable:

**Windows (Permanent):**
1. Press `Win + R`
2. Type `sysdm.cpl`
3. Press Enter
4. Click **"Advanced"** tab
5. Click **"Environment Variables"**
6. Under "User variables", click **"New"**
7. Variable name: `PUSHBULLET_TOKEN`
8. Variable value: `o.YourActualTokenHere` (paste your token)
9. Click **OK, OK, OK**
10. **Close and reopen** Command Prompt

**Windows (Quick test - temporary):**
```cmd
set PUSHBULLET_TOKEN=o.YourActualTokenHere
```

**Mac/Linux (Permanent):**
```bash
nano ~/.bashrc
```
Add this line at the end:
```bash
export PUSHBULLET_TOKEN="o.YourActualTokenHere"
```
Save: `Ctrl + X`, then `Y`, then `Enter`

Apply changes:
```bash
source ~/.bashrc
```

**Mac/Linux (Quick test - temporary):**
```bash
export PUSHBULLET_TOKEN="o.YourActualTokenHere"
```

### D. Test It:

**Verify token is set:**
```bash
# Windows
echo %PUSHBULLET_TOKEN%

# Mac/Linux
echo $PUSHBULLET_TOKEN
```

Should show your token!

**Test notification:**
1. Go to: https://www.pushbullet.com
2. Click "Send yourself a push"
3. Type "Test"
4. Click Send
5. **Check your phone** - you should get notification!

✅ **Pushbullet configured!**

---

## STEP 5: Launch the Dashboard! (1 minute)

### Start Streamlit:

**Windows:**
```cmd
cd C:\PriceTracker
streamlit run streamlit_app.py
```

**Mac/Linux:**
```bash
cd ~/PriceTracker
streamlit run streamlit_app.py
```

### What Happens:

You'll see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Your browser will **automatically open** to the dashboard!

If it doesn't open automatically:
- Open browser manually
- Go to: http://localhost:8501

🎉 **YOU'RE RUNNING!** 🎉

---

## STEP 6: Add Your First Product (2 minutes)

### In the Dashboard:

1. **Click** "➕ Add Product" in the sidebar

2. **Get a product URL:**
   - Go to Amazon, Flipkart, or any store
   - Find a product
   - Copy the URL
   - Example: `https://www.amazon.in/dp/B08CFSZLQ4/`

3. **Fill the form:**
   - **Product URL:** Paste the URL
   - **Product Name:** "Fire TV Stick" (or whatever)
   - **Price Threshold:** 2500 (or any amount)
   - **Enable notifications:** ✅ Checked

4. **Click** "✅ Add Product"

5. **Wait for price detection test** (10 seconds)

6. **Success!** 🎉 You should see:
   - "✅ Added: Fire TV Stick"
   - "✅ Price detected: ₹2,499"

### View Your Product:

1. **Click** "📊 Dashboard" in sidebar

2. **You'll see:**
   - Product card with name
   - Current price
   - Threshold
   - Notification toggle

3. **Try the toggle:**
   - Click the "🔔 Alerts" switch
   - It toggles ON/OFF!

✅ **First product added!**

---

## STEP 7: Check Price Manually (1 minute)

1. **On Dashboard page**

2. **Click** "🔍 Check All Prices Now"

3. **Watch the magic:**
   - Spinner shows "Checking prices..."
   - Terminal shows progress
   - Dashboard updates with new price

4. **Look at the product card:**
   - Shows latest price
   - Shows when last checked
   - If below threshold → Green price! 💚

✅ **Manual price check works!**

---

## STEP 8: View Price History (1 minute)

1. **Click** "📈 Price History" in sidebar

2. **Select your product** from dropdown

3. **See the chart!**
   - Price line graph
   - Your threshold as red dashed line
   - Statistics (current, min, max, avg)
   - Detailed table below

4. **Interact with chart:**
   - Hover to see exact values
   - Zoom in/out
   - Pan around

✅ **History working!**

---

## 🎉 CONGRATULATIONS!

You now have a **fully working price tracker**!

### What You Can Do Now:

✅ Add more products (any website!)
✅ Set individual thresholds
✅ Toggle notifications per product
✅ Check prices manually
✅ View beautiful charts
✅ Get phone notifications

### Keep Dashboard Running:

- **Don't close the terminal/command prompt**
- Dashboard runs at: http://localhost:8501
- Access from any browser on your computer

### To Stop:

- Press `Ctrl + C` in the terminal

### To Restart:

```bash
streamlit run streamlit_app.py
```

---

# PART 2: CLOUD SETUP (20 MINUTES)

Now let's make it run **24/7 for FREE** in the cloud!

## OPTION A: GitHub Actions (Background Checker)

### STEP 1: Create GitHub Account (2 minutes)

1. Go to: https://github.com
2. Click **"Sign up"**
3. Enter email, password, username
4. Verify email
5. ✅ Done!

### STEP 2: Create Repository (3 minutes)

1. **Click** the **"+"** icon (top right)
2. **Select** "New repository"
3. **Fill in:**
   - Repository name: `price-tracker`
   - Description: "My price tracker"
   - **IMPORTANT:** Select **"Public"** (for unlimited free minutes)
   - ✅ Check "Add a README file"
4. **Click** "Create repository"

### STEP 3: Upload Files (5 minutes)

1. **Click** "Add file" → "Upload files"

2. **Drag and drop these files:**
   - `price_tracker_universal.py`
   - `requirements.txt`
   - `price_tracker_config.json`

3. **Click** "Commit changes"

4. **Create workflow folder:**
   - Click "Add file" → "Create new file"
   - Name: `.github/workflows/price-tracker.yml`
   - This creates the folders automatically

5. **Paste this content:**

```yaml
name: Price Tracker

on:
  schedule:
    - cron: '*/20 * * * *'  # Every 20 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  track-prices:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: pip install requests beautifulsoup4 lxml
        
    - name: Run tracker
      env:
        PUSHBULLET_TOKEN: ${{ secrets.PUSHBULLET_TOKEN }}
      run: python price_tracker_universal.py
        
    - name: Commit updates
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add price_tracker_config.json
        git diff --quiet && git diff --staged --quiet || git commit -m "Update prices"
        git push
```

6. **Click** "Commit changes"

### STEP 4: Add Pushbullet Secret (2 minutes)

1. **Go to** your repository page

2. **Click** "Settings" tab

3. **Click** "Secrets and variables" → "Actions"

4. **Click** "New repository secret"

5. **Fill in:**
   - Name: `PUSHBULLET_TOKEN`
   - Secret: `o.YourActualTokenHere` (your Pushbullet token)

6. **Click** "Add secret"

### STEP 5: Test It! (1 minute)

1. **Click** "Actions" tab

2. **Click** "Price Tracker" workflow

3. **Click** "Run workflow" button

4. **Click** green "Run workflow" button

5. **Wait** 30 seconds

6. **Click** the workflow run to see logs

7. **You should see:**
   - ✅ Setup Python
   - ✅ Install dependencies
   - ✅ Run tracker
   - ✅ Price checks in logs

🎉 **GitHub Actions running!**

### What Happens Now:

- **Every 20 minutes**, GitHub checks your prices
- **Automatically** updates config file
- **Sends notifications** when prices drop
- **100% FREE** - runs forever!
- **No PC needed!**

---

## OPTION B: Streamlit Cloud (Web Dashboard)

### STEP 1: Prepare Repository (2 minutes)

1. **In your GitHub repo**, create `.streamlit/secrets.toml`:
   - Click "Add file" → "Create new file"
   - Name: `.streamlit/secrets.toml`
   - Content:
```toml
PUSHBULLET_TOKEN = "o.YourActualTokenHere"
```
   - Commit

2. **Upload streamlit_app.py** if you haven't:
   - Click "Add file" → "Upload files"
   - Upload `streamlit_app.py`
   - Commit

### STEP 2: Deploy to Streamlit Cloud (5 minutes)

1. **Go to:** https://share.streamlit.io

2. **Click** "Sign in with GitHub"

3. **Authorize** Streamlit

4. **Click** "New app"

5. **Fill in:**
   - Repository: `your-username/price-tracker`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

6. **Click** "Advanced settings"

7. **Add secret:**
   - In the secrets box, paste:
```toml
PUSHBULLET_TOKEN = "o.YourActualTokenHere"
```

8. **Click** "Deploy!"

9. **Wait** 2-3 minutes

10. **Your app is live!**
    - URL: `https://your-app-name.streamlit.app`
    - Save this URL!

🎉 **Dashboard online!**

### Access Your Dashboard:

1. **Open the URL** on any device
2. **On phone:** Open in browser, works perfectly!
3. **Add to home screen** for quick access

---

## 🎯 FINAL SETUP - HYBRID MODE (BEST!)

Now you have **both**:

✅ **GitHub Actions** - Checks prices every 20 min (24/7, free)
✅ **Streamlit Dashboard** - Manage products from anywhere

### How They Work Together:

```
GitHub Actions (Cloud)
  ↓
  Checks prices automatically
  ↓
  Updates config.json
  ↓
  
Streamlit Dashboard (Cloud)
  ↓
  Shows latest prices
  ↓
  You manage products
  ↓
  
Both FREE, both 24/7! 🎉
```

---

## ✅ VERIFICATION CHECKLIST

Make sure everything works:

### Local Setup:
- [ ] Python installed (`python --version` works)
- [ ] Dependencies installed (no errors)
- [ ] Pushbullet token set (`echo $PUSHBULLET_TOKEN` shows token)
- [ ] Dashboard opens at http://localhost:8501
- [ ] Can add products
- [ ] Can check prices
- [ ] Can see history
- [ ] Phone notifications work

### Cloud Setup:
- [ ] GitHub repository created
- [ ] Files uploaded
- [ ] GitHub Actions workflow added
- [ ] Pushbullet secret added
- [ ] Workflow runs successfully
- [ ] Streamlit app deployed
- [ ] Can access dashboard from phone
- [ ] Both services update same config

---

## 🆘 TROUBLESHOOTING

### "python: command not found"

**Solution:**
- Windows: Use `python` not `python3`
- Mac/Linux: Use `python3` not `python`
- Restart terminal after installing Python

### "pip: command not found"

**Solution:**
- Windows: Use `pip` not `pip3`
- Mac/Linux: Use `pip3` not `pip`

### "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit plotly pandas requests beautifulsoup4 lxml
```

### "Pushbullet token not set"

**Solution:**
```bash
# Check if set
echo %PUSHBULLET_TOKEN%  # Windows
echo $PUSHBULLET_TOKEN   # Mac/Linux

# If empty, set it again
set PUSHBULLET_TOKEN=o.YourToken  # Windows
export PUSHBULLET_TOKEN="o.YourToken"  # Mac/Linux
```

### Dashboard won't load

**Solution:**
1. Check terminal for errors
2. Make sure you're in the right folder
3. Try: `streamlit run streamlit_app.py --server.port 8502`

### GitHub Actions fails

**Solution:**
1. Check if PUSHBULLET_TOKEN secret is added
2. Check if all files are uploaded
3. Check workflow logs for specific error

### "Price not found with any method"

**Solution:**
1. Try a different product
2. Make sure URL is the product page (not cart/search)
3. Some products might not work - try another

---

## 📱 USING ON YOUR PHONE

### Local Dashboard (same WiFi):

1. **Find your computer's IP:**
   - Windows: `ipconfig` (look for IPv4)
   - Mac/Linux: `ifconfig` (look for inet)

2. **On phone:**
   - Open browser
   - Go to: `http://192.168.x.x:8501` (your IP)

### Cloud Dashboard (anywhere):

1. **Open browser on phone**
2. **Go to your Streamlit URL**
3. **Tap menu** (Safari) or **"Add to Home Screen"** (Chrome)
4. **Use like an app!**

---

## 🎉 YOU'RE DONE!

### What You Now Have:

✅ Beautiful web dashboard
✅ Works with ANY website  
✅ Individual price limits per product
✅ Individual notifications ON/OFF
✅ Runs 24/7 in cloud for FREE
✅ Accessible from phone/tablet
✅ Price history with charts
✅ Phone notifications via Pushbullet

### Next Steps:

1. **Add more products** - Track everything you want!
2. **Set realistic thresholds** - 10-20% below current price
3. **Toggle notifications** - ON for urgent, OFF for just tracking
4. **Check dashboard daily** - See if any deals came up
5. **Enjoy saving money!** 💰

---

## 💡 QUICK TIPS

1. **Start with 3-5 products** - Don't add too many at once
2. **Test with one product** first - Make sure everything works
3. **Check price history** after a week - See the trends
4. **Set smart thresholds** - Not too low (unrealistic)
5. **Use the dashboard** - It's easier than editing JSON files!

---

## 📞 NEED HELP?

### Check These:

1. **Terminal/Command Prompt** - Shows error messages
2. **Browser console** - F12 → Console tab
3. **GitHub Actions logs** - Shows why workflow failed
4. **This guide** - Read again carefully

### Common Issues:

- **Can't install Python** → Use Python installer from python.org
- **Dependencies fail** → Try: `pip install --upgrade pip` first
- **Pushbullet not working** → Test on pushbullet.com first
- **GitHub Actions fails** → Check if files are uploaded
- **Price not found** → Try different product URL

---

## 🎊 CONGRATULATIONS!

You've successfully set up a **professional-grade price tracker**!

**Enjoy your automated deal hunting! 🛒💰**

---

**Any questions? Re-read the relevant section above. Everything you need is here!**
