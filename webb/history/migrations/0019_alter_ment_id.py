# Generated by Django 4.0 on 2022-02-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0018_ment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]