# Generated by Django 4.2.4 on 2023-08-13 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0004_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_set',
            field=models.DateTimeField(blank=True, null=True, verbose_name='time OTP is set'),
        ),
    ]
