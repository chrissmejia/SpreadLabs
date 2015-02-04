# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('host', models.CharField(max_length=1000)),
                ('path', models.CharField(max_length=1000)),
                ('method', models.CharField(max_length=50)),
                ('uri', models.CharField(max_length=2000)),
                ('referer', models.CharField(max_length=2000, null=True, blank=True)),
                ('origin', models.CharField(max_length=2000, null=True, blank=True)),
                ('status_code', models.IntegerField()),
                ('user_agent', models.CharField(max_length=1000, null=True, blank=True)),
                ('remote_addr', models.IPAddressField()),
                ('remote_addr_fwd', models.IPAddressField(null=True, blank=True)),
                ('meta', models.TextField()),
                ('cookies', models.TextField(null=True, blank=True)),
                ('get', models.TextField(null=True, blank=True)),
                ('post', models.TextField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('is_secure', models.BooleanField(default=False)),
                ('is_ajax', models.BooleanField(default=False)),
                ('window_height', models.IntegerField(null=True, blank=True)),
                ('window_width', models.IntegerField(null=True, blank=True)),
                ('screen_height', models.IntegerField(null=True, blank=True)),
                ('screen_width', models.IntegerField(null=True, blank=True)),
                ('color', models.CharField(max_length=10, null=True, blank=True)),
                ('flash', models.CharField(max_length=20, null=True, blank=True)),
                ('java', models.BooleanField(default=False)),
                ('silverlight', models.CharField(max_length=20, null=True, blank=True)),
                ('html5_canvas', models.BooleanField(default=False)),
                ('html5_video', models.BooleanField(default=False)),
                ('html5_audio', models.BooleanField(default=False)),
                ('html5_storage', models.BooleanField(default=False)),
                ('svg', models.BooleanField(default=False)),
                ('webgl', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Visitas SpreadLabs',
            },
            bases=(models.Model,),
        ),
    ]
