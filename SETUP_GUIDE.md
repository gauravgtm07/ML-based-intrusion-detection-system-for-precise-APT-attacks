# Quick Setup Guide

## Step 1: Backend Setup (5 minutes)

1. Open a terminal and navigate to the backend folder:
```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\backend"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
.\venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Start the Flask server:
```bash
python app.py
```

You should see:
```
🚀 IDS Backend Server Starting...
📊 Dashboard: http://localhost:5000
🔌 WebSocket: ws://localhost:5000/socket.io
```

**Keep this terminal open!**

## Step 2: Frontend Setup (5 minutes)

1. Open a **NEW** terminal and navigate to the frontend folder:
```bash
cd "c:\Users\AMAR BIRADAR\OneDrive\Desktop\Intrusion Project\frontend"
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

You should see:
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
```

4. Open your browser and go to: **http://localhost:5173**

## What You'll See

✅ **Real-time Dashboard** with live threat monitoring  
✅ **Network Statistics** showing packets, threats, and connections  
✅ **Live Alert Feed** with color-coded severity levels  
✅ **Interactive Charts** for threat analysis  
✅ **WebSocket Connection** indicator in the header  

## Troubleshooting

### Backend Issues

**Error: "No module named 'flask'"**
- Make sure you activated the virtual environment
- Run: `pip install -r requirements.txt`

**Error: "Address already in use"**
- Port 5000 is occupied
- Stop any other Flask apps or change the port in `app.py`

### Frontend Issues

**Error: "command not found: npm"**
- Install Node.js from https://nodejs.org/

**Error: "Cannot connect to backend"**
- Make sure the Flask server is running on port 5000
- Check if you see the backend startup messages

**Blank page or errors**
- Clear browser cache
- Check browser console (F12) for errors
- Make sure both servers are running

## Testing the System

Once both servers are running:

1. Watch the **Live Alerts** panel - new threats appear every 3-8 seconds
2. Monitor the **Stats Cards** - numbers update in real-time
3. Check the **Connection Status** in the header (should be green)
4. Explore the **Charts** - they show threat patterns and distributions

## Stopping the Servers

- Backend: Press `Ctrl+C` in the backend terminal
- Frontend: Press `Ctrl+C` in the frontend terminal

## Next Steps

- Customize alert types in `backend/app.py`
- Modify UI colors in `frontend/src/index.css`
- Add more charts in `frontend/src/components/ThreatCharts.tsx`
- Integrate real network monitoring tools (Scapy, Suricata, etc.)

---

**Need help?** Check the main README.md for detailed documentation.
