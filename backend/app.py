from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import random
import time
from datetime import datetime, timedelta
import threading
import os
import sys

# Import email service
try:
    from email_service import email_service
    EMAIL_SERVICE_AVAILABLE = True
except ImportError:
    EMAIL_SERVICE_AVAILABLE = False
    print("⚠️  Email service not available.")

# Import packet sniffer (optional - will work in simulation mode if not available)
try:
    from packet_sniffer import PacketAnalyzer
    PACKET_CAPTURE_AVAILABLE = True
except ImportError:
    PACKET_CAPTURE_AVAILABLE = False
    print("⚠️  Packet capture not available. Running in simulation mode.")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# Data storage
alerts = []
threat_data = []
blocked_ips_list = []  # List of blocked IP addresses
network_stats = {
    'total_packets': 0,
    'threats_detected': 0,
    'blocked_ips': 0,
    'active_connections': 0
}

# Packet analyzer instance
packet_analyzer = None
REAL_TIME_MODE = False  # Toggle between real packet capture and simulation

# Threat types and severity levels
THREAT_TYPES = [
    'Port Scan', 'DDoS Attack', 'SQL Injection', 'XSS Attack',
    'Brute Force', 'Malware', 'Phishing', 'Man-in-the-Middle',
    'Buffer Overflow', 'Zero-Day Exploit'
]

SEVERITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']

def generate_ip():
    """Generate a random IP address"""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def generate_alert():
    """Generate a simulated security alert"""
    severity = random.choice(SEVERITY_LEVELS)
    threat_type = random.choice(THREAT_TYPES)
    
    alert = {
        'id': len(alerts) + 1,
        'timestamp': datetime.now().isoformat(),
        'source_ip': generate_ip(),
        'destination_ip': generate_ip(),
        'threat_type': threat_type,
        'severity': severity,
        'status': random.choice(['Active', 'Blocked', 'Investigating']),
        'description': f"{threat_type} detected from suspicious source",
        'port': random.randint(1, 65535),
        'protocol': random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS'])
    }
    
    return alert

def generate_threat_stats():
    """Generate threat statistics for charts"""
    stats = []
    for i in range(24):
        hour = (datetime.now() - timedelta(hours=23-i)).strftime('%H:00')
        stats.append({
            'time': hour,
            'threats': random.randint(5, 50),
            'blocked': random.randint(3, 40),
            'allowed': random.randint(100, 500)
        })
    return stats

def handle_real_alert(alert_data):
    """Handle alerts from real packet capture"""
    alert = {
        'id': len(alerts) + 1,
        'timestamp': alert_data.get('timestamp', datetime.now().isoformat()),
        'source_ip': alert_data.get('source_ip', 'Unknown'),
        'destination_ip': alert_data.get('destination_ip', 'Unknown'),
        'threat_type': alert_data.get('threat_type', 'Unknown'),
        'severity': alert_data.get('severity', 'Medium'),
        'status': alert_data.get('status', 'Active'),
        'description': alert_data.get('description', 'Threat detected'),
        'port': alert_data.get('port', 0),
        'protocol': alert_data.get('protocol', 'Unknown')
    }
    
    # Add to alerts list
    alerts.insert(0, alert)
    if len(alerts) > 100:
        alerts.pop()
    
    # Update stats
    network_stats['threats_detected'] += 1
    if alert['severity'] in ['High', 'Critical']:
        network_stats['blocked_ips'] += 1
    
    # Emit via WebSocket
    socketio.emit('new_alert', alert)
    socketio.emit('stats_update', network_stats)
    
    print(f"🚨 Real threat detected: {alert['threat_type']} from {alert['source_ip']}")

def background_monitoring():
    """Simulate real-time monitoring in background (only when not in real-time mode)"""
    while True:
        time.sleep(random.uniform(6, 7.5))  # 8-10 attacks per minute
        
        # Skip simulation if real-time mode is active
        if REAL_TIME_MODE:
            continue
        
        # Generate new alert
        alert = generate_alert()
        alerts.insert(0, alert)
        
        # Keep only last 100 alerts
        if len(alerts) > 100:
            alerts.pop()
        
        # Update network stats
        network_stats['total_packets'] += random.randint(10, 100)
        network_stats['active_connections'] = random.randint(50, 200)
        
        if alert['severity'] in ['High', 'Critical']:
            network_stats['threats_detected'] += 1
            if alert['status'] == 'Blocked':
                network_stats['blocked_ips'] += 1
        
        # Emit real-time update via WebSocket
        socketio.emit('new_alert', alert)
        socketio.emit('stats_update', network_stats)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts with optional filtering"""
    severity = request.args.get('severity')
    limit = request.args.get('limit', type=int, default=50)
    
    filtered_alerts = alerts
    if severity:
        filtered_alerts = [a for a in alerts if a['severity'] == severity]
    
    return jsonify({
        'alerts': filtered_alerts[:limit],
        'total': len(filtered_alerts)
    })

@app.route('/api/alerts/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get specific alert by ID"""
    alert = next((a for a in alerts if a['id'] == alert_id), None)
    if alert:
        return jsonify(alert)
    return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current network statistics"""
    return jsonify(network_stats)

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get threat statistics for visualization"""
    return jsonify({
        'hourly_stats': generate_threat_stats(),
        'threat_distribution': [
            {'name': 'Port Scan', 'value': random.randint(10, 50)},
            {'name': 'DDoS', 'value': random.randint(5, 30)},
            {'name': 'SQL Injection', 'value': random.randint(8, 25)},
            {'name': 'XSS', 'value': random.randint(6, 20)},
            {'name': 'Brute Force', 'value': random.randint(10, 35)},
            {'name': 'Other', 'value': random.randint(5, 15)}
        ],
        'severity_breakdown': {
            'Low': random.randint(20, 50),
            'Medium': random.randint(15, 40),
            'High': random.randint(10, 30),
            'Critical': random.randint(5, 15)
        }
    })

