# Generated by Django 5.0.2 on 2024-02-10 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0002_trackermodel_is_stopped'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackermodel',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]