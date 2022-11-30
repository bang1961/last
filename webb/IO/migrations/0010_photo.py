# Generated by Django 4.0 on 2022-03-23 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IO', '0009_remove_board_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IO.board')),
            ],
        ),
    ]
