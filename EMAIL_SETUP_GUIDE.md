# 📧 Email Alerts Setup Guide

## 🎯 Current Status

✅ **Email system is now fully implemented!**
⚠️ **But it's disabled by default** - You need to configure it

---

## 🚀 Quick Setup (Gmail - Recommended)

### Step 1: Get Gmail App Password

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Enable 2-Step Verification** (if not already enabled):
   - Go to Security → 2-Step Verification
   - Follow the setup process

3. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Other** (type "IDS System")
   - Click **Generate**
   - **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 2: Configure Backend

1. **Navigate to backend folder**:
   ```bash
   cd backend
   ```

2. **Copy the example .env file**:
   ```bash
   copy .env.example .env
   ```

3. **Edit `.env` file** and update these lines:
   ```env
   EMAIL_ENABLED=True
   EMAIL_SERVICE=gmail
   GMAIL_SENDER=your-email@gmail.com
   GMAIL_APP_PASSWORD=abcdefghijklmnop
   GMAIL_RECIPIENT=where-to-send-alerts@gmail.com
   ```

### Step 3: Restart Backend

1. **Stop the current backend** (Ctrl+C in backend terminal)
2. **Start it again**:
   ```bash
   python app.py
   ```

### Step 4: Test It!

1. **Go to Settings page** in your browser
2. **Make sure "Email Alerts" is enabled** (checkbox checked)
3. **Click "Test Notification"** button
4. **Check your email!** You should receive an alert email

---

## 📧 What You'll Receive

### Email Subject:
```
[IDS Alert] High Threat Detected
```

### Email Content:
- 🚨 **Security Alert Header** (color-coded by severity)
- **Threat Details**:
  - Threat Type (e.g., "DDoS Attack")
  - Severity (Critical/High/Medium/Low)
  - Status (Active/Blocked/Investigating)
- **Network Details**:
  - Source IP
  - Destination IP
  - Port
  - Protocol
- **Description** of the threat
- **Timestamp** of detection

### Email Format:
- ✅ Beautiful HTML email with color coding
- ✅ Plain text fallback for email clients that don't support HTML
- ✅ Professional formatting
- ✅ Mobile-friendly

---

## ⚙️ Alternative Email Services

### Option 2: Generic SMTP

If you have another email provider (Outlook, Yahoo, custom domain):

1. **Edit `.env` file**:
   ```env
   EMAIL_ENABLED=True
   EMAIL_SERVICE=smtp
   SMTP_HOST=smtp.your-provider.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@example.com
   SMTP_PASSWORD=your-password
   SMTP_USE_TLS=True
   ```

2. **Common SMTP Settings**:
   - **Outlook**: `smtp.office365.com:587`
   - **Yahoo**: `smtp.mail.yahoo.com:587`
   - **Custom Domain**: Check with your email provider

### Option 3: SendGrid (For Production)

SendGrid is recommended for high-volume email sending:

1. **Sign up**: https://signup.sendgrid.com/
2. **Get API Key**: https://app.sendgrid.com/settings/api_keys
3. **Install SendGrid**:
   ```bash
   pip install sendgrid
   ```
4. **Edit `.env` file**:
   ```env
   EMAIL_ENABLED=True
   EMAIL_SERVICE=sendgrid
   SENDGRID_API_KEY=your-api-key-here
   SENDGRID_FROM_EMAIL=alerts@yourdomain.com
   SENDGRID_TO_EMAIL=admin@yourdomain.com
   ```

---

## 🧪 Testing Email Alerts

### Test 1: Settings Page Test Button
1. Go to **Settings** page
2. Enable **"Email Alerts"** checkbox
3. Click **"Test Notification"** button
4. Check your email inbox

### Test 2: Real Alert Test
1. Run attack simulator:
   ```bash
   python attack_simulator.py
   ```
2. Choose any attack option
3. Check your email - you should receive an alert!

### Test 3: Real-time Monitoring
1. Start real-time monitoring (as admin):
   ```bash
   python start_realtime_monitoring.py
   ```
2. Generate network activity
3. Real threats will trigger email alerts!

---

## 🔧 Troubleshooting

### No Emails Received?

#### Check 1: Email Enabled?
- Open `backend/.env` file
- Verify: `EMAIL_ENABLED=True`

#### Check 2: Correct Credentials?
- Double-check your Gmail address
- Verify App Password is correct (16 characters, no spaces)
- Make sure you're using **App Password**, not regular password

#### Check 3: Backend Console
- Look for: `✅ Email sent successfully to...`
- Or error messages like: `❌ Email sending failed:`

#### Check 4: Spam Folder
- Check your spam/junk folder
- Mark as "Not Spam" if found there

#### Check 5: Gmail Security
- Go to: https://myaccount.google.com/security
- Check for "Critical security alert" emails
- You may need to allow "Less secure app access" (not recommended)
- Better: Use App Password (see Step 1 above)

### Backend Errors?

#### Error: "Email service not configured"
- Make sure `.env` file exists in `backend/` folder
- Copy from `.env.example` if needed

#### Error: "Gmail App Password not configured"
- Check `GMAIL_APP_PASSWORD` in `.env` file
- Remove any spaces from the password
- Should be 16 characters

#### Error: "Authentication failed"
- Wrong email or password
- Use App Password, not regular password
- Enable 2-Step Verification first

---

## 📊 Email Settings Control

### From Settings Page:
- **Email Alerts Toggle**: Turn email alerts on/off instantly
- **Critical Alerts Only**: Only send emails for Critical threats
- **Test Button**: Send a test email to verify setup

### Settings Apply Immediately:
- No need to click "Save Changes"
- Toggle "Email Alerts" off → No emails sent
- Toggle "Email Alerts" on → Emails resume

---

## 🎨 Customization

### Change Email Subject Prefix:
Edit `backend/.env`:
```env
EMAIL_SUBJECT_PREFIX=[My IDS]
```

### Change Email Template:
Edit `backend/email_service.py`:
- Modify `_create_html_email()` for HTML version
- Modify `_create_text_email()` for plain text version

### Send to Multiple Recipients:
Edit `backend/.env`:
```env
GMAIL_RECIPIENT=email1@example.com,email2@example.com,email3@example.com
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use App Passwords (not regular passwords)
- Enable 2-Step Verification on Gmail
- Keep `.env` file private (never commit to Git)
- Use SendGrid for production systems
- Limit email recipients to authorized personnel

### ❌ DON'T:
- Share your App Password
- Commit `.env` file to version control
- Use regular Gmail password
- Send alerts to public email addresses
- Disable 2-Step Verification

---

## 📝 Summary

**What's Implemented:**
- ✅ Full email sending system
- ✅ Gmail SMTP support
- ✅ Generic SMTP support
- ✅ SendGrid API support
- ✅ Beautiful HTML emails
- ✅ Plain text fallback
- ✅ Color-coded by severity
- ✅ Settings page toggle
- ✅ Test button

**What You Need to Do:**
1. Get Gmail App Password
2. Create `backend/.env` file
3. Add your email credentials
4. Restart backend
5. Test it!

---

## 🎯 Quick Checklist

- [ ] Created Gmail App Password
- [ ] Copied `.env.example` to `.env`
- [ ] Updated email credentials in `.env`
- [ ] Set `EMAIL_ENABLED=True`
- [ ] Restarted backend server
- [ ] Enabled "Email Alerts" in Settings page
- [ ] Clicked "Test Notification" button
- [ ] Received test email successfully

---

**Once configured, you'll receive beautiful email alerts for every threat detected! 📧🚨**
