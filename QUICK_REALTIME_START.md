# ⚡ Quick Start - Real-time Packet Capture

## 🎯 3 Simple Steps to Detect Real Threats

### Step 1: Install Scapy
```bash
cd backend
pip install scapy
```

### Step 2: Start Backend
```bash
python app.py
```

### Step 3: Enable Real-time Monitoring (Run as Administrator!)
```bash
# Open NEW PowerShell as Administrator, then:
cd "C:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project"
python run_realtime_capture.py
```

---

## ✅ That's it!

Now open the dashboard at **http://localhost:5173** and watch **REAL threats** appear!

---

## 🧪 Test It

Try these commands to generate real alerts:

### Test 1: Port Scan
```bash
nmap -p 1-100 localhost
```
**Expected**: "Port Scan" alert on dashboard

### Test 2: High Traffic
```bash
ping -t localhost
```
**Expected**: "DDoS Attack" alert after sustained traffic

### Test 3: Suspicious Port
```bash
telnet localhost 23
```
**Expected**: "Suspicious Connection" alert

---

## 🛑 Stop Monitoring

Press `Ctrl+C` in the monitoring terminal

---

## 📖 Need More Details?

See **[REALTIME_SETUP.md](REALTIME_SETUP.md)** for:
- Detailed configuration
- Troubleshooting
- Advanced features
- Security considerations

---

## ⚠️ Important Notes

1. **Administrator privileges required** - Packet capture needs elevated access
2. **Windows users**: May need to install Npcap from https://npcap.com/
3. **Linux users**: May need libpcap: `sudo apt-get install libpcap-dev`
4. **Performance**: Expect 10-30% CPU usage during active monitoring

---

## 🔄 Switch Back to Simulation Mode

Just stop the real-time monitoring script. The backend automatically returns to simulation mode.

---

**Happy threat hunting! 🎯**
