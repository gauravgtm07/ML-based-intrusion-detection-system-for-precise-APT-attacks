# ✅ FIXED - Use This New Script

## The Problem
The `start_realtime_monitoring.py` script had connection issues with the backend's async mode.

## The Solution
I created a **better script** that uses WebSocket directly: `run_realtime_capture.py`

---

## 🚀 How to Use It (3 Steps)

### Step 1: Install required libraries
```powershell
cd backend
pip install python-socketio[client] websocket-client
```

### Step 2: Restart Your Backend
If it's already running, **stop it (Ctrl+C)** and restart:
```powershell
python app.py
```

### Step 3: Run the New Script (as Administrator)
In your **Administrator PowerShell** window:
```powershell
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project"
python run_realtime_capture.py
```

---

## ✅ What You Should See

The script will:
1. ✅ Check administrator privileges
2. ✅ Check if Scapy is installed
3. ✅ Connect to backend via WebSocket
4. 🚀 Start capturing packets
5. 🚨 Show alerts as they're detected

Example output:
```
🔍 REAL-TIME NETWORK MONITORING
✅ Running with administrator privileges
✅ Scapy is installed
✅ SocketIO client is available
🔌 Connecting to backend...
✅ Connected to backend server

🚀 STARTING REAL-TIME PACKET CAPTURE
🎯 MONITORING ACTIVE - Press Ctrl+C to stop

🚨 [1] Port Scan from 192.168.1.100
🚨 [2] Suspicious Connection from 10.0.0.5
```

---

## 🧪 Test It

Open another terminal and run:
```powershell
# Test 1: Port scan
nmap -p 1-100 localhost

# Test 2: Ping flood
ping -t localhost
```

Watch the alerts appear on your dashboard at **http://localhost:5173**!

---

## 🛑 To Stop

Press **Ctrl+C** in the PowerShell window running the capture script.

---

## ❓ Troubleshooting

### "SocketIO client not found" or "websocket-client package not installed"
```powershell
cd backend
pip install python-socketio[client] websocket-client
```

### "Could not connect to backend"
Make sure backend is running:
```powershell
cd backend
python app.py
```

### "Administrator privileges required"
Right-click PowerShell → **Run as Administrator**

---

**This new script is simpler and more reliable!** 🎯
