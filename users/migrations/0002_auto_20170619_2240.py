# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 22:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='findrequest',
            unique_together=set([('user', 'date')]),
        ),
    ]
