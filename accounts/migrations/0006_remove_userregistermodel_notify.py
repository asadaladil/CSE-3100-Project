# Generated by Django 5.1.7 on 2025-03-23 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_userregistermodel_notify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistermodel',
            name='notify',
        ),
    ]
