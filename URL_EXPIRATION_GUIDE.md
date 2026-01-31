# DO PRODUCT URLS EXPIRE? 🔗

## Quick Answer: **Usually NO, but sometimes YES**

Here's everything you need to know about product URL expiration:

---

## 🟢 URLs That DON'T Expire (Most Common)

### **Permanent Product URLs**
Most e-commerce sites use **permanent product IDs** in URLs:

#### Amazon
```
https://www.amazon.in/dp/B08CFSZLQ4/
                        ^^^^^^^^^^^^
                        Product ID (permanent)
```
**Expires?** ❌ NO - Works forever (as long as product exists)

#### Flipkart
```
https://www.flipkart.com/product/p/itm123abc456xyz
                                     ^^^^^^^^^^^^^^^
                                     Product ID (permanent)
```
**Expires?** ❌ NO - Permanent

#### Myntra
```
https://www.myntra.com/tshirts/roadster/12345678
                                         ^^^^^^^^
                                         Product ID
```
**Expires?** ❌ NO - Permanent

#### Nykaa
```
https://www.nykaa.com/product-name/p/12345
                                      ^^^^^
                                      Product ID
```
**Expires?** ❌ NO - Permanent

---

## 🟡 URLs That MIGHT Expire

### **Search Result URLs**
Some URLs contain session IDs or tracking parameters:

```
https://www.example.com/product?sessionid=abc123&ref=search
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                These might expire
```

**Solution:** Remove query parameters, keep only the product ID!

### **Quick Delivery Apps (Zepto, Blinkit, Swiggy)**
These URLs sometimes include location/session data:

```
https://blinkit.com/prn/product/prid/12345?location=mumbai
                                           ^^^^^^^^^^^^^^^^
                                           Might expire
```

**Status:** Usually works, but product availability varies by location

---

## 🔴 URLs That DO Expire

### **Cart/Checkout URLs**
```
https://www.amazon.in/gp/cart/view.html?ref=...
```
**Expires?** ✅ YES - These are temporary session URLs

**Solution:** Don't track these! Get the actual product page URL.

### **Time-Limited Deals**
```
https://www.flipkart.com/flash-sale/item/12345
```
**Expires?** ✅ YES - Deal pages expire after sale ends

**Solution:** Track the regular product page instead.

---

## 🛠️ HOW TO GET THE RIGHT URL

### ✅ **Correct Way:**

1. Go to the product page
2. Make sure you're on the **PRODUCT DETAILS** page
3. Copy URL from address bar
4. Remove any parameters after `?` (optional but recommended)

### ❌ **Wrong Way:**

Don't copy URLs from:
- Search results pages
- Cart pages
- Checkout pages
- Email links (often have tracking)
- "Share" buttons (might have referral codes)

---

## 📝 CLEANING URLs (Optional but Recommended)

### Before (with tracking parameters):
```
https://www.amazon.in/dp/B08CFSZLQ4/?tag=xyz&ref=search&pf_rd=123
```

### After (clean):
```
https://www.amazon.in/dp/B08CFSZLQ4/
```

**Both work, but clean URLs are better!**

### How to Clean:

**Method 1: Manual**
- Remove everything after `?` in the URL

**Method 2: Browser Extension**
- Use "ClearURLs" extension
- Automatically removes tracking

**Method 3: Online Tool**
- Use https://www.urldecoder.org/
- Paste and clean

---

## 🔍 WHAT HAPPENS IF URL EXPIRES?

### **In the Tracker:**

If a URL stops working, you'll see:
```
⚠️ Error: HTTP 404 - Product not found
⚠️ Error: Price not found with any method
```

### **Why This Happens:**

1. **Product discontinued** - No longer sold
2. **URL changed** - Rare, but possible
3. **Temporarily unavailable** - Out of stock
4. **Regional restriction** - Not available in your area

### **What to Do:**

1. **Visit the site manually** - Is product still there?
2. **Search for product again** - Get new URL
3. **Update in tracker** - Replace old URL with new one
4. **Or remove product** - If discontinued

---

## 🎯 BEST PRACTICES

### ✅ DO:
1. ✅ Use direct product page URLs
2. ✅ Remove query parameters
3. ✅ Test URL in browser before adding
4. ✅ Save product name clearly
5. ✅ Check if product is in stock

### ❌ DON'T:
1. ❌ Use cart/checkout URLs
2. ❌ Use search result URLs
3. ❌ Use deal/flash sale URLs
4. ❌ Use "share" links without cleaning
5. ❌ Assume URL will work forever without checking

---

## 🌐 SITE-SPECIFIC NOTES

### Amazon India
- **Product ID:** `/dp/XXXXXXXXXX/`
- **Permanent:** ✅ YES
- **Note:** Works even if product title changes

