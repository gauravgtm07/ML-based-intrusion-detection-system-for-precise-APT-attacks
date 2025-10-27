# Intrusion Detection System Web Portal

A modern, fast, and reliable web portal for real-time intrusion detection and network security monitoring.

## 🚀 Features

- **🔐 Secure Authentication**: User login/signup powered by Supabase
- **🔴 REAL Packet Capture**: Analyze live network traffic from your laptop (requires admin privileges)
- **Real-time Monitoring**: Live dashboard with WebSocket support for instant threat detection
- **Advanced Analytics**: Comprehensive threat analysis and visualization
- **Alert System**: Instant notifications for security events
- **Traffic Analysis**: Network traffic monitoring and pattern detection
- **Dual Mode**: Switch between real packet capture and simulation mode
- **Modern UI**: Beautiful, responsive interface built with React and TailwindCSS
- **RESTful API**: Flask-based backend with comprehensive endpoints
- **Session Management**: Secure user sessions with automatic persistence

## 🛠️ Technology Stack

### Frontend
- React 18 with TypeScript
- Supabase for authentication
- TailwindCSS for styling
- shadcn/ui components
- Recharts for data visualization
- Lucide React for icons
- Axios for API calls
- Socket.IO client for real-time updates

### Backend
- Flask (Python 3.9+)
- Flask-CORS for cross-origin support
- Flask-SocketIO for real-time communication
- Scapy for network packet analysis
- SQLite for data storage

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- pip

## 🔧 Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## 🎯 Usage

### First Time Setup
1. Start the backend and frontend servers (see Installation above)
2. Open your browser to `http://localhost:5173`
3. **Create an account** - Click "Sign up" and register with email/password
4. **Login** - Use your credentials to access the dashboard

📖 **See [AUTH_SETUP.md](AUTH_SETUP.md) for authentication details**

### Simulation Mode (Default)
1. Start the backend server first
2. Start the frontend development server
3. Login to access the dashboard
4. Monitor simulated intrusion detection events on the dashboard

### 🔴 Real-time Packet Capture Mode
**Detects ACTUAL threats from your laptop's network traffic!**

1. Start the backend server
2. Start the frontend
3. **Run as administrator**: `python start_realtime_monitoring.py`
4. Watch real threats appear on the dashboard!

📖 **See [REALTIME_SETUP.md](REALTIME_SETUP.md) for detailed setup guide**

## 📊 Dashboard Features

- **User Authentication**: Secure login/signup system
- **Live Threat Feed**: Real-time display of detected threats
- **Network Statistics**: Traffic analysis and metrics
- **Alert Management**: View and manage security alerts
- **Threat Severity Levels**: Color-coded threat classification
- **Historical Data**: View past intrusion attempts
- **User Profile**: Display logged-in user with logout option

## 🔒 Security Features

### Real-time Detection (when enabled)
- **Port scanning detection** - Monitors access to multiple ports
- **DDoS attack detection** - SYN floods, ICMP floods, high packet rates
- **SQL injection detection** - Analyzes payloads for SQL patterns
- **XSS attack detection** - Detects cross-site scripting attempts
- **Suspicious connections** - Monitors dangerous ports (Telnet, SMB, RDP, etc.)
- **Malicious payload identification** - Command injection, path traversal
- **Protocol analysis** - TCP, UDP, ICMP traffic analysis
- **Anomaly detection** - Unusual traffic patterns

## 📝 API Endpoints

### Standard Endpoints
- `GET /api/alerts` - Retrieve all alerts
- `GET /api/stats` - Get system statistics
- `GET /api/threats` - Get threat data
- `POST /api/scan` - Trigger network scan
- `WebSocket /socket.io` - Real-time updates

### Real-time Packet Capture
- `POST /api/realtime/start` - Start live packet capture
- `POST /api/realtime/stop` - Stop live packet capture
- `GET /api/realtime/status` - Check capture status

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 👨‍💻 Author

Created with ❤️ for network security monitoring
