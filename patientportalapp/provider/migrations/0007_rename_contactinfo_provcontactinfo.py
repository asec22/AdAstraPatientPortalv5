# Generated by Django 5.0.6 on 2024-07-06 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_providerinfo_dea_number'),
        ('provider', '0006_medprescription_add_instructions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactInfo',
            new_name='ProvContactInfo',
        ),
    ]
