# Generated by Django 3.0.4 on 2020-05-26 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_remove_rate_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Product'),
            preserve_default=False,
        ),
    ]
