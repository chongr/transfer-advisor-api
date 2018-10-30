# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-26 04:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubwayLine',
            fields=[
                ('name', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('stations', models.ManyToManyField(to='station.Station')),
            ],
        ),
    ]
