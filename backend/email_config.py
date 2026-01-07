"""
Email Configuration for IDS Alert System
Configure your email settings here
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'gmail')  # 'gmail', 'sendgrid', 'smtp'

# Gmail SMTP Configuration
GMAIL_SENDER = os.getenv('GMAIL_SENDER', 'your-email@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')  # Use App Password, not regular password
GMAIL_RECIPIENT = os.getenv('GMAIL_RECIPIENT', 'recipient@example.com')

# Generic SMTP Configuration
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'

# SendGrid Configuration
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'alerts@yourdomain.com')
SENDGRID_TO_EMAIL = os.getenv('SENDGRID_TO_EMAIL', 'admin@yourdomain.com')

# Email Template Settings
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[IDS Alert]')
