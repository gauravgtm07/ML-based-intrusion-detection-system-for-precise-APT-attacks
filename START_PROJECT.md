# 🚀 Complete Project Startup Guide

## 📋 Quick Start Commands

### Option 1: Start Everything (3 Terminals)

#### Terminal 1: Backend Server
```bash
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\Intrusion Project\backend"
venv\Scripts\activate
python app.py
```
**Wait for:** `🚀 IDS Backend Server Starting...`

---

#### Terminal 2: Frontend Dashboard
```bash
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\Intrusion Project\frontend"
npm run dev
```
**Open browser:** http://localhost:5174

---

#### Terminal 3: Attack Simulator (Optional)
```bash
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\Intrusion Project"
python attack_simulator.py
```
**Choose attacks** to see them on dashboard!

---

## 🔴 Real-time Packet Capture (Optional)

### Run as Administrator:
```bash
# Open PowerShell as Administrator, then:
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\Intrusion Project"
python start_realtime_monitoring.py
```
**Detects REAL threats** from your network traffic!

---

## 🎯 What You Get

Once started, you'll have:
- ✅ **Dashboard:** http://localhost:5174
- ✅ **Backend API:** http://localhost:5000
- ✅ **Real-time Alerts:** WebSocket connection
- ✅ **Email Alerts:** Sent to amarmbbs00@gmail.com
- ✅ **Browser Notifications:** Desktop popups
- ✅ **Alert Sounds:** Different tones by severity
- ✅ **Analytics Page:** Detailed reports and charts
- ✅ **Settings Page:** Full control over alerts

---

## 📊 Access Your Dashboard

1. **Open browser:** http://localhost:5174
2. **Login** with your credentials
3. **Navigate:**
   - **Dashboard** - Main view with real-time alerts
   - **Analytics** - Reports, charts, and statistics
   - **Settings** - Configure notifications and alerts

---

## 🛑 Stop Everything

Press `Ctrl+C` in each terminal window.

---

## 🔧 Troubleshooting

### Backend Won't Start?
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Won't Start?
```bash
cd frontend
npm install
npm run dev
```

### Port Already in Use?
- Backend (5000): Check if another Flask app is running
- Frontend (5173/5174): Vite will automatically use next available port

---

## ✅ Features Checklist

- ✅ Real-time threat monitoring
- ✅ WebSocket live updates
- ✅ Browser notifications
- ✅ Alert sounds (different tones)
- ✅ Email alerts (Gmail)
- ✅ Analytics & Reports page
- ✅ Settings & Configuration page
- ✅ Attack simulator
- ✅ Real-time packet capture
- ✅ User authentication
- ✅ Export reports
- ✅ IP whitelist/blacklist

---

## 📧 Email Alerts

**Status:** ✅ ENABLED
**Your Email:** amarmbbs00@gmail.com
**Service:** Gmail SMTP

To test:
1. Go to Settings page
2. Click "Test Notification"
3. Check your Gmail inbox!

---

## 🎮 Demo Flow

1. **Start backend and frontend** (Terminal 1 & 2)
2. **Open dashboard** in browser
3. **Run attack simulator** (Terminal 3)
4. **Choose attack type** (e.g., option 2 for DDoS)
5. **Watch:**
   - Alert appears on dashboard
   - Browser notification pops up
   - Sound plays
   - Email sent to your Gmail
6. **Check Analytics page** for detailed reports
7. **Adjust Settings** to control notifications

---

## 🎯 Your Project Path

```
C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\Intrusion Project
```

---

**You're all set! Start the servers and enjoy your complete IDS system! 🚀**
