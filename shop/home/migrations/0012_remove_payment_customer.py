# Generated by Django 3.0.4 on 2020-04-07 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200407_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='customer',
        ),
    ]
