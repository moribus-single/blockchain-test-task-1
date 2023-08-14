from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True)
def send_otp_email(self, email, otp_code):
    send_mail(
        'OTP code',                 # subject
        f'Your OTP is: {otp_code}', # message 
        settings.EMAIL_HOST_USER,   # from_email
        [email]              # recipients_list
    )
