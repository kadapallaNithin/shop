# Generated by Django 3.0.7 on 2020-06-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_payment_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='intrest',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]