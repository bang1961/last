# Generated by Django 4.0 on 2022-03-07 02:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0043_tagging_tags_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdb',
            name='Tags_default',
            field=models.ManyToManyField(blank=True, related_name='Tags_default', to=settings.AUTH_USER_MODEL),
        ),
    ]