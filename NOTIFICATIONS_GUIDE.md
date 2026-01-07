# 🔔 Notifications, Emails & Sounds - Complete Guide

## ✅ What's Been Implemented

I've added **full notification functionality** to your IDS system! Now you'll get:
- 🔊 **Alert Sounds** - Different tones for different severity levels
- 🔔 **Browser Notifications** - Desktop notifications for threats
- 📧 **Email Alerts** - Backend endpoint ready for email integration

---

## 🚀 How to Enable Notifications

### Step 1: Enable Browser Notifications

1. **Go to Settings page** (click "Settings" in navigation)
2. **Look for the yellow warning box** that says "Browser notifications are not enabled"
3. **Click "Enable Notifications"** button
4. **Allow notifications** when your browser asks for permission

### Step 2: Test Your Notifications

1. Once enabled, you'll see a **green success box**
2. **Click "Test Notification"** button
3. You should:
   - 🔊 Hear an alert sound
   - 🔔 See a desktop notification
   - 📧 See email logged in backend console

---

## 🎵 Alert Sounds

### How It Works:
- **Different frequencies** for different severity levels:
  - 🔴 **Critical**: 880 Hz (high pitch)
  - 🟠 **High**: 660 Hz
  - 🟡 **Medium**: 440 Hz
  - 🟢 **Low**: 330 Hz (low pitch)

### To Enable/Disable:
- Go to **Settings** → **Alert Settings**
- Toggle **"Alert Sound"** checkbox
- Click **"Save Changes"**

---

## 🔔 Browser Notifications

### Features:
- **Desktop notifications** appear even when browser is minimized
- **Auto-close** after 10 seconds (except Critical alerts)
- **Click notification** to focus the browser window
- **Critical alerts** require manual dismissal

### Settings:
- **Enable Notifications**: Master toggle for all notifications
- **Critical Alerts Only**: Only show Critical severity alerts
- **Alert Sound**: Play sound with notification

### Notification Content:
- **Title**: "🚨 [Severity] Threat Detected"
- **Body**: Threat type, source IP, and description
- **Icon**: Severity emoji (🔴🟠🟡🟢)

---

## 📧 Email Alerts

### Current Status:
✅ **Backend endpoint ready** - `/api/send-email-alert`
⚠️ **Email service not configured** - Needs SMTP/SendGrid/AWS SES setup

### How It Works Now:
- Email alerts are **logged to backend console**
- You'll see: `📧 Email Alert Request:` in your backend terminal
- Shows: Threat type, severity, source IP, description

### To Configure Real Email Sending:

#### Option 1: Gmail SMTP (Simple)
```python
# Add to backend/app.py
import smtplib
from email.mime.text import MIMEText

def send_email_smtp(alert_data):
    sender = "your-email@gmail.com"
    receiver = "recipient@example.com"
    password = "your-app-password"  # Use App Password, not regular password
    
    msg = MIMEText(f"""
    Threat Detected!
    
    Type: {alert_data['threat_type']}
    Severity: {alert_data['severity']}
    Source IP: {alert_data['source_ip']}
    Description: {alert_data['description']}
    """)
    
    msg['Subject'] = f"🚨 {alert_data['severity']} Threat Detected"
    msg['From'] = sender
    msg['To'] = receiver
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
```

#### Option 2: SendGrid (Recommended for Production)
```bash
pip install sendgrid
```

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(alert_data):
    message = Mail(
        from_email='alerts@yourdomain.com',
        to_emails='admin@yourdomain.com',
        subject=f"🚨 {alert_data['severity']} Threat Detected",
        html_content=f"""
        <h2>Threat Detected!</h2>
        <p><strong>Type:</strong> {alert_data['threat_type']}</p>
        <p><strong>Severity:</strong> {alert_data['severity']}</p>
        <p><strong>Source IP:</strong> {alert_data['source_ip']}</p>
        <p><strong>Description:</strong> {alert_data['description']}</p>
        """
    )
    
    sg = SendGridAPIClient('YOUR_SENDGRID_API_KEY')
    sg.send(message)
