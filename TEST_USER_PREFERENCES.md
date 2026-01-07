# 🧪 Test User Preferences - Step by Step

## ⚠️ IMPORTANT: Refresh Your Browser First!

**Before testing, you MUST refresh your browser:**
- Press `Ctrl + Shift + R` (hard refresh)
- Or press `F5`
- Or click the refresh button

The changes won't work without refreshing!

---

## 🎨 Test Theme Switching

### Step 1: Open Browser Console
1. Press `F12` to open Developer Tools
2. Click on "Console" tab
3. Keep it open to see debug messages

### Step 2: Go to Settings Page
1. Navigate to Settings page
2. Scroll down to "User Preferences" section

### Step 3: Change Theme
1. Click on the "Theme" dropdown
2. Select "Light"
3. **What should happen:**
   - Console shows: `🎨 Applying theme: light`
   - Console shows: `Switching to LIGHT mode`
   - Green toast notification appears: "✅ Theme changed to: Light"
   - Background might change (depending on CSS)

### Step 4: Try Other Themes
1. Select "Dark" - should see console logs and toast
2. Select "Auto" - should see console logs and toast

---

## 🌍 Test Timezone Change

### Step 1: Change Timezone
1. In "User Preferences" section
2. Click on "Timezone" dropdown
3. Select "India (IST)"

### Step 2: Check Console
**You should see:**
- `🌍 Changing timezone to: Asia/Kolkata`
- `✅ Timezone toast shown`
- Green toast notification: "✅ Timezone changed to: Asia/Kolkata"

---

## 🔍 Debugging

### If Nothing Happens:

**1. Check Browser Console (F12)**
- Do you see any error messages?
- Do you see the console.log messages?
- If no messages appear, the code isn't running

**2. Hard Refresh**
```
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

**3. Clear Cache**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh page

**4. Check if Frontend is Running**
- Look at your Terminal 2
- Should show: `[vite] hmr update`
- If not, restart frontend:
  ```bash
  cd frontend
  npm run dev
  ```

---

## ✅ What You Should See

### When Theme Changes:
1. **Console logs:**
   ```
   🎨 Applying theme: light
   Switching to LIGHT mode
   ✅ Toast notification shown
   Toast removed
   ```

2. **Visual feedback:**
   - Green toast notification in top-right corner
   - Lasts for 3 seconds
   - Says "✅ Theme changed to: Light"

3. **Saved to localStorage:**
   - Open Console
   - Type: `localStorage.getItem('ids_theme')`
   - Should show: `"light"`

### When Timezone Changes:
1. **Console logs:**
   ```
   🌍 Changing timezone to: Asia/Kolkata
   ✅ Timezone toast shown
   Timezone toast removed
   ```

2. **Visual feedback:**
   - Green toast notification
   - Says "✅ Timezone changed to: Asia/Kolkata"

3. **Saved to localStorage:**
   - Type: `localStorage.getItem('ids_timezone')`
   - Should show: `"Asia/Kolkata"`

---

## 🎯 Quick Test Checklist

- [ ] Refreshed browser (Ctrl + Shift + R)
- [ ] Opened Developer Console (F12)
- [ ] Went to Settings page
- [ ] Found "User Preferences" section
- [ ] Changed Theme dropdown
- [ ] Saw console logs
- [ ] Saw green toast notification
- [ ] Changed Timezone dropdown
- [ ] Saw console logs
- [ ] Saw green toast notification

---

## 📸 What to Look For

### Green Toast Notification:
- Appears in **top-right corner**
- **Below the header** (80px from top)
- **Green background** (#10b981)
- **White text**
- **Large and bold** (16px, font-weight 600)
- **Stays for 3 seconds**
- **Then disappears**

### Console Logs:
- Should appear immediately when you change dropdown
- Shows what's happening behind the scenes
- Helps debug if something isn't working

---

## 🆘 Still Not Working?

### Try This:
1. **Close all browser tabs** of the app
2. **Stop frontend** (Ctrl+C in Terminal 2)
3. **Restart frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
4. **Open fresh browser tab:** http://localhost:5174
5. **Hard refresh:** Ctrl + Shift + R
6. **Try again**

### Check This:
- Is frontend running? (check Terminal 2)
- Is backend running? (check Terminal 1)
- Are you on the Settings page?
- Did you scroll to "User Preferences"?
- Is Developer Console open (F12)?

---

**If you see the console logs, the code is working! The toast notification should appear in the top-right corner.** 🎉
