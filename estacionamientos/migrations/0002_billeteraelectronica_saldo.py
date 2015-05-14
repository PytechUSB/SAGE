# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billeteraelectronica',
            name='saldo',
            field=models.DecimalField(default=0.0, decimal_places=2, max_digits=20),
            preserve_default=False,
        ),
    ]
