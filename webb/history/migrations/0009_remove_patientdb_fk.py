# Generated by Django 4.0 on 2022-01-10 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0008_patientdb_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdb',
            name='fk',
        ),
    ]
