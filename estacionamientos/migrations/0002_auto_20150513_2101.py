# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propietario',
            name='apellidos',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='cedula',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='nombres',
            field=models.CharField(max_length=30),
        ),
    ]
