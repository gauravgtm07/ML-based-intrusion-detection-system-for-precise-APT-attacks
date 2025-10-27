"""
Attack Simulator for IDS Testing
Simulates various network attacks to test the Intrusion Detection System
This is a HARMLESS testing tool - no actual attacks are performed
"""

import requests
import time
import random
from datetime import datetime

# Backend API endpoint
API_BASE = "http://localhost:5000/api"

# Attack simulation types
ATTACK_TYPES = {
    '1': {
        'name': 'Port Scan Attack',
        'description': 'Simulates port scanning activity',
        'severity': 'Medium',
        'count': 5
    },
    '2': {
        'name': 'DDoS Attack',
        'description': 'Simulates distributed denial of service',
        'severity': 'Critical',
        'count': 10
    },
    '3': {
        'name': 'SQL Injection',
        'description': 'Simulates SQL injection attempts',
        'severity': 'High',
        'count': 3
    },
    '4': {
        'name': 'Brute Force',
        'description': 'Simulates password brute force attack',
        'severity': 'High',
        'count': 8
    },
    '5': {
        'name': 'XSS Attack',
        'description': 'Simulates cross-site scripting attempts',
        'severity': 'Medium',
        'count': 4
    },
    '6': {
        'name': 'Man-in-the-Middle',
        'description': 'Simulates MITM attack',
        'severity': 'Critical',
        'count': 2
    },
    '7': {
        'name': 'Malware Detection',
        'description': 'Simulates malware traffic',
        'severity': 'Critical',
        'count': 3
    },
    '8': {
        'name': 'Phishing Attempt',
        'description': 'Simulates phishing activity',
        'severity': 'Medium',
        'count': 2
    }
}

def print_banner():
    """Display banner"""
    print("\n" + "="*60)
    print("🎯  IDS ATTACK SIMULATOR - TESTING TOOL")
    print("="*60)
    print("⚠️  This is a HARMLESS testing tool")
    print("✅  Simulates attacks for demonstration purposes only")
    print("="*60 + "\n")

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Backend server is running\n")
            return True
    except requests.exceptions.RequestException:
        print("❌ Backend server is not running!")
        print("   Please start the backend first: python backend/app.py\n")
        return False

def simulate_attack(attack_type, intensity='normal'):
    """Simulate a specific attack type"""
    attack = ATTACK_TYPES[attack_type]
    count = attack['count']
    
    if intensity == 'heavy':
        count *= 3
    elif intensity == 'light':
        count = max(1, count // 2)
    
    print(f"\n🔴 Launching: {attack['name']}")
    print(f"   Description: {attack['description']}")
    print(f"   Severity: {attack['severity']}")
    print(f"   Packets: {count}")
    print(f"   Intensity: {intensity.upper()}\n")
    
    for i in range(count):
        # Trigger actual alert on the backend
        try:
            payload = {
                'threat_type': attack['name'],
                'severity': attack['severity'],
                'description': attack['description']
            }
            response = requests.post(f"{API_BASE}/trigger-alert", json=payload, timeout=2)
            
            if response.status_code == 200:
                print(f"   [{i+1}/{count}] 🚨 Alert triggered... ", end='')
                time.sleep(random.uniform(0.3, 0.8))
                print("✓")
            else:
                print(f"   [{i+1}/{count}] ✗ Failed")
        except Exception as e:
            print(f"   [{i+1}/{count}] ✗ Error: {str(e)}")
    
    print(f"\n✅ {attack['name']} simulation complete!")
    print(f"   Check your dashboard for detected threats\n")

def continuous_attack():
    """Simulate continuous mixed attacks"""
    print("\n🔥 CONTINUOUS ATTACK MODE")
    print("   Simulating random attacks every 2-5 seconds")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            attack_type = random.choice(list(ATTACK_TYPES.keys()))
            attack = ATTACK_TYPES[attack_type]
            
            print(f"⚡ {datetime.now().strftime('%H:%M:%S')} - {attack['name']} ({attack['severity']})")
            
            try:
                payload = {
                    'threat_type': attack['name'],
                    'severity': attack['severity'],
                    'description': attack['description']
                }
                requests.post(f"{API_BASE}/trigger-alert", json=payload, timeout=1)
            except:
                pass
            
            time.sleep(random.uniform(2, 5))
    except KeyboardInterrupt:
        print("\n\n✅ Continuous attack mode stopped\n")

def stress_test():
    """Stress test with multiple simultaneous attacks"""
    print("\n💥 STRESS TEST MODE")
    print("   Launching multiple attack types simultaneously")
    print("   This will flood your dashboard with alerts\n")
    
    input("   Press ENTER to start stress test...")
    
    for attack_type in ATTACK_TYPES.keys():
        attack = ATTACK_TYPES[attack_type]
        print(f"   🚀 Launching {attack['name']}...")
        
        for _ in range(attack['count']):
            try:
                payload = {
                    'threat_type': attack['name'],
                    'severity': attack['severity'],
                    'description': attack['description']
                }
                requests.post(f"{API_BASE}/trigger-alert", json=payload, timeout=0.5)
            except:
                pass
            time.sleep(0.1)
    
    print("\n✅ Stress test complete! Check your dashboard\n")

def show_menu():
    """Display main menu"""
    print("\n" + "─"*60)
    print("SELECT ATTACK TYPE:")
    print("─"*60)
    
    for key, attack in ATTACK_TYPES.items():
        print(f"  {key}. {attack['name']:<25} [{attack['severity']}]")
    
    print("\n  9. Continuous Attack Mode (Random)")
    print("  0. Stress Test (All Attacks)")
    print("  q. Quit")
    print("─"*60)

def main():
    """Main function"""
    print_banner()
    
    if not check_backend():
        return
    
    print("📊 Open your dashboard at: http://localhost:5173")
    print("   Watch the alerts appear in real-time!\n")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Exiting attack simulator. Stay safe!\n")
            break
        elif choice == '9':
            continuous_attack()
        elif choice == '0':
            stress_test()
        elif choice in ATTACK_TYPES:
            print("\nSelect intensity:")
            print("  1. Light")
            print("  2. Normal")
            print("  3. Heavy")
            intensity_choice = input("\nEnter intensity (default: 2): ").strip() or '2'
            
            intensity_map = {'1': 'light', '2': 'normal', '3': 'heavy'}
            intensity = intensity_map.get(intensity_choice, 'normal')
            
            simulate_attack(choice, intensity)
        else:
            print("\n❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Attack simulator stopped. Goodbye!\n")
