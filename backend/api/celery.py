import os
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def send_otp_email(email, otp_code):
    send_mail(
        'OTP code',                 # subject
        f'Your OTP is: {otp_code}', # message 
        settings.EMAIL_HOST_USER,   # from_email
        [email]              # recipients_list
    )