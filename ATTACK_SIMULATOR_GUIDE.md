# 🎯 Attack Simulator Guide

## What is This?

The **Attack Simulator** is a harmless testing tool that simulates various network attacks to demonstrate your Intrusion Detection System. No actual attacks are performed - it simply triggers the IDS to generate alerts.

## 🚀 How to Use

### Step 1: Make Sure Everything is Running

1. **Backend server** must be running on port 5000
2. **Frontend dashboard** must be open at http://localhost:5173

### Step 2: Run the Attack Simulator

Open a **third terminal** and run:

```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project"
python attack_simulator.py
```

### Step 3: Choose Your Attack

You'll see a menu with different attack types:

```
1. Port Scan Attack        [Medium]
2. DDoS Attack            [Critical]
3. SQL Injection          [High]
4. Brute Force            [High]
5. XSS Attack             [Medium]
6. Man-in-the-Middle      [Critical]
7. Malware Detection      [Critical]
8. Phishing Attempt       [Medium]
9. Continuous Attack Mode (Random)
0. Stress Test (All Attacks)
```

## 📋 Attack Types Explained

### 1. Port Scan Attack
- **Severity**: Medium
- **Description**: Simulates an attacker scanning your network ports
- **Use Case**: Demonstrate reconnaissance detection

### 2. DDoS Attack
- **Severity**: Critical
- **Description**: Simulates distributed denial of service
- **Use Case**: Show high-volume attack detection

### 3. SQL Injection
- **Severity**: High
- **Description**: Simulates database attack attempts
- **Use Case**: Demonstrate web application attack detection

### 4. Brute Force
- **Severity**: High
- **Description**: Simulates password cracking attempts
- **Use Case**: Show authentication attack detection

### 5. XSS Attack
- **Severity**: Medium
- **Description**: Simulates cross-site scripting
- **Use Case**: Demonstrate web security monitoring

### 6. Man-in-the-Middle
- **Severity**: Critical
- **Description**: Simulates traffic interception
- **Use Case**: Show network eavesdropping detection

### 7. Malware Detection
- **Severity**: Critical
- **Description**: Simulates malicious software traffic
- **Use Case**: Demonstrate malware detection capabilities

### 8. Phishing Attempt
- **Severity**: Medium
- **Description**: Simulates social engineering attacks
- **Use Case**: Show email/web phishing detection

### 9. Continuous Attack Mode
- **Description**: Randomly simulates different attacks every 2-5 seconds
- **Use Case**: Demonstrate real-time monitoring capabilities
- **Stop**: Press Ctrl+C

### 0. Stress Test
- **Description**: Launches ALL attack types simultaneously
- **Use Case**: Test system performance under heavy load
- **Warning**: Will flood your dashboard with alerts!

## 🎮 Intensity Levels

When you select an attack (1-8), you can choose intensity:

- **Light**: Fewer packets, slower attack
- **Normal**: Standard simulation (default)
- **Heavy**: 3x more packets, aggressive attack

## 💡 Demo Scenarios

### Scenario 1: Basic Demo
```
1. Choose option 2 (DDoS Attack)
2. Select Normal intensity
3. Watch alerts appear in real-time on dashboard
```

### Scenario 2: Continuous Monitoring
```
1. Choose option 9 (Continuous Attack Mode)
2. Watch different attack types appear randomly
3. Show real-time detection capabilities
4. Press Ctrl+C to stop
```

### Scenario 3: Stress Test
```
1. Choose option 0 (Stress Test)
2. Press ENTER to confirm
3. Watch dashboard flood with multiple alerts
4. Demonstrate system handling high load
```

## 🎬 Presentation Tips

1. **Open dashboard first** - Make sure audience can see it
2. **Explain what you're doing** - "I'm now simulating a DDoS attack..."
3. **Point out the alerts** - Show severity levels, IPs, timestamps
4. **Use continuous mode** - Great for live demonstrations
5. **Show the charts** - Point out threat distribution and trends

## ⚠️ Important Notes

- ✅ This is **completely safe** - no real attacks are performed
- ✅ Only sends harmless HTTP requests to your local server
- ✅ All alerts are simulated by the backend
- ✅ No network scanning or malicious activity
- ✅ Safe to use for presentations and testing

## 🔧 Troubleshooting

**"Backend server is not running"**
- Start the backend: `python backend/app.py`

**"No alerts appearing"**
- Check if frontend is connected (green status in header)
- Refresh the dashboard page
- Make sure backend is running without errors

**"Connection timeout"**
- Backend might be overloaded
- Wait a few seconds and try again
- Restart the backend server

## 🎯 Example Session

```bash
$ python attack_simulator.py

============================================================
🎯  IDS ATTACK SIMULATOR - TESTING TOOL
============================================================
⚠️  This is a HARMLESS testing tool
✅  Simulates attacks for demonstration purposes only
============================================================

✅ Backend server is running

📊 Open your dashboard at: http://localhost:5173
   Watch the alerts appear in real-time!

SELECT ATTACK TYPE:
────────────────────────────────────────────────────────────
  1. Port Scan Attack        [Medium]
  2. DDoS Attack            [Critical]
  ...

Enter your choice: 2

Select intensity:
  1. Light
  2. Normal
  3. Heavy

Enter intensity (default: 2): 3

🔴 Launching: DDoS Attack
   Description: Simulates distributed denial of service
   Severity: Critical
   Packets: 30
   Intensity: HEAVY

   [1/30] 📡 Packet sent... ✓
   [2/30] 📡 Packet sent... ✓
   ...

✅ DDoS Attack simulation complete!
   Check your dashboard for detected threats
```

## 🎓 Educational Use

This tool is perfect for:
- **Class presentations** on network security
- **Project demonstrations** 
- **Testing IDS functionality**
- **Understanding attack patterns**
- **Training security teams**

---

**Remember**: This is a demonstration tool. Always use responsibly and only on your own systems!
