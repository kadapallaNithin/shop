# Generated by Django 3.0.4 on 2020-05-20 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_bill_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='particular',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='rate',
        ),
        migrations.AddField(
            model_name='particular',
            name='bill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Bill'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Product')),
            ],
        ),
        migrations.AddField(
            model_name='particular',
            name='rate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Rate'),
            preserve_default=False,
        ),
    ]
