# Generated by Django 3.0.7 on 2020-06-09 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_payment_intrest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='intrest',
            new_name='intrest_rate',
        ),
    ]
