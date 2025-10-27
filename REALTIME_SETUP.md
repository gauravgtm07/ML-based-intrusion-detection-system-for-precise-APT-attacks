# 🔴 Real-time Network Monitoring Setup Guide

This guide will help you enable **REAL packet capture** to detect actual threats on your laptop's network traffic.

---

## ⚠️ Important Requirements

### 1. Administrator/Root Privileges
Real-time packet capture requires elevated privileges:
- **Windows**: Run as Administrator
- **Linux/Mac**: Run with `sudo`

### 2. Scapy Library
Install the packet capture library:
```bash
pip install scapy
```

### 3. Network Permissions
- Windows: May require WinPcap or Npcap driver
- Linux: Requires libpcap
- Mac: Built-in support

---

## 🚀 Quick Start - Real-time Monitoring

### Method 1: Using the Helper Script (Recommended)

1. **Start the backend** (in one terminal):
```bash
cd backend
python app.py
```

2. **Start real-time monitoring** (in another terminal, **as administrator**):
```bash
# Windows (Run PowerShell as Administrator)
python start_realtime_monitoring.py

# Linux/Mac
sudo python start_realtime_monitoring.py
```

3. **Open the dashboard**:
```
http://localhost:5173
```

4. **Watch real threats appear** as they happen on your network!

---

### Method 2: Using API Calls

Start the backend, then make API calls:

**Start real-time capture:**
```bash
curl -X POST http://localhost:5000/api/realtime/start
```

**Check status:**
```bash
curl http://localhost:5000/api/realtime/status
```

**Stop capture:**
```bash
curl -X POST http://localhost:5000/api/realtime/stop
```

---

## 🎯 What Gets Detected

The system analyzes **every packet** on your network and detects:

### 1. **Port Scanning**
- Detects when someone scans multiple ports on your system
- Threshold: 10+ different ports accessed

### 2. **DDoS Attacks**
- SYN flood detection (50+ SYN packets)
- High packet rate detection (100+ packets/sec from single IP)
- ICMP flood detection (30+ ICMP packets)

### 3. **SQL Injection**
- Detects SQL injection patterns in packet payloads
- Patterns: `SELECT * FROM`, `UNION SELECT`, `DROP TABLE`

### 4. **XSS Attacks**
- Detects cross-site scripting attempts
- Patterns: `<script>`, `javascript:`, `eval()`

### 5. **Suspicious Connections**
- Monitors connections to dangerous ports:
  - Port 23 (Telnet)
  - Port 445 (SMB)
  - Port 3389 (RDP)
  - Port 3306 (MySQL)
  - And more...

### 6. **Malicious Payloads**
- Command injection attempts
- Path traversal (`../../`)
- Encoded malicious code

---

## 🔧 Configuration

### Adjust Detection Thresholds

Edit `backend/packet_sniffer.py`:

```python
# Thresholds for detection
self.PORT_SCAN_THRESHOLD = 10      # Number of ports
self.SYN_FLOOD_THRESHOLD = 50      # SYN packets
self.PACKET_RATE_THRESHOLD = 100   # Packets per second
self.TIME_WINDOW = 10              # Time window in seconds
```

### Select Network Interface

By default, the system captures on all interfaces. To specify:

```python
# In start_realtime_monitoring.py, modify the start call:
response = requests.post(
    f"{API_BASE}/realtime/start", 
    json={'interface': 'eth0'},  # Your interface name
    timeout=5
)
```

To list available interfaces:
```python
from scapy.all import get_if_list
print(get_if_list())
```

---

## 🧪 Testing Real-time Detection

### Test 1: Port Scan Detection
Use `nmap` to scan your own machine:
```bash
nmap -p 1-100 localhost
```
You should see a "Port Scan" alert appear on the dashboard!

### Test 2: High Traffic Detection
Generate traffic with `ping`:
```bash
# Windows
ping -t -l 65500 localhost

# Linux/Mac
ping -f localhost
```

### Test 3: Suspicious Port Connection
Try connecting to a suspicious port:
```bash
telnet localhost 23
```

---

## 📊 Dashboard Integration

When real-time mode is active:
- ✅ Simulation mode is automatically disabled
- 🔴 Only **real threats** appear on the dashboard
- 📈 All charts show **actual network data**
- 🚨 Alerts are triggered by **real packet analysis**

---

## 🛑 Stopping Real-time Monitoring

### Option 1: Using the script
Press `Ctrl+C` in the terminal running `start_realtime_monitoring.py`

### Option 2: Using API
```bash
curl -X POST http://localhost:5000/api/realtime/stop
```

### Option 3: Restart backend
Simply restart the backend server (it starts in simulation mode by default)

---

## ⚡ Performance Considerations

### CPU Usage
- Real-time packet capture is CPU-intensive
- Expect 10-30% CPU usage depending on network traffic
- High traffic networks may require more resources

### Memory Usage
- The system keeps last 100 alerts in memory
- Old tracking data is cleaned every 10 seconds
- Typical memory usage: 50-100 MB

### Network Impact
- Packet capture is **passive** - no packets are injected
- No impact on network performance
- Only reads packets, doesn't modify or block them

---

## 🐛 Troubleshooting

### "Permission denied" error
**Solution**: Run with administrator/root privileges

### "Packet capture not available"
**Solution**: Install Scapy: `pip install scapy`

### "No suitable device found"
**Solution**: 
- Windows: Install Npcap from https://npcap.com/
- Linux: Install libpcap: `sudo apt-get install libpcap-dev`

### No alerts appearing
**Possible causes**:
1. No actual threats on your network (good!)
2. Wrong network interface selected
3. Firewall blocking packet capture

**Solution**: Test with the testing methods above

### Too many false positives
**Solution**: Adjust thresholds in `packet_sniffer.py` (increase values)

---

## 🔒 Security & Privacy

### What data is captured?
- Source/destination IP addresses
- Port numbers
- Protocol types
- Packet payloads (analyzed, not stored)

### What is NOT stored?
- Full packet contents
- Personal data
- Passwords or credentials
- File contents

### Data retention
- Only last 100 alerts are kept
- No persistent storage of packet data
- All data cleared on server restart

---

## 📝 API Endpoints

### Start Real-time Capture
```
POST /api/realtime/start
Body: { "interface": "eth0" }  // optional
```

### Stop Real-time Capture
```
POST /api/realtime/stop
```

### Get Status
```
GET /api/realtime/status
Response: {
  "available": true,
  "running": false,
  "mode": "simulation",
  "timestamp": "2024-10-24T11:39:00"
}
```

---

## 🎓 Learning Resources

### Understanding the Code
- `backend/packet_sniffer.py` - Packet capture and analysis
- `backend/app.py` - Integration with Flask backend
- `start_realtime_monitoring.py` - Helper script

### Scapy Documentation
- Official docs: https://scapy.readthedocs.io/
- Packet sniffing: https://scapy.readthedocs.io/en/latest/usage.html#sniffing

### Network Security Concepts
- Port scanning
- DDoS attacks
- Intrusion detection systems
- Packet analysis

---

## ✅ Checklist

Before starting real-time monitoring:

- [ ] Backend server is running
- [ ] Scapy is installed (`pip install scapy`)
- [ ] Running with administrator/root privileges
- [ ] Network drivers installed (Npcap on Windows)
- [ ] Dashboard is open in browser
- [ ] Firewall allows packet capture

---

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Verify all requirements are met
4. Test with the provided testing methods

---

**Happy threat hunting! 🎯**
