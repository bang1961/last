# Generated by Django 4.0 on 2022-01-10 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IO', '0006_alter_board_id'),
        ('history', '0009_remove_patientdb_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientdb',
            name='fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='IO.board'),
        ),
    ]
