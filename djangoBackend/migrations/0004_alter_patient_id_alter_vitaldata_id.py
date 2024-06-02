# Generated by Django 5.0.4 on 2024-06-02 16:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoBackend', '0003_alter_patient_id_alter_vitaldata_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vitaldata',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]