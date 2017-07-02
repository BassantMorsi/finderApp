# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-01 12:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='findrequest',
            name='stop',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
        migrations.AddField(
            model_name='missrequest',
            name='stop',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
