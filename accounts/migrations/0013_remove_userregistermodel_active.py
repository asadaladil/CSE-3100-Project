# Generated by Django 5.1.7 on 2025-03-29 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_userregistermodel_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistermodel',
            name='active',
        ),
    ]
