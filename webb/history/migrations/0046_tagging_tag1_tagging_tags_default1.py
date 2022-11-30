# Generated by Django 4.0 on 2022-04-05 07:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0045_patientdb_tags1_patientdb_tags2_patientdb_tags3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagging',
            name='Tag1',
            field=models.ManyToManyField(blank=True, related_name='likes1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tagging',
            name='Tags_default1',
            field=models.ManyToManyField(blank=True, related_name='dislike1', to=settings.AUTH_USER_MODEL),
        ),
    ]