### Flipkart
- **Product ID:** `/p/itmXXXXXX` or `/p/XXXXX`
- **Permanent:** ✅ YES
- **Note:** Sometimes redirects but still works

### BigBasket
- **Product ID:** `/pd/12345678/product-name/`
- **Permanent:** ✅ YES
- **Note:** Product availability varies by area

### Zepto/Blinkit/Swiggy
- **Product ID:** Varies
- **Permanent:** ⚠️ MOSTLY
- **Note:** Availability depends on location

### Myntra
- **Product ID:** `/category/brand/12345678`
- **Permanent:** ✅ YES
- **Note:** Works as long as product exists

### Nykaa
- **Product ID:** `/p/12345`
- **Permanent:** ✅ YES
- **Note:** Reliable URLs

---

## 💡 PRO TIPS

### Tip 1: Bookmark Products
- Save product URLs in browser bookmarks
- If tracker fails, you have backup

### Tip 2: Check Regularly
- Visit products manually once a month
- Ensure they're still active

### Tip 3: Use Product ID
- Note down product ID separately
- Easy to find product again if URL changes

### Tip 4: Multiple Products
- Track same item from different sites
- If one URL fails, you have alternatives

### Tip 5: Screenshot
- Take screenshot when adding
- Helps identify product later

---

## 🔄 HANDLING URL CHANGES

### If Amazon Changes Product URL:

**Old:** `https://www.amazon.in/old-name/dp/B08CFSZLQ4/`
**New:** `https://www.amazon.in/new-name/dp/B08CFSZLQ4/`

**Still works!** ✅ Amazon redirects automatically.

### If Product Gets New Version:

**Old:** `iPhone 14 Pro - https://...dp/B0XX14XX`
**New:** `iPhone 15 Pro - https://...dp/B0XX15XX`

**Different products!** You need to add new URL.

---

## 📊 URL EXPIRATION BY CATEGORY

| Platform | Product URLs | Search URLs | Deal URLs | Cart URLs |
|----------|-------------|-------------|-----------|-----------|
| Amazon | ✅ Never | ❌ Yes | ⚠️ Maybe | ✅ Yes |
| Flipkart | ✅ Never | ❌ Yes | ⚠️ Maybe | ✅ Yes |
| BigBasket | ✅ Never | ❌ Yes | ⚠️ Maybe | ✅ Yes |
| Myntra | ✅ Never | ❌ Yes | ⚠️ Maybe | ✅ Yes |
| Zepto | ⚠️ Rarely | ❌ Yes | ✅ Yes | ✅ Yes |
| Blinkit | ⚠️ Rarely | ❌ Yes | ✅ Yes | ✅ Yes |

**Legend:**
- ✅ Never = Works forever
- ⚠️ Rarely/Maybe = Usually works
- ❌ Yes = Expires

---

## 🚨 ERROR HANDLING IN TRACKER

The tracker automatically handles URL issues:

### Error Messages:

```
⚠️ HTTP 404 - Product not found
```
**Meaning:** URL doesn't work anymore
**Action:** Update or remove product

```
⚠️ Price not found with any method
```
**Meaning:** Page structure changed OR product unavailable
**Action:** Check manually, might just be temporary

```
⚠️ Connection timeout
```
**Meaning:** Network issue
**Action:** Wait for next check, usually temporary

### Auto-Recovery:

- Tracker keeps trying on next run
- Temporary errors don't stop other products
- You get notified of persistent errors

---

## ✅ QUICK CHECKLIST

Before adding a product URL:

- [ ] Is it the product page? (not search/cart)
- [ ] Does it load in my browser?
- [ ] Can I see the price on the page?
- [ ] Is the product in stock?
- [ ] Have I removed tracking parameters?
- [ ] Is the product ID visible in URL?

If all YES → URL is good! ✅

---

## 🎯 SUMMARY

### TLDR:

✅ **Most product URLs DON'T expire**
- Amazon, Flipkart, Myntra, Nykaa: Permanent
- BigBasket: Permanent (if product exists)
- Zepto/Blinkit: Usually permanent

❌ **These URLs DO expire:**
- Cart/checkout links
- Search result pages
- Flash sale/deal pages
- Session-based URLs

💡 **Best Practice:**
1. Use clean product page URLs
2. Remove query parameters
3. Test before adding
4. Check occasionally

**You're good for 95%+ of products! 🎉**

---

## 🆘 NEED HELP?

If a URL stops working:

1. **Check the product manually** - Still exists?
2. **Get new URL** - Search and copy again
3. **Update in Streamlit dashboard** - Edit → Save
4. **Or use GitHub config** - Edit JSON directly

**Questions?** The tracker will tell you if URLs don't work!
