# Generated by Django 4.0 on 2022-04-22 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0049_tagging3_tagging2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientdb',
            name='Tags4',
        ),
        migrations.RemoveField(
            model_name='patientdb',
            name='Tags_default4',
        ),
    ]