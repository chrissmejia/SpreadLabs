# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('balance', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Agencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('facebook_page_id', models.CharField(max_length=100, blank=True)),
                ('agency', models.ForeignKey(to='accounts.Agency')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('membership', models.ForeignKey(to='dashboard.Membership')),
            ],
            options={
                'verbose_name_plural': 'Campa\xf1as',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('facebook_id', models.CharField(max_length=100, blank=True)),
                ('facebook_token', models.CharField(max_length=400, blank=True)),
                ('facebook_token_expiration', models.DateTimeField(null=True, blank=True)),
                ('agency', models.ForeignKey(to='accounts.Agency')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
