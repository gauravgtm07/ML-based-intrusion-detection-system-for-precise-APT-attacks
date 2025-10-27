# ⚡ Quick Start Guide - IDS Project

## 🎯 Complete Setup in 3 Terminals

### Terminal 1: Backend Server
```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\backend"
.\venv\Scripts\activate
python app.py
```
**Wait for**: `🚀 IDS Backend Server Starting...`

---

### Terminal 2: Frontend Dashboard
```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\frontend"
npm run dev
```
**Open browser**: http://localhost:5173

---

### Terminal 3: Attack Simulator (Optional)
```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project"
python attack_simulator.py
```
**Choose attacks** to see them appear on dashboard!

---

## 🎮 Quick Demo

1. **Start all three terminals** (as shown above)
2. **Open dashboard** in browser
3. **Run attack simulator** - Choose option `9` for continuous attacks
4. **Watch live alerts** appear in real-time!

---

## 🎬 For Presentations

**Best Demo Flow:**
1. Show the dashboard (explain the UI)
2. Run attack simulator with option `2` (DDoS - Critical severity)
3. Point out the red alert appearing
4. Switch to option `9` (Continuous mode)
5. Show charts updating in real-time
6. Run option `0` (Stress test) for dramatic effect!

---

## 🛑 Stop Everything

Press `Ctrl+C` in each terminal window.

---

## ✅ You're All Set!

Your Intrusion Detection System is now running with:
- ✅ Real-time threat monitoring
- ✅ Live dashboard with charts
- ✅ Attack simulation for testing
- ✅ WebSocket updates
