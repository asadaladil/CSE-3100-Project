# Generated by Django 5.1.7 on 2025-03-29 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_userregistermodel_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistermodel',
            name='OTP',
            field=models.IntegerField(default=0),
        ),
    ]
