# Generated by Django 3.2.25 on 2024-07-14 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightfinder', '0008_alter_flight_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['departure_time']},
        ),
    ]