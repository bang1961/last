# Generated by Django 3.2.10 on 2021-12-13 00:37

import IO.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IO', '0003_alter_board_imgfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='imgfile',
            field=models.ImageField(blank=True, null=True, upload_to=IO.models.image_upload_path),
        ),
    ]