```

---

## ⚙️ Settings Configuration

### Alert Settings:
- ✅ **Enable Notifications**: Turn all notifications on/off
- ✅ **Email Alerts**: Enable/disable email sending
- ✅ **Critical Alerts Only**: Only notify for Critical threats
- ✅ **Alert Sound**: Play sound on new alerts

### How Settings Are Saved:
- Stored in **browser's localStorage**
- Persists across page refreshes
- Each user has their own settings

---

## 🧪 Testing Your Setup

### Test 1: Settings Page Test Button
1. Go to **Settings** page
2. Click **"Test Notification"** button
3. Should see/hear:
   - 🔊 Alert sound
   - 🔔 Desktop notification
   - 📧 Console log in backend

### Test 2: Real Alert Test
1. Go to **Dashboard**
2. Run the attack simulator:
   ```bash
   python attack_simulator.py
   ```
3. Choose any attack option
4. Watch for:
   - Alert appears on dashboard
   - Sound plays
   - Notification pops up

### Test 3: Real-time Packet Capture
1. Start real-time monitoring (as admin):
   ```bash
   python start_realtime_monitoring.py
   ```
2. Generate network activity:
   ```bash
   ping -t localhost
   ```
3. Real threats will trigger notifications!

---

## 🎯 Notification Behavior

### When You'll Get Notified:
- ✅ New threat detected
- ✅ Real-time packet capture finds threat
- ✅ Attack simulator triggers alert
- ✅ Manual alert trigger via API

### When You Won't Get Notified:
- ❌ Notifications disabled in settings
- ❌ Browser permission denied
- ❌ "Critical Only" mode + non-critical alert
- ❌ Alert sound disabled (no sound, but notification still shows)

---

## 🔧 Troubleshooting

### No Sound Playing?
1. Check browser isn't muted
2. Check "Alert Sound" is enabled in Settings
3. Click "Test Notification" to verify
4. Try different browser (Chrome/Firefox/Edge)

### No Desktop Notifications?
1. Check browser notification permission:
   - Chrome: Settings → Privacy → Site Settings → Notifications
   - Firefox: Settings → Privacy → Permissions → Notifications
2. Check "Enable Notifications" is ON in Settings
3. Click "Enable Notifications" button again
4. Check OS notification settings (Windows/Mac)

### Emails Not Sending?
1. Check backend console - should see `📧 Email Alert Request:`
2. Email service needs to be configured (see Email Alerts section above)
3. Currently only logs to console - not actually sending emails

### Notifications Not Appearing for New Alerts?
1. Check Settings → "Enable Notifications" is ON
2. Check browser permission is granted (green box in Settings)
3. Check "Critical Only" mode isn't filtering alerts
4. Open browser console (F12) for error messages

---

## 📊 Notification Statistics

### What Gets Tracked:
- Settings saved to localStorage
- Notification permission status
- Email alert requests logged to backend

### What Doesn't Get Tracked:
- Number of notifications sent
- Notification click-through rate
- Email delivery status (unless you configure email service)

---

## 🎨 Customization Options

### Change Sound Frequency:
Edit `frontend/src/services/notificationService.ts`:
```typescript
const frequencies: Record<string, number> = {
  Critical: 880,  // Change these values
  High: 660,
  Medium: 440,
  Low: 330,
}
```

### Change Notification Duration:
```typescript
// Auto-close after X seconds
setTimeout(() => notification.close(), 10000)  // Change 10000 to desired milliseconds
```

### Change Notification Icons:
```typescript
private getSeverityIcon(severity: string): string {
  const icons: Record<string, string> = {
    Critical: '🔴',  // Change these emojis
    High: '🟠',
    Medium: '🟡',
    Low: '🟢',
  }
  return icons[severity] || '⚠️'
}
```

---

## 🚀 Next Steps

### To Get Full Email Functionality:
1. Choose an email service (Gmail SMTP, SendGrid, AWS SES)
2. Get API credentials
3. Update backend `/api/send-email-alert` endpoint
4. Test with "Test Notification" button

### To Add SMS Alerts:
1. Use Twilio API
2. Add SMS toggle to Settings page
3. Create `/api/send-sms-alert` endpoint
4. Integrate with notification service

### To Add Slack/Discord Alerts:
1. Create webhook URL
2. Add webhook settings to Settings page
3. Create `/api/send-webhook-alert` endpoint
4. Send JSON payload to webhook

---

## ✅ Summary

**What Works Now:**
- ✅ Alert sounds with different tones
- ✅ Desktop browser notifications
- ✅ Settings page with toggles
- ✅ Test notification button
- ✅ Automatic notifications on new alerts
- ✅ Email endpoint (logs to console)

**What Needs Configuration:**
- ⚠️ Email service (SMTP/SendGrid/AWS SES)
- ⚠️ SMS service (optional - Twilio)
- ⚠️ Webhook integration (optional - Slack/Discord)

---

**Enjoy your fully functional notification system! 🎉**
