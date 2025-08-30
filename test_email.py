import os
import django
from django.conf import settings
from django.core.mail import send_mail

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

# Test email
try:
    send_mail(
        'Test Email',
        'This is a test email.',
        settings.EMAIL_HOST_USER,
        ['nirnayakhadka98@gmail.com'],
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
