# Generated by Django 2.1.15 on 2020-09-29 21:22

import create_voice.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_voice', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='voice_record',
            field=models.FileField(upload_to=create_voice.models.user_directory_path),
        ),
    ]