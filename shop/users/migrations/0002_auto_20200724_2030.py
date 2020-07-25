# Generated by Django 3.0.7 on 2020-07-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]