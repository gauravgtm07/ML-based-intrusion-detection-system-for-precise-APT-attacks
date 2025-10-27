"""
Real-time Network Packet Sniffer and Analyzer
Captures live network traffic and detects potential security threats
Requires administrator/root privileges to run
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from collections import defaultdict
import threading
import time
from datetime import datetime, timedelta

class PacketAnalyzer:
    def __init__(self, alert_callback=None):
        """
        Initialize the packet analyzer
        
        Args:
            alert_callback: Function to call when a threat is detected
        """
        self.alert_callback = alert_callback
        self.running = False
        self.sniffer_thread = None
        
        # Tracking dictionaries for anomaly detection
        self.connection_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        self.port_scan_tracker = defaultdict(lambda: {'ports': set(), 'last_seen': datetime.now()})
        self.syn_flood_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        self.packet_rate_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        
        # Thresholds for detection
        self.PORT_SCAN_THRESHOLD = 10  # Number of different ports accessed
        self.SYN_FLOOD_THRESHOLD = 50  # Number of SYN packets in time window
        self.PACKET_RATE_THRESHOLD = 100  # Packets per second from single IP
        self.TIME_WINDOW = 10  # seconds
        
        # Suspicious ports
        self.SUSPICIOUS_PORTS = {
            23: 'Telnet',
            135: 'RPC',
            139: 'NetBIOS',
            445: 'SMB',
            3389: 'RDP',
            5900: 'VNC',
            1433: 'MSSQL',
            3306: 'MySQL',
            5432: 'PostgreSQL'
        }
        
        # Known malicious patterns in payloads
        self.MALICIOUS_PATTERNS = [
            b'<script',
            b'javascript:',
            b'SELECT * FROM',
            b'UNION SELECT',
            b'DROP TABLE',
            b'../../',
            b'cmd.exe',
            b'/bin/bash',
            b'eval(',
            b'base64_decode'
        ]
    
    def start_sniffing(self, interface=None):
        """Start packet sniffing in a separate thread"""
        if self.running:
            print("⚠️  Sniffer is already running")
            return
        
        self.running = True
        self.sniffer_thread = threading.Thread(
            target=self._sniff_packets,
            args=(interface,),
            daemon=True
        )
        self.sniffer_thread.start()
        print(f"✅ Packet sniffer started on interface: {interface or 'default'}")
    
    def stop_sniffing(self):
        """Stop packet sniffing"""
        self.running = False
        if self.sniffer_thread:
            self.sniffer_thread.join(timeout=2)
        print("🛑 Packet sniffer stopped")
    
    def _sniff_packets(self, interface):
        """Internal method to sniff packets"""
        try:
            sniff(
                iface=interface,
                prn=self.analyze_packet,
                store=False,
                stop_filter=lambda x: not self.running
            )
        except Exception as e:
            print(f"❌ Sniffing error: {str(e)}")
            print("💡 Make sure you're running with administrator/root privileges")
            self.running = False
    
    def analyze_packet(self, packet):
        """Analyze a single packet for threats"""
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Clean old entries
                self._clean_old_entries()
                
                # Check for various attack patterns
                self._check_port_scan(packet, src_ip)
                self._check_syn_flood(packet, src_ip)
                self._check_packet_rate(src_ip)
                self._check_suspicious_ports(packet, src_ip, dst_ip)
                self._check_malicious_payload(packet, src_ip, dst_ip)
                self._check_icmp_flood(packet, src_ip)
                
        except Exception as e:
            # Silently ignore packet processing errors
            pass
    
    def _check_port_scan(self, packet, src_ip):
        """Detect port scanning activity"""
        if TCP in packet:
            dst_port = packet[TCP].dport
            
            # Track ports accessed by this IP
            self.port_scan_tracker[src_ip]['ports'].add(dst_port)
            self.port_scan_tracker[src_ip]['last_seen'] = datetime.now()
            
            # Check if threshold exceeded
            if len(self.port_scan_tracker[src_ip]['ports']) >= self.PORT_SCAN_THRESHOLD:
                self._trigger_alert({
                    'threat_type': 'Port Scan',
                    'severity': 'High',
                    'source_ip': src_ip,
                    'destination_ip': packet[IP].dst,
                    'description': f'Port scan detected: {len(self.port_scan_tracker[src_ip]["ports"])} ports accessed',
                    'port': dst_port,
                    'protocol': 'TCP'
                })
                # Reset counter after alert
                self.port_scan_tracker[src_ip]['ports'].clear()
    
    def _check_syn_flood(self, packet, src_ip):
        """Detect SYN flood attacks"""
        if TCP in packet and packet[TCP].flags == 'S':  # SYN flag
            self.syn_flood_tracker[src_ip]['count'] += 1
            self.syn_flood_tracker[src_ip]['last_seen'] = datetime.now()
            
            if self.syn_flood_tracker[src_ip]['count'] >= self.SYN_FLOOD_THRESHOLD:
                self._trigger_alert({
                    'threat_type': 'DDoS Attack',
                    'severity': 'Critical',
                    'source_ip': src_ip,
                    'destination_ip': packet[IP].dst,
                    'description': f'Possible SYN flood: {self.syn_flood_tracker[src_ip]["count"]} SYN packets',
                    'port': packet[TCP].dport,
                    'protocol': 'TCP'
                })
                self.syn_flood_tracker[src_ip]['count'] = 0
    
    def _check_packet_rate(self, src_ip):
        """Detect abnormally high packet rates"""
        self.packet_rate_tracker[src_ip]['count'] += 1
        self.packet_rate_tracker[src_ip]['last_seen'] = datetime.now()
        
        if self.packet_rate_tracker[src_ip]['count'] >= self.PACKET_RATE_THRESHOLD:
            self._trigger_alert({
                'threat_type': 'DDoS Attack',
                'severity': 'Critical',
                'source_ip': src_ip,
                'destination_ip': 'Multiple',
                'description': f'High packet rate detected: {self.packet_rate_tracker[src_ip]["count"]} packets/sec',
                'port': 0,
                'protocol': 'Multiple'
            })
            self.packet_rate_tracker[src_ip]['count'] = 0
    
    def _check_suspicious_ports(self, packet, src_ip, dst_ip):
        """Detect connections to suspicious ports"""
        if TCP in packet:
            dst_port = packet[TCP].dport
            if dst_port in self.SUSPICIOUS_PORTS:
                self._trigger_alert({
                    'threat_type': 'Suspicious Connection',
                    'severity': 'Medium',
                    'source_ip': src_ip,
                    'destination_ip': dst_ip,
                    'description': f'Connection to suspicious port: {self.SUSPICIOUS_PORTS[dst_port]}',
                    'port': dst_port,
                    'protocol': 'TCP'
                })
    
    def _check_malicious_payload(self, packet, src_ip, dst_ip):
        """Check packet payload for malicious patterns"""
        if Raw in packet:
            payload = bytes(packet[Raw].load)
            
            for pattern in self.MALICIOUS_PATTERNS:
                if pattern in payload.lower():
                    threat_type = 'SQL Injection' if b'SELECT' in pattern or b'UNION' in pattern else \
                                  'XSS Attack' if b'script' in pattern or b'javascript' in pattern else \
                                  'Command Injection' if b'cmd.exe' in pattern or b'bash' in pattern else \
                                  'Malicious Payload'
                    
                    self._trigger_alert({
                        'threat_type': threat_type,
                        'severity': 'High',
                        'source_ip': src_ip,
                        'destination_ip': dst_ip,
                        'description': f'Malicious pattern detected in payload: {pattern.decode("utf-8", errors="ignore")}',
                        'port': packet[TCP].dport if TCP in packet else packet[UDP].dport if UDP in packet else 0,
                        'protocol': 'TCP' if TCP in packet else 'UDP' if UDP in packet else 'Unknown'
                    })
                    break
    
    def _check_icmp_flood(self, packet, src_ip):
        """Detect ICMP flood attacks"""
        if ICMP in packet:
            self.connection_tracker[src_ip]['count'] += 1
            self.connection_tracker[src_ip]['last_seen'] = datetime.now()
            
            if self.connection_tracker[src_ip]['count'] >= 30:
                self._trigger_alert({
                    'threat_type': 'ICMP Flood',
                    'severity': 'High',
                    'source_ip': src_ip,
                    'destination_ip': packet[IP].dst,
                    'description': f'ICMP flood detected: {self.connection_tracker[src_ip]["count"]} packets',
                    'port': 0,
                    'protocol': 'ICMP'
                })
                self.connection_tracker[src_ip]['count'] = 0
    
    def _clean_old_entries(self):
        """Remove old entries from tracking dictionaries"""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(seconds=self.TIME_WINDOW)
        
        # Clean port scan tracker
        for ip in list(self.port_scan_tracker.keys()):
            if self.port_scan_tracker[ip]['last_seen'] < cutoff_time:
                del self.port_scan_tracker[ip]
        
        # Clean SYN flood tracker
        for ip in list(self.syn_flood_tracker.keys()):
            if self.syn_flood_tracker[ip]['last_seen'] < cutoff_time:
                del self.syn_flood_tracker[ip]
        
        # Clean packet rate tracker
        for ip in list(self.packet_rate_tracker.keys()):
            if self.packet_rate_tracker[ip]['last_seen'] < cutoff_time:
                del self.packet_rate_tracker[ip]
        
        # Clean connection tracker
        for ip in list(self.connection_tracker.keys()):
            if self.connection_tracker[ip]['last_seen'] < cutoff_time:
                del self.connection_tracker[ip]
    
    def _trigger_alert(self, alert_data):
        """Trigger an alert when a threat is detected"""
        if self.alert_callback:
            alert_data['timestamp'] = datetime.now().isoformat()
            alert_data['status'] = 'Active'
            self.alert_callback(alert_data)


# Test function
if __name__ == "__main__":
    def print_alert(alert):
        print(f"\n🚨 THREAT DETECTED!")
        print(f"   Type: {alert['threat_type']}")
        print(f"   Severity: {alert['severity']}")
        print(f"   Source: {alert['source_ip']}")
        print(f"   Description: {alert['description']}")
    
    print("="*60)
    print("🔍 Real-time Packet Sniffer - TEST MODE")
    print("="*60)
    print("⚠️  This requires administrator/root privileges")
    print("📡 Starting packet capture...")
    print("Press Ctrl+C to stop\n")
    
    analyzer = PacketAnalyzer(alert_callback=print_alert)
    
    try:
        analyzer.start_sniffing()
        while analyzer.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping sniffer...")
        analyzer.stop_sniffing()
        print("✅ Done!")
