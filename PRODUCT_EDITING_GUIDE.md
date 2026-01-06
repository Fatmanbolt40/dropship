# 📝 PRODUCT EDITING GUIDE

## ✅ NEW FEATURE: Edit Products with Custom Images!

You can now edit your products directly from the admin panel:
- ✏️ Change product names
- 📝 Edit descriptions  
- 🖼️ Upload custom images

---

## HOW TO EDIT PRODUCTS:

### Step 1: Open Admin Panel
Press **Alt+Shift+O** on your store page

### Step 2: Find "Edit Product" Section
Look for the section labeled "✏️ Edit Product"

### Step 3: Select a Product
- Click the dropdown menu
- Choose the product you want to edit
- The edit form will appear

### Step 4: Make Your Changes

**Product Name:**
- Edit the text field with your desired name
- Example: "Amazon Product B0CHWRXH8B" → "Premium Wireless Earbuds Pro"

**Description:**
- Write a compelling product description
- Include features, benefits, and why customers should buy
- Example: "Experience crystal-clear audio with these premium wireless earbuds. Features: noise cancellation, 24hr battery, waterproof design."

**Upload Image:**
- Click "Choose File"
- Select an image from your computer (JPG, PNG, GIF, etc.)
- High-quality product photos work best (800x800px or larger)
- Image will replace the Amazon placeholder

### Step 5: Save
Click **💾 Save Changes**

---

## WHAT HAPPENS:

**Before:**
```
Name: Amazon Product B0CHWRXH8B
Description: Premium quality product sourced...
Image: Green placeholder box
```

**After Your Edit:**
```
Name: Premium Wireless Earbuds Pro
Description: Experience crystal-clear audio with these premium...
Image: Your custom product photo
```

**On Your Store:**
- Product immediately updates
- Customers see your custom name and image
- Description shows on product details
- Still links to Amazon with your affiliate tag
- Still processes payments and auto-fulfills

---

## IMAGE TIPS:

✅ **Best Practices:**
- Use high-resolution product photos (minimum 800x800px)
- White or clean background works best
- Show the product clearly
- Multiple angles (upload one at a time to test different views)

✅ **Where to Get Images:**
- Screenshot from Amazon product page
- Use Amazon's product images (download from listing)
- Find stock photos online
- Take your own if you have the product
- Use Canva to create branded product images

⚠️ **Avoid:**
- Blurry or low-quality images
- Copyrighted images (unless from Amazon listing you're selling)
- Images with watermarks
- Too small (under 500x500px)

---

## EXAMPLE WORKFLOW:

**Scenario:** You added AirPods from Amazon URL, but it shows as "Amazon Product B0CHWRXH8B"

1. Press Alt+Shift+O
2. Go to "Edit Product" section
3. Select "Amazon Product B0CHWRXH8B" from dropdown
4. Change name to: "Apple AirPods Pro (2nd Gen) - Premium Wireless Earbuds"
5. Update description to:
   ```
   Premium wireless earbuds with active noise cancellation.
   Features: Spatial audio, adaptive transparency, 6-hour battery,
   MagSafe charging case. Perfect for music, calls, and workouts.
   Free shipping with Prime!
   ```
6. Upload AirPods product image (download from Amazon or Google)
7. Click Save
8. Refresh store - see your professional product listing!

---

## IMPORTANT NOTES:

✅ **Images are stored in:** `/static/uploads/`
✅ **Original Amazon link still works** (affiliate tag preserved)
✅ **Auto-fulfillment still works** (bot purchases from Amazon)
✅ **Pricing stays the same** (unless you edit the JSON file manually)

⚠️ **Currently can't edit pricing from UI** (coming soon)
- To change prices, edit the campaign JSON file directly
- Or delete and re-add the product with new pricing

---

## TESTING IT:

1. **Add a test product:**
   - Use Quick Add with any Amazon URL
   - Example: `https://www.amazon.com/dp/B0CHWRXH8B`

2. **Edit it:**
   - Select it from the Edit Product dropdown
   - Change name to "Test Product - Custom Name"
   - Add description: "This is my custom description!"
   - Upload any image from your computer

3. **Verify:**
   - Click Save
   - Refresh your store (Ctrl+Shift+R)
   - You should see your custom name and image!

---

## TROUBLESHOOTING:

**"Product not found"**
- Make sure you selected a product from dropdown
- Try refreshing the admin panel (close and reopen with Alt+Shift+O)

**Image not showing**
- Make sure image uploaded successfully (check for success message)
- Try JPG format (most compatible)
- Make sure file is under 5MB
- Refresh page with Ctrl+Shift+R (force reload)

**Changes not saving**
- Check server is running (products should load on main page)
- Check browser console for errors (F12 → Console tab)
- Try again with a smaller image file

**Want to revert to Amazon image**
- Currently no UI option (coming soon)
- Delete product and re-add from URL
- Or edit JSON file and remove custom_image field

---

## QUICK REFERENCE:

| Action | Steps |
|--------|-------|
| Edit Name | Admin Panel → Edit Product → Select → Change name → Save |
| Edit Description | Admin Panel → Edit Product → Select → Change description → Save |
| Upload Image | Admin Panel → Edit Product → Select → Choose File → Save |
| Cancel Edit | Click "❌ Cancel" button or close dropdown |

---

## YOUR WORKFLOW:

1. **Find products on Amazon** → Copy URL
2. **Quick Add to store** → Paste URL, click Add
3. **Edit for branding** → Change name, description, image
4. **Share your store** → Start making sales!

Your store: https://locomotively-needy-crysta.ngrok-free.dev

---

**Pro Tip:** Edit all your products with professional names, descriptions, and images to make your store look like a real brand instead of a generic dropship store. This increases trust and conversion rates!
