# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Input_restriction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(default=b'text', max_length=100)),
                ('min_characters', models.IntegerField(default=1)),
                ('max_characters', models.IntegerField(default=1)),
                ('required', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Restricciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('lastname', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.CharField(max_length=100, null=True, blank=True)),
                ('identification', models.CharField(max_length=100, null=True, blank=True)),
                ('cellphone', models.IntegerField(null=True, blank=True)),
                ('year_of_birth', models.IntegerField(null=True, blank=True)),
                ('birth_month', models.IntegerField(null=True, blank=True)),
                ('day_of_birth', models.IntegerField(null=True, blank=True)),
                ('campaign', models.ForeignKey(to='accounts.Campaign')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
