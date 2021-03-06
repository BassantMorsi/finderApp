# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-27 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FindRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fName', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MissRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fName', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=250, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='missrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AddField(
            model_name='findrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
        migrations.AlterUniqueTogether(
            name='missrequest',
            unique_together=set([('user', 'date')]),
        ),
        migrations.AlterUniqueTogether(
            name='findrequest',
            unique_together=set([('user', 'date')]),
        ),
    ]
