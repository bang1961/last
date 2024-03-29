# Generated by Django 4.0 on 2022-02-23 05:55

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0026_alter_patientdb_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='ment',
            name='interpretation',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ment',
            name='body',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