@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    """Trigger a network scan"""
    data = request.get_json()
    target = data.get('target', 'all')
    
    # Simulate scan
    scan_result = {
        'scan_id': random.randint(1000, 9999),
        'target': target,
        'status': 'initiated',
        'timestamp': datetime.now().isoformat(),
        'estimated_duration': '2-5 minutes'
    }
    
    return jsonify(scan_result)

@app.route('/api/block-ip', methods=['POST'])
def block_ip():
    """Block an IP address"""
    data = request.get_json()
    ip_address = data.get('ip')
    alert_id = data.get('alert_id')
    
    if not ip_address:
        return jsonify({'error': 'IP address required'}), 400
    
    # Add to blocked IPs list if not already blocked
    if ip_address not in blocked_ips_list:
        blocked_ips_list.append(ip_address)
        network_stats['blocked_ips'] += 1
    
    # Update the alert status to 'Blocked' if alert_id is provided
    if alert_id:
        for alert in alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'Blocked'
                # Emit updated alert
                socketio.emit('alert_updated', alert)
                break
    
    return jsonify({
        'status': 'success',
        'message': f'IP {ip_address} has been blocked',
        'timestamp': datetime.now().isoformat(),
        'blocked_ip': ip_address
    })

@app.route('/api/blocked-ips', methods=['GET'])
def get_blocked_ips():
    """Get list of all blocked IPs"""
    return jsonify({
        'blocked_ips': blocked_ips_list,
        'total': len(blocked_ips_list)
    })

@app.route('/api/alerts/export', methods=['GET'])
def export_alerts_csv():
    """Export alerts to CSV format"""
    import csv
    from io import StringIO
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Timestamp', 'Source IP', 'Destination IP', 'Threat Type', 
                     'Severity', 'Status', 'Description', 'Port', 'Protocol'])
    
    # Write data
    for alert in alerts:
        writer.writerow([
            alert['id'],
            alert['timestamp'],
            alert['source_ip'],
            alert['destination_ip'],
            alert['threat_type'],
            alert['severity'],
            alert['status'],
            alert['description'],
            alert['port'],
            alert['protocol']
        ])
    
    # Get CSV content
    csv_content = output.getvalue()
    output.close()
    
    # Return as downloadable file
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=alerts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )

@app.route('/api/alerts/filter-by-time', methods=['GET'])
def filter_alerts_by_time():
    """Filter alerts by time period"""
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({'error': 'start_time and end_time are required'}), 400
    
    try:
        # Parse time strings - strip timezone info to make them naive
        start_dt = datetime.fromisoformat(start_time.replace('Z', '').split('+')[0].split('-05:30')[0])
        end_dt = datetime.fromisoformat(end_time.replace('Z', '').split('+')[0].split('-05:30')[0])
        
        # Filter alerts
        filtered_alerts = []
        for alert in alerts:
            # Parse alert timestamp - strip timezone info to make it naive
            alert_timestamp_str = alert['timestamp'].replace('Z', '').split('+')[0].split('-05:30')[0]
            alert_dt = datetime.fromisoformat(alert_timestamp_str)
            
            if start_dt <= alert_dt <= end_dt:
                filtered_alerts.append(alert)
        
        return jsonify({
            'alerts': filtered_alerts,
            'total': len(filtered_alerts),
            'start_time': start_time,
            'end_time': end_time
        })
    except Exception as e:
        return jsonify({'error': f'Invalid time format: {str(e)}'}), 400

