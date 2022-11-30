# Generated by Django 4.0 on 2022-02-21 01:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0021_tagging'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdb',
            name='Tags',
            field=models.ManyToManyField(blank=True, related_name='Tags', to=settings.AUTH_USER_MODEL),
        ),
    ]
