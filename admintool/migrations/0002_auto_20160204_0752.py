# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admintool', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='players',
            options={'managed': False, 'permissions': (('change_exp', 'Can change player experience'),)},
        ),
    ]
