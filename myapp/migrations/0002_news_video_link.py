# Generated by Django 5.1.1 on 2024-09-05 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='video_link',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