@app.route('/api/trigger-alert', methods=['POST'])
def trigger_alert():
    """Trigger a custom alert (for testing/simulation)"""
    data = request.get_json()
    
    threat_type = data.get('threat_type', random.choice(THREAT_TYPES))
    severity = data.get('severity', random.choice(SEVERITY_LEVELS))
    
    # Create custom alert
    alert = {
        'id': len(alerts) + 1,
        'timestamp': datetime.now().isoformat(),
        'source_ip': data.get('source_ip', generate_ip()),
        'destination_ip': data.get('destination_ip', generate_ip()),
        'threat_type': threat_type,
        'severity': severity,
        'status': data.get('status', random.choice(['Active', 'Blocked', 'Investigating'])),
        'description': data.get('description', f"{threat_type} detected from suspicious source"),
        'port': data.get('port', random.randint(1, 65535)),
        'protocol': data.get('protocol', random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS']))
    }
    
    # Add to alerts list
    alerts.insert(0, alert)
    if len(alerts) > 100:
        alerts.pop()
    
    # Update stats
    network_stats['total_packets'] += random.randint(10, 50)
    if severity in ['High', 'Critical']:
        network_stats['threats_detected'] += 1
        if alert['status'] == 'Blocked':
            network_stats['blocked_ips'] += 1
    
    # Emit via WebSocket
    socketio.emit('new_alert', alert)
    socketio.emit('stats_update', network_stats)
    
    return jsonify({
        'status': 'success',
        'alert': alert,
        'message': 'Alert triggered successfully'
    })

@app.route('/api/send-email-alert', methods=['POST'])
def send_email_alert():
    """Send email alert"""
    data = request.get_json()
    
    # Log the email alert request
    print(f"📧 Email Alert Request:")
    print(f"   Threat: {data.get('threat_type')}")
    print(f"   Severity: {data.get('severity')}")
    print(f"   Source IP: {data.get('source_ip')}")
    print(f"   Description: {data.get('description')}")
    
    # Send email if service is available
    if EMAIL_SERVICE_AVAILABLE:
        result = email_service.send_alert_email(data)
        return jsonify({
            'status': result.get('status'),
            'message': result.get('message'),
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'status': 'unavailable',
            'message': 'Email service not configured. See backend/.env.example for setup instructions.',
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/realtime/start', methods=['POST'])
def start_realtime_capture():
    """Start real-time packet capture"""
    global packet_analyzer, REAL_TIME_MODE
    
    if not PACKET_CAPTURE_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'Packet capture not available. Install scapy: pip install scapy'
        }), 400
    
    if REAL_TIME_MODE:
        return jsonify({
            'status': 'warning',
            'message': 'Real-time capture is already running'
        }), 200
    
    try:
        data = request.get_json() or {}
        interface = data.get('interface', None)
        
        # Initialize packet analyzer
        packet_analyzer = PacketAnalyzer(alert_callback=handle_real_alert)
        packet_analyzer.start_sniffing(interface=interface)
        
        REAL_TIME_MODE = True
        
        return jsonify({
            'status': 'success',
            'message': 'Real-time packet capture started',
            'interface': interface or 'default',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to start capture: {str(e)}'
        }), 500

@app.route('/api/realtime/stop', methods=['POST'])
def stop_realtime_capture():
    """Stop real-time packet capture"""
    global packet_analyzer, REAL_TIME_MODE
    
    if not REAL_TIME_MODE:
        return jsonify({
            'status': 'warning',
            'message': 'Real-time capture is not running'
        }), 200
    
    try:
        if packet_analyzer:
            packet_analyzer.stop_sniffing()
            packet_analyzer = None
        
        REAL_TIME_MODE = False
        
        return jsonify({
            'status': 'success',
            'message': 'Real-time packet capture stopped',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to stop capture: {str(e)}'
        }), 500

@app.route('/api/realtime/status', methods=['GET'])
def get_realtime_status():
    """Get real-time capture status"""
    return jsonify({
        'available': PACKET_CAPTURE_AVAILABLE,
        'running': REAL_TIME_MODE,
        'mode': 'real-time' if REAL_TIME_MODE else 'simulation',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('request_stats')
def handle_stats_request():
    """Handle stats request via WebSocket"""
    emit('stats_update', network_stats)

@socketio.on('enable_realtime_mode')
def handle_enable_realtime(data):
    """Enable real-time mode and disable simulation"""
    global REAL_TIME_MODE
    REAL_TIME_MODE = data.get('enabled', True)
    mode = 'REAL-TIME' if REAL_TIME_MODE else 'SIMULATION'
    print(f'🔄 Mode switched to: {mode}')
    emit('mode_changed', {'mode': mode, 'realtime': REAL_TIME_MODE})

@socketio.on('trigger_alert')
def handle_trigger_alert(data):
    """Handle alert triggered from real-time packet capture"""
    handle_real_alert(data)

if __name__ == '__main__':
    # Initialize with some sample data
    for _ in range(20):
        alerts.append(generate_alert())
    
    # Start background monitoring thread
    monitor_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitor_thread.start()
    
    print("🚀 IDS Backend Server Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔌 WebSocket: ws://localhost:5000/socket.io")
    
    if PACKET_CAPTURE_AVAILABLE:
        print("✅ Real-time packet capture: AVAILABLE")
        print("   Use POST /api/realtime/start to enable live detection")
        print("   ⚠️  Requires administrator/root privileges")
    else:
        print("⚠️  Real-time packet capture: NOT AVAILABLE")
        print("   Running in simulation mode only")
        print("   To enable: pip install scapy")
    
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
