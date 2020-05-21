# Generated by Django 3.0.4 on 2020-04-07 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denom2000', models.IntegerField()),
                ('denom500', models.IntegerField()),
                ('denom200', models.IntegerField()),
                ('denom100', models.IntegerField()),
                ('denom50', models.IntegerField()),
                ('denom20', models.IntegerField()),
                ('denom10', models.IntegerField()),
                ('denom5', models.IntegerField()),
                ('denom2', models.IntegerField()),
                ('denom1', models.IntegerField()),
            ],
        ),
    ]