"""
Email Service for IDS Alert System
Supports Gmail SMTP, Generic SMTP, and SendGrid
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email_config import *

class EmailService:
    def __init__(self):
        self.enabled = EMAIL_ENABLED
        self.service = EMAIL_SERVICE
        
    def send_alert_email(self, alert_data):
        """Send email alert based on configured service"""
        if not self.enabled:
            print("📧 Email alerts are disabled in configuration")
            return {'status': 'disabled', 'message': 'Email alerts are disabled'}
        
        try:
            if self.service == 'gmail':
                return self._send_gmail(alert_data)
            elif self.service == 'smtp':
                return self._send_smtp(alert_data)
            elif self.service == 'sendgrid':
                return self._send_sendgrid(alert_data)
            else:
                return {'status': 'error', 'message': f'Unknown email service: {self.service}'}
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _send_gmail(self, alert_data):
        """Send email using Gmail SMTP"""
        if not GMAIL_APP_PASSWORD:
            return {'status': 'error', 'message': 'Gmail App Password not configured'}
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} {alert_data.get('severity', 'Unknown')} Threat Detected"
        msg['From'] = GMAIL_SENDER
        msg['To'] = GMAIL_RECIPIENT
        
        # Create HTML email body
        html_body = self._create_html_email(alert_data)
        text_body = self._create_text_email(alert_data)
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {GMAIL_RECIPIENT}")
        return {'status': 'success', 'message': f'Email sent to {GMAIL_RECIPIENT}'}
    
    def _send_smtp(self, alert_data):
        """Send email using generic SMTP"""
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            return {'status': 'error', 'message': 'SMTP credentials not configured'}
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} {alert_data.get('severity', 'Unknown')} Threat Detected"
        msg['From'] = SMTP_USERNAME
        msg['To'] = GMAIL_RECIPIENT
        
        # Create email body
        html_body = self._create_html_email(alert_data)
        text_body = self._create_text_email(alert_data)
        
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        if SMTP_USE_TLS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
        
        print(f"✅ Email sent successfully via SMTP")
        return {'status': 'success', 'message': 'Email sent via SMTP'}
    
    def _send_sendgrid(self, alert_data):
        """Send email using SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
        except ImportError:
            return {'status': 'error', 'message': 'SendGrid library not installed. Run: pip install sendgrid'}
        
        if not SENDGRID_API_KEY:
            return {'status': 'error', 'message': 'SendGrid API key not configured'}
        
        # Create message
        message = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=SENDGRID_TO_EMAIL,
            subject=f"{EMAIL_SUBJECT_PREFIX} {alert_data.get('severity', 'Unknown')} Threat Detected",
            html_content=self._create_html_email(alert_data)
        )
        
        # Send email
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"✅ Email sent via SendGrid (status: {response.status_code})")
        return {'status': 'success', 'message': 'Email sent via SendGrid'}
    
    def _create_text_email(self, alert_data):
        """Create plain text email body"""
        return f"""
INTRUSION DETECTION SYSTEM ALERT

Threat Detected: {alert_data.get('threat_type', 'Unknown')}
Severity: {alert_data.get('severity', 'Unknown')}
Status: {alert_data.get('status', 'Unknown')}

Source IP: {alert_data.get('source_ip', 'Unknown')}
Destination IP: {alert_data.get('destination_ip', 'Unknown')}
Port: {alert_data.get('port', 'Unknown')}
Protocol: {alert_data.get('protocol', 'Unknown')}

Description:
{alert_data.get('description', 'No description available')}

Timestamp: {alert_data.get('timestamp', datetime.now().isoformat())}

---
This is an automated alert from your Intrusion Detection System.
Please review and take appropriate action.
"""
    
    def _create_html_email(self, alert_data):
        """Create HTML email body"""
        severity = alert_data.get('severity', 'Unknown')
        severity_colors = {
            'Critical': '#ef4444',
            'High': '#f59e0b',
            'Medium': '#3b82f6',
            'Low': '#10b981'
        }
        color = severity_colors.get(severity, '#6b7280')
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
        .content {{ background-color: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }}
        .alert-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid {color}; }}
        .label {{ font-weight: bold; color: #4b5563; }}
        .value {{ color: #1f2937; }}
        .footer {{ background-color: #f3f4f6; padding: 15px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 5px 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Security Alert</h1>
            <h2>{severity} Threat Detected</h2>
        </div>
        
        <div class="content">
            <div class="alert-box">
                <p><span class="label">Threat Type:</span> <span class="value">{alert_data.get('threat_type', 'Unknown')}</span></p>
                <p><span class="label">Severity:</span> <span class="value" style="color: {color}; font-weight: bold;">{severity}</span></p>
                <p><span class="label">Status:</span> <span class="value">{alert_data.get('status', 'Unknown')}</span></p>
            </div>
            
            <div class="alert-box">
                <h3>Network Details</h3>
                <p><span class="label">Source IP:</span> <span class="value">{alert_data.get('source_ip', 'Unknown')}</span></p>
                <p><span class="label">Destination IP:</span> <span class="value">{alert_data.get('destination_ip', 'Unknown')}</span></p>
                <p><span class="label">Port:</span> <span class="value">{alert_data.get('port', 'Unknown')}</span></p>
                <p><span class="label">Protocol:</span> <span class="value">{alert_data.get('protocol', 'Unknown')}</span></p>
            </div>
            
            <div class="alert-box">
                <h3>Description</h3>
                <p>{alert_data.get('description', 'No description available')}</p>
            </div>
            
            <div class="alert-box">
                <p><span class="label">Timestamp:</span> <span class="value">{alert_data.get('timestamp', datetime.now().isoformat())}</span></p>
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated alert from your Intrusion Detection System.</p>
            <p>Please review and take appropriate action.</p>
        </div>
    </div>
</body>
</html>
"""

# Create singleton instance
email_service = EmailService()
