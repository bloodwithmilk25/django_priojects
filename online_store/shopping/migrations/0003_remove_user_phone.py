# Generated by Django 2.1 on 2018-09-02 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0002_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
    ]
