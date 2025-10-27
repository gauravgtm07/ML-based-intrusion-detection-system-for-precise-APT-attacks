"""
Start Real-time Network Monitoring
This script enables live packet capture and threat detection
REQUIRES: Administrator/Root privileges
"""

import requests
import time
import sys

API_BASE = "http://localhost:5000/api"

def check_admin():
    """Check if running with admin privileges"""
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        return is_admin
    except:
        # For non-Windows systems
        import os
        return os.geteuid() == 0

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def check_realtime_status():
    """Check real-time capture status"""
    try:
        response = requests.get(f"{API_BASE}/realtime/status", timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def start_realtime():
    """Start real-time packet capture"""
    try:
        response = requests.post(f"{API_BASE}/realtime/start", json={}, timeout=5)
        return response.json()
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def stop_realtime():
    """Stop real-time packet capture"""
    try:
        response = requests.post(f"{API_BASE}/realtime/stop", json={}, timeout=5)
        return response.json()
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def main():
    print("\n" + "="*70)
    print("🔍 REAL-TIME NETWORK MONITORING")
    print("="*70)
    
    # Check admin privileges
    if not check_admin():
        print("\n❌ ERROR: Administrator/Root privileges required!")
        print("   Please run this script as administrator:")
        print("   - Windows: Right-click → Run as administrator")
        print("   - Linux/Mac: sudo python start_realtime_monitoring.py")
        sys.exit(1)
    
    print("✅ Running with administrator privileges")
    
    # Check backend
    print("\n🔍 Checking backend server...")
    if not check_backend():
        print("❌ Backend server is not running!")
        print("   Please start the backend first:")
        print("   cd backend && python app.py")
        sys.exit(1)
    
    print("✅ Backend server is running")
    
    # Check real-time status
    print("\n🔍 Checking real-time capture capability...")
    status = check_realtime_status()
    
    if not status:
        print("❌ Could not get status from backend")
        sys.exit(1)
    
    if not status.get('available'):
        print("❌ Real-time packet capture is not available!")
        print("   Install Scapy: pip install scapy")
        sys.exit(1)
    
    print("✅ Real-time packet capture is available")
    
    if status.get('running'):
        print("\n⚠️  Real-time capture is already running")
        choice = input("\nDo you want to stop it? (y/n): ").strip().lower()
        if choice == 'y':
            print("\n🛑 Stopping real-time capture...")
            result = stop_realtime()
            print(f"   {result.get('message', 'Stopped')}")
        sys.exit(0)
    
    # Start real-time capture
    print("\n" + "="*70)
    print("🚀 STARTING REAL-TIME PACKET CAPTURE")
    print("="*70)
    print("\n⚠️  This will capture and analyze ALL network traffic on your laptop")
    print("   The system will detect:")
    print("   • Port scans")
    print("   • DDoS attacks")
    print("   • SQL injection attempts")
    print("   • XSS attacks")
    print("   • Suspicious connections")
    print("   • Malicious payloads")
    print("   • And more...")
    print("\n📊 Open dashboard at: http://localhost:5173")
    print("   Watch real threats appear in real-time!")
    
    input("\n👉 Press ENTER to start monitoring (Ctrl+C to stop)...")
    
    print("\n🔄 Starting packet capture...")
    result = start_realtime()
    
    if result.get('status') == 'success':
        print(f"✅ {result.get('message')}")
        print(f"   Interface: {result.get('interface', 'default')}")
        print("\n🎯 MONITORING ACTIVE - Analyzing live network traffic...")
        print("   Press Ctrl+C to stop\n")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping real-time capture...")
            result = stop_realtime()
            print(f"✅ {result.get('message', 'Stopped')}")
            print("\n👋 Real-time monitoring stopped. Goodbye!\n")
    else:
        print(f"❌ Failed to start: {result.get('message')}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
        sys.exit(0)
