# Generated by Django 3.0.4 on 2020-04-07 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_rate',
            new_name='rate',
        ),
    ]