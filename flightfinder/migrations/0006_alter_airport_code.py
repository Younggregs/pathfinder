# Generated by Django 3.2.25 on 2024-07-10 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightfinder', '0005_auto_20240707_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='code',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]