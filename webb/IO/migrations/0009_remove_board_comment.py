# Generated by Django 4.0 on 2022-02-25 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IO', '0008_delete_mymodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='comment',
        ),
    ]
