# Generated by Django 5.0.4 on 2024-06-02 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoBackend', '0004_alter_patient_id_alter_vitaldata_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitaldata',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoBackend.patient'),
        ),
    ]
