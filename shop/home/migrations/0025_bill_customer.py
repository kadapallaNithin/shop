# Generated by Django 3.0.4 on 2020-05-19 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Customer'),
            preserve_default=False,
        ),
    ]