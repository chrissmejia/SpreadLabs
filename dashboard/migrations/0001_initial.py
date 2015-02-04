# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('max_apps', models.IntegerField(default=0)),
                ('white_mark', models.BooleanField(default=False)),
                ('like_page', models.BooleanField(default=False)),
                ('own_domain', models.BooleanField(default=False)),
                ('button_tool', models.BooleanField(default=False)),
                ('youtube_tool', models.BooleanField(default=False)),
                ('form_tool', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Membres\xedas',
            },
            bases=(models.Model,),
        ),
    ]
