# Generated by Django 3.0.4 on 2020-05-19 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_bill_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='customer',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='home.Customer'),
            preserve_default=False,
        ),
    ]
