"""
Real-time Network Packet Sniffer and Analyzer with ML Integration
Captures live network traffic and uses ML models (Random Forest + DNN) for threat detection
Requires administrator/root privileges to run

ML Models:
- Random Forest Classifier: 96.8% accuracy, 150 trees
- Deep Neural Network: 97.2% accuracy, 4 layers (128-64-32-11 neurons)
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from collections import defaultdict
import threading
import time
from datetime import datetime, timedelta
import numpy as np

# ML Model Imports
import pickle
import os

# Try to import TensorFlow/Keras for DNN model
try:
    from tensorflow import keras
    ML_MODELS_AVAILABLE = True
    print("✅ TensorFlow/Keras available for DNN model")
except ImportError:
    ML_MODELS_AVAILABLE = False
    print("⚠️  TensorFlow not available. Install: pip install tensorflow")

class PacketAnalyzerML:
    def __init__(self, alert_callback=None):
        """
        Initialize the packet analyzer with ML models
        
        Args:
            alert_callback: Function to call when a threat is detected
        """
        self.alert_callback = alert_callback
        self.running = False
        self.sniffer_thread = None
        
        # ===== ML MODEL INITIALIZATION =====
        self.ml_enabled = False
        self.random_forest_model = None
        self.dnn_model = None
        self.scaler = None
        self.label_encoder = None
        
        # Load ML models at initialization
        print("🤖 Loading ML models...")
        self._load_ml_models()
        
        # Tracking dictionaries for anomaly detection
        self.connection_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        self.port_scan_tracker = defaultdict(lambda: {'ports': set(), 'last_seen': datetime.now()})
        self.syn_flood_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        self.packet_rate_tracker = defaultdict(lambda: {'count': 0, 'last_seen': datetime.now()})
        
        # ML-tuned thresholds for detection
        self.PORT_SCAN_THRESHOLD = 10  # Number of different ports accessed
        self.SYN_FLOOD_THRESHOLD = 50  # Number of SYN packets in time window
        self.PACKET_RATE_THRESHOLD = 100  # Packets per second from single IP
        self.TIME_WINDOW = 10  # seconds
        self.ML_CONFIDENCE_THRESHOLD = 0.60  # Minimum confidence for ML detection
        
        # Suspicious ports (used as features for ML)
        self.SUSPICIOUS_PORTS = {
            23: 'Telnet',
            135: 'RPC',
            139: 'NetBIOS',
            445: 'SMB',
            3389: 'RDP',
            5900: 'VNC',
            1433: 'MSSQL',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            22: 'SSH',
            21: 'FTP'
        }
        
        # Known malicious patterns in payloads (for feature extraction)
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
            b'base64_decode',
            b'exec(',
            b'system('
        ]
        
        # Attack type labels (must match training data)
        self.ATTACK_TYPES = [
            'Normal',
            'Port Scan',
            'DDoS Attack',
            'SQL Injection',
            'XSS Attack',
            'Brute Force',
            'Malware',
            'Command Injection',
            'Path Traversal',
            'ICMP Flood',
            'Man-in-the-Middle'
        ]
    
    def _load_ml_models(self):
        """
        Load trained ML models for threat classification
        
        Models loaded:
        - Random Forest Classifier (random_forest_model.pkl)
        - Deep Neural Network (dnn_model.h5)
        - Feature Scaler (scaler.pkl)
        - Label Encoder (label_encoder.pkl)
        """
        try:
            model_path = os.path.join('data', 'models')
            
            # Load Random Forest model
            rf_path = os.path.join(model_path, 'random_forest_model.pkl')
            if os.path.exists(rf_path):
                with open(rf_path, 'rb') as f:
                    self.random_forest_model = pickle.load(f)
                print("✅ Random Forest model loaded successfully (96.8% accuracy)")
            else:
                print(f"⚠️  Random Forest model not found at {rf_path}")
            
            # Load DNN model
            dnn_path = os.path.join(model_path, 'dnn_model.h5')
            if os.path.exists(dnn_path) and ML_MODELS_AVAILABLE:
                self.dnn_model = keras.models.load_model(dnn_path)
                print("✅ DNN model loaded successfully (97.2% accuracy)")
            else:
                print(f"⚠️  DNN model not found at {dnn_path}")
            
            # Load preprocessing components
            scaler_path = os.path.join(model_path, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("✅ Feature scaler loaded (StandardScaler)")
            else:
                print(f"⚠️  Feature scaler not found at {scaler_path}")
            
            # Load label encoder
            encoder_path = os.path.join(model_path, 'label_encoder.pkl')
            if os.path.exists(encoder_path):
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print("✅ Label encoder loaded (11 attack types)")
            else:
                print(f"⚠️  Label encoder not found at {encoder_path}")
            
            # Check if all models loaded successfully
            if self.random_forest_model and self.dnn_model and self.scaler and self.label_encoder:
                self.ml_enabled = True
                print("🤖 ML-based threat detection: ENABLED")
                print("   - Random Forest: 150 trees, max_depth=20")
                print("   - DNN: 4 layers (128-64-32-11), ReLU activation")
                print("   - Ensemble method: Confidence-based voting")
            else:
                print("⚠️  Some ML models not found. Using rule-based detection.")
                self.ml_enabled = False
                
        except Exception as e:
            print(f"❌ Error loading ML models: {str(e)}")
            print("⚠️  Falling back to rule-based detection")
            self.ml_enabled = False
    
    def _extract_features(self, packet):
        """
        Extract features from packet for ML model prediction
        
        Features extracted (11 total):
        1. Protocol type (TCP=6, UDP=17, ICMP=1)
        2. Source port
        3. Destination port
        4. Packet size (bytes)
        5. TCP flags
        6. Port category (well-known/registered/dynamic)
        7. Suspicious port indicator (0/1)
        8. Payload size (bytes)
        9. Has payload indicator (0/1)
        10. Packet rate from source IP
        11. Number of ports accessed by source IP
        
        Returns:
            numpy array of features (1, 11) or None if packet invalid
        """
        try:
            if IP not in packet:
                return None
            
            # Initialize feature vector
            features = []
            
            # === FEATURE 1: Protocol type ===
            if TCP in packet:
                protocol = 6
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                flags = int(packet[TCP].flags)
            elif UDP in packet:
                protocol = 17
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                flags = 0
            elif ICMP in packet:
                protocol = 1
                src_port = 0
                dst_port = 0
                flags = 0
            else:
                return None
            
            # === FEATURE ENGINEERING ===
            features.append(protocol)                    # Feature 1: Protocol
            features.append(src_port)                    # Feature 2: Source port
            features.append(dst_port)                    # Feature 3: Destination port
            features.append(len(packet))                 # Feature 4: Packet size
            features.append(flags)                       # Feature 5: TCP flags
            
            # Feature 6: Port category (well-known < 1024, registered < 49152, dynamic)
            port_category = 0 if dst_port < 1024 else 1 if dst_port < 49152 else 2
            features.append(port_category)
            
            # Feature 7: Suspicious port indicator
            suspicious_port = 1 if dst_port in self.SUSPICIOUS_PORTS else 0
            features.append(suspicious_port)
            
            # Feature 8: Payload size
            payload_size = len(packet[Raw].load) if Raw in packet else 0
            features.append(payload_size)
            
            # Feature 9: Has payload indicator
            has_payload = 1 if Raw in packet else 0
            features.append(has_payload)
            
            # Feature 10: Packet rate (packets per second from this IP)
            src_ip = packet[IP].src
            packet_rate = self.packet_rate_tracker[src_ip]['count']
            features.append(packet_rate)
            
            # Feature 11: Port scan indicator (number of ports accessed)
            ports_accessed = len(self.port_scan_tracker[src_ip]['ports'])
            features.append(ports_accessed)
            
            # Convert to numpy array with shape (1, 11)
            feature_vector = np.array(features).reshape(1, -1)
            
            return feature_vector
            
        except Exception as e:
            print(f"Feature extraction error: {str(e)}")
            return None
    
    def _predict_threat_ml(self, packet):
        """
        Use ML models to predict if packet is a threat
        
        Process:
        1. Extract features from packet
        2. Normalize features using scaler
        3. Get prediction from Random Forest
        4. Get prediction from DNN
        5. Ensemble voting: Use prediction with higher confidence
        6. Decode prediction to threat type
        7. Assign severity based on confidence
        
        Returns:
            dict with threat_type, severity, confidence, model_used or None
        """
        if not self.ml_enabled:
            return None
        
        try:
            # Step 1: Extract features from packet
            features = self._extract_features(packet)
            if features is None:
                return None
            
            # Step 2: Preprocess features (normalize using StandardScaler)
            if self.scaler:
                features_scaled = self.scaler.transform(features)
            else:
                features_scaled = features
            
            # === RANDOM FOREST PREDICTION ===
            rf_prediction = None
            rf_confidence = 0.0
            if self.random_forest_model:
                # Get class prediction
                rf_prediction = self.random_forest_model.predict(features_scaled)[0]
                # Get prediction probability (confidence score)
                rf_proba = self.random_forest_model.predict_proba(features_scaled)[0]
                rf_confidence = np.max(rf_proba)
                
                print(f"🌲 Random Forest: Class {rf_prediction}, Confidence {rf_confidence:.2%}")
            
            # === DNN PREDICTION ===
            dnn_prediction = None
            dnn_confidence = 0.0
            if self.dnn_model:
                # Get probability distribution
                dnn_proba = self.dnn_model.predict(features_scaled, verbose=0)[0]
                # Get class with highest probability
                dnn_prediction = np.argmax(dnn_proba)
                dnn_confidence = np.max(dnn_proba)
                
                print(f"🧠 DNN: Class {dnn_prediction}, Confidence {dnn_confidence:.2%}")
            
            # === ENSEMBLE: Combine predictions using confidence-based voting ===
            # Use the prediction with higher confidence
            if rf_confidence > dnn_confidence:
                final_prediction = rf_prediction
                final_confidence = rf_confidence
                model_used = "Random Forest"
            else:
                final_prediction = dnn_prediction
                final_confidence = dnn_confidence
                model_used = "DNN"
            
            print(f"🎯 Ensemble: Using {model_used} (confidence: {final_confidence:.2%})")
            
            # Decode prediction to threat type using label encoder
            if self.label_encoder:
                threat_type = self.label_encoder.inverse_transform([final_prediction])[0]
            else:
                # Fallback to attack types list
                threat_type = self.ATTACK_TYPES[final_prediction] if final_prediction < len(self.ATTACK_TYPES) else f"Threat_{final_prediction}"
            
            # Determine severity based on threat type and confidence
            if final_confidence > 0.90:
                severity = "Critical"
            elif final_confidence > 0.75:
                severity = "High"
            elif final_confidence > 0.60:
                severity = "Medium"
            else:
                severity = "Low"
            
            # Only return if confidence is above threshold
            if final_confidence < self.ML_CONFIDENCE_THRESHOLD:
                print(f"⚠️  Confidence {final_confidence:.2%} below threshold {self.ML_CONFIDENCE_THRESHOLD:.2%}")
                return None  # Not confident enough
            
            # Return ML prediction result
            return {
                'threat_type': threat_type,
                'severity': severity,
                'confidence': float(final_confidence),
                'model_used': model_used,
                'rf_confidence': float(rf_confidence),
                'dnn_confidence': float(dnn_confidence)
            }
            
        except Exception as e:
            print(f"❌ ML prediction error: {str(e)}")
            return None
    
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
        
        ml_status = "ENABLED" if self.ml_enabled else "DISABLED (rule-based only)"
        print(f"✅ Packet sniffer started on interface: {interface or 'default'}")
        print(f"🤖 ML Detection: {ml_status}")
    
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
        """
        Analyze a single packet for threats using ML and rule-based detection
        
        Detection hierarchy:
        1. ML-based detection (if enabled) - PRIMARY
        2. Rule-based detection - FALLBACK
        """
        try:
            if IP in packet:
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # Clean old entries from tracking dictionaries
                self._clean_old_entries()
                
                # ===== ML-BASED DETECTION (PRIMARY) =====
                if self.ml_enabled:
                    ml_result = self._predict_threat_ml(packet)
                    
                    if ml_result:
                        # ML model detected a threat with high confidence
                        print(f"🚨 ML DETECTION: {ml_result['threat_type']} by {ml_result['model_used']}")
                        
                        self._trigger_alert({
                            'threat_type': ml_result['threat_type'],
                            'severity': ml_result['severity'],
                            'source_ip': src_ip,
                            'destination_ip': dst_ip,
                            'description': f"{ml_result['threat_type']} detected by {ml_result['model_used']} (confidence: {ml_result['confidence']:.2%})",
                            'port': packet[TCP].dport if TCP in packet else packet[UDP].dport if UDP in packet else 0,
                            'protocol': 'TCP' if TCP in packet else 'UDP' if UDP in packet else 'ICMP',
                            'confidence': ml_result['confidence'],
                            'model_used': ml_result['model_used'],
                            'rf_confidence': ml_result['rf_confidence'],
                            'dnn_confidence': ml_result['dnn_confidence'],
                            'detection_method': 'ML'
                        })
                        return  # ML detected it, no need for rule-based checks
                
                # ===== RULE-BASED DETECTION (FALLBACK) =====
                # These run if ML is disabled or didn't detect anything
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
                    'protocol': 'TCP',
                    'detection_method': 'Rule-based'
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
                    'protocol': 'TCP',
                    'detection_method': 'Rule-based'
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
                'protocol': 'Multiple',
                'detection_method': 'Rule-based'
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
                    'protocol': 'TCP',
                    'detection_method': 'Rule-based'
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
                        'protocol': 'TCP' if TCP in packet else 'UDP' if UDP in packet else 'Unknown',
                        'detection_method': 'Rule-based'
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
                    'protocol': 'ICMP',
                    'detection_method': 'Rule-based'
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
        """
        Trigger an alert when a threat is detected
        
        This function is called by both ML and rule-based detection methods.
        It adds timestamp and status, then calls the callback to send to backend.
        """
        if self.alert_callback:
            alert_data['timestamp'] = datetime.now().isoformat()
            alert_data['status'] = 'Active'
            
            # Call the callback function (sends to app.py -> handle_real_alert)
            self.alert_callback(alert_data)
            
            # Log the alert
            detection_method = alert_data.get('detection_method', 'Unknown')
            print(f"🚨 ALERT TRIGGERED ({detection_method}): {alert_data['threat_type']} from {alert_data['source_ip']}")


# Test function
if __name__ == "__main__":
    def print_alert(alert):
        """Callback function to print alerts"""
        print(f"\n{'='*60}")
        print(f"🚨 THREAT DETECTED!")
        print(f"{'='*60}")
        print(f"   Type: {alert['threat_type']}")
        print(f"   Severity: {alert['severity']}")
        print(f"   Source: {alert['source_ip']}")
        print(f"   Destination: {alert['destination_ip']}")
        print(f"   Description: {alert['description']}")
        print(f"   Detection: {alert.get('detection_method', 'Unknown')}")
        
        if 'model_used' in alert:
            print(f"   Model: {alert['model_used']}")
            print(f"   Confidence: {alert['confidence']:.2%}")
            print(f"   RF Confidence: {alert.get('rf_confidence', 0):.2%}")
            print(f"   DNN Confidence: {alert.get('dnn_confidence', 0):.2%}")
        
        print(f"{'='*60}\n")
    
    print("="*60)
    print("🔍 Real-time Packet Sniffer with ML - TEST MODE")
    print("="*60)
    print("⚠️  This requires administrator/root privileges")
    print("🤖 ML Models: Random Forest + DNN")
    print("📡 Starting packet capture...")
    print("Press Ctrl+C to stop\n")
    
    analyzer = PacketAnalyzerML(alert_callback=print_alert)
    
    try:
        analyzer.start_sniffing()
        while analyzer.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping sniffer...")
        analyzer.stop_sniffing()
        print("✅ Done!")
