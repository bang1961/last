# Generated by Django 4.0 on 2022-04-05 03:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('history', '0044_alter_patientdb_tags_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdb',
            name='Tags1',
            field=models.ManyToManyField(blank=True, related_name='Tags1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags2',
            field=models.ManyToManyField(blank=True, related_name='Tags2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags3',
            field=models.ManyToManyField(blank=True, related_name='Tags3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags4',
            field=models.ManyToManyField(blank=True, related_name='Tags4', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags_default1',
            field=models.ManyToManyField(blank=True, related_name='Tags_default1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags_default2',
            field=models.ManyToManyField(blank=True, related_name='Tags_default2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags_default3',
            field=models.ManyToManyField(blank=True, related_name='Tags_default3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientdb',
            name='Tags_default4',
            field=models.ManyToManyField(blank=True, related_name='Tags_default4', to=settings.AUTH_USER_MODEL),
        ),
    ]
