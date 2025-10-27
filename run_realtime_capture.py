"""
Direct Real-time Packet Capture
Runs packet capture and sends alerts directly to the backend via SocketIO
No HTTP requests needed - uses WebSocket connection
"""

import sys
import time
from datetime import datetime

# Check admin privileges first
try:
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("\n❌ ERROR: Administrator privileges required!")
        print("   Please run PowerShell as Administrator")
        input("\nPress ENTER to exit...")
        sys.exit(1)
except:
    pass

print("\n" + "="*70)
print("🔍 REAL-TIME NETWORK MONITORING")
print("="*70)
print("✅ Running with administrator privileges\n")

# Import required libraries
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
    print("✅ Scapy is installed")
except ImportError:
    print("❌ Scapy not found!")
    print("   Install it: pip install scapy")
    input("\nPress ENTER to exit...")
    sys.exit(1)

try:
    import socketio
    print("✅ SocketIO client is available")
except ImportError:
    print("❌ SocketIO client not found!")
    print("   Install it: pip install python-socketio")
    input("\nPress ENTER to exit...")
    sys.exit(1)

from collections import defaultdict

# Connect to backend via WebSocket
print("\n🔌 Connecting to backend...")
sio = socketio.Client()

try:
    sio.connect('http://localhost:5000')
    print("✅ Connected to backend server\n")
except Exception as e:
    print(f"❌ Could not connect to backend: {e}")
    print("   Make sure the backend is running: python backend/app.py")
    input("\nPress ENTER to exit...")
    sys.exit(1)

# Tracking dictionaries
port_scan_tracker = defaultdict(lambda: {'ports': set(), 'last_seen': datetime.now()})
syn_flood_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
packet_rate_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})

# Thresholds
PORT_SCAN_THRESHOLD = 10
SYN_FLOOD_THRESHOLD = 50
PACKET_RATE_THRESHOLD = 100

# Suspicious ports
SUSPICIOUS_PORTS = {
    23: 'Telnet', 135: 'RPC', 139: 'NetBIOS', 445: 'SMB',
    3389: 'RDP', 5900: 'VNC', 1433: 'MSSQL', 3306: 'MySQL'
}

# Malicious patterns
MALICIOUS_PATTERNS = [
    b'<script', b'javascript:', b'SELECT * FROM', b'UNION SELECT',
    b'DROP TABLE', b'../../', b'cmd.exe', b'/bin/bash'
]

alert_count = 0

def send_alert(alert_data):
    """Send alert to backend via WebSocket"""
    global alert_count
    alert_count += 1
    
    alert_data['timestamp'] = datetime.now().isoformat()
    alert_data['status'] = 'Active'
    
    # Emit to backend
    try:
        sio.emit('trigger_alert', alert_data)
        print(f"🚨 [{alert_count}] {alert_data['threat_type']} from {alert_data['source_ip']}")
    except:
        pass

def analyze_packet(packet):
    """Analyze packet for threats"""
    try:
        if IP not in packet:
            return
        
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Skip localhost traffic
        if src_ip.startswith('127.') or dst_ip.startswith('127.'):
            return
        
        # Port scan detection
        if TCP in packet:
            dst_port = packet[TCP].dport
            port_scan_tracker[src_ip]['ports'].add(dst_port)
            
            if len(port_scan_tracker[src_ip]['ports']) >= PORT_SCAN_THRESHOLD:
                send_alert({
                    'threat_type': 'Port Scan',
                    'severity': 'High',
                    'source_ip': src_ip,
                    'destination_ip': dst_ip,
                    'description': f'Port scan detected: {len(port_scan_tracker[src_ip]["ports"])} ports',
                    'port': dst_port,
                    'protocol': 'TCP'
                })
                port_scan_tracker[src_ip]['ports'].clear()
            
            # SYN flood detection
            if packet[TCP].flags == 'S':
                syn_flood_tracker[src_ip]['count'] += 1
                if syn_flood_tracker[src_ip]['count'] >= SYN_FLOOD_THRESHOLD:
                    send_alert({
                        'threat_type': 'DDoS Attack',
                        'severity': 'Critical',
                        'source_ip': src_ip,
                        'destination_ip': dst_ip,
                        'description': f'SYN flood: {syn_flood_tracker[src_ip]["count"]} packets',
                        'port': dst_port,
                        'protocol': 'TCP'
                    })
                    syn_flood_tracker[src_ip]['count'] = 0
            
            # Suspicious ports
            if dst_port in SUSPICIOUS_PORTS:
                send_alert({
                    'threat_type': 'Suspicious Connection',
                    'severity': 'Medium',
                    'source_ip': src_ip,
                    'destination_ip': dst_ip,
                    'description': f'Connection to {SUSPICIOUS_PORTS[dst_port]} port',
                    'port': dst_port,
                    'protocol': 'TCP'
                })
        
        # Malicious payload detection
        if Raw in packet:
            payload = bytes(packet[Raw].load)
            for pattern in MALICIOUS_PATTERNS:
                if pattern in payload.lower():
                    threat_type = 'SQL Injection' if b'SELECT' in pattern else \
                                  'XSS Attack' if b'script' in pattern else \
                                  'Malicious Payload'
                    
                    send_alert({
                        'threat_type': threat_type,
                        'severity': 'High',
                        'source_ip': src_ip,
                        'destination_ip': dst_ip,
                        'description': f'Malicious pattern detected',
                        'port': packet[TCP].dport if TCP in packet else 0,
                        'protocol': 'TCP' if TCP in packet else 'UDP'
                    })
                    break
        
        # Packet rate tracking
        packet_rate_tracker[src_ip]['count'] += 1
        if packet_rate_tracker[src_ip]['count'] >= PACKET_RATE_THRESHOLD:
            send_alert({
                'threat_type': 'DDoS Attack',
                'severity': 'Critical',
                'source_ip': src_ip,
                'destination_ip': dst_ip,
                'description': f'High packet rate: {packet_rate_tracker[src_ip]["count"]} packets',
                'port': 0,
                'protocol': 'Multiple'
            })
            packet_rate_tracker[src_ip]['count'] = 0
            
    except Exception as e:
        pass

print("="*70)
print("🚀 STARTING REAL-TIME PACKET CAPTURE")
print("="*70)
print("\n⚠️  Capturing ALL network traffic on your laptop")
print("📊 Open dashboard at: http://localhost:5173")
print("   Watch real threats appear in real-time!")
print("\n🎯 MONITORING ACTIVE - Press Ctrl+C to stop\n")

try:
    sniff(prn=analyze_packet, store=False)
except KeyboardInterrupt:
    print("\n\n🛑 Stopping packet capture...")
    sio.disconnect()
    print(f"✅ Captured {alert_count} threats")
    print("\n👋 Real-time monitoring stopped. Goodbye!\n")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("💡 Make sure you're running as administrator")
    sio.disconnect()
    input("\nPress ENTER to exit...")
