# Generated by Django 4.0 on 2022-03-03 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0036_alter_ment_body_alter_ment_interpretation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pallet', to='history.patientdb'),
        ),
    ]
