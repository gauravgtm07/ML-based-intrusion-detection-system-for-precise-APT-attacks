# 🔧 Quick Fix - Install Missing Package

You're seeing this error:
```
websocket-client package not installed, only polling transport is available
❌ Could not connect to backend
```

## ✅ Solution (One Command)

Run this in your terminal:

```powershell
cd backend
pip install websocket-client
```

That's it! Now run the capture script again:

```powershell
cd ..
python run_realtime_capture.py
```

---

## 🎯 It Should Work Now!

You should see:
```
✅ Scapy is installed
✅ SocketIO client is available
🔌 Connecting to backend...
✅ Connected to backend server

🚀 STARTING REAL-TIME PACKET CAPTURE
```

---

**Problem solved!** 🚀
