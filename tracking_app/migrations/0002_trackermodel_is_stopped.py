# Generated by Django 5.0.2 on 2024-02-10 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackermodel',
            name='is_stopped',
            field=models.BooleanField(default=True),
        ),
    ]