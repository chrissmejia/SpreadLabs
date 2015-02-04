# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import apps.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('stats', '0001_initial'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('picture', models.ImageField(upload_to=apps.models.upload_to_app)),
                ('like_page', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('premium', models.BooleanField(default=False)),
                ('height', models.IntegerField(default=800)),
                ('width', models.IntegerField(default=810)),
                ('pattern', models.ImageField(upload_to=apps.models.upload_pattern)),
                ('campaign', models.ForeignKey(to='accounts.Campaign')),
            ],
            options={
                'verbose_name_plural': 'Aplicaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='App_hit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('remote_addr', models.IPAddressField()),
                ('app', models.ForeignKey(to='apps.App')),
            ],
            options={
                'verbose_name_plural': 'Visitas a la aplicaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='App_record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(to='apps.App')),
                ('record', models.ForeignKey(blank=True, to='records.Record', null=True)),
            ],
            options={
                'verbose_name_plural': 'Registros desde aplicaci\xf3n',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='App_source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('app', models.ForeignKey(to='apps.App')),
            ],
            options={
                'verbose_name_plural': 'Fuentes de acceso',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Core_app',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('namespace', models.CharField(max_length=100)),
                ('order', models.IntegerField(null=True)),
                ('app', models.ForeignKey(to='apps.App')),
            ],
            options={
                'verbose_name_plural': 'Micro-aplicaciones',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Core_object_background',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=apps.models.upload_to_background)),
                ('core_app', models.ForeignKey(to='apps.Core_app')),
            ],
            options={
                'verbose_name_plural': 'Objetos de Fondo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Core_object_image_links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=apps.models.upload_to_image_link)),
                ('type', models.CharField(default=b'external', max_length=255)),
                ('top', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('link', models.CharField(max_length=255)),
                ('core_app', models.ForeignKey(related_name='core_app', to='apps.Core_app')),
                ('internal_page', models.ForeignKey(related_name='internal_page', blank=True, to='apps.Core_app', null=True)),
            ],
            options={
                'verbose_name_plural': 'Objetos de Enlace',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Core_object_input',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('top', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=300)),
                ('type', models.CharField(max_length=255)),
                ('size', models.IntegerField(default=12)),
                ('color', models.CharField(default=b'#000000', max_length=7)),
                ('default', models.CharField(default=b'', max_length=255)),
                ('default_color', models.CharField(default=b'#C0C0C0', max_length=7)),
                ('error_color', models.CharField(default=b'#DD1010', max_length=7)),
                ('transparent', models.BooleanField(default=False)),
                ('custom_name', models.CharField(max_length=100, null=True, blank=True)),
                ('core_app', models.ForeignKey(to='apps.Core_app')),
                ('restriction', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='records.Input_restriction', null=True)),
            ],
            options={
                'verbose_name_plural': 'Objetos de Formulario',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Core_object_youtube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('video', models.CharField(max_length=255)),
                ('top', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('core_app', models.ForeignKey(to='apps.Core_app')),
            ],
            options={
                'verbose_name_plural': 'Objetos de Video Youtube',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('domain', models.CharField(max_length=150, null=True, blank=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='apps.App', null=True)),
                ('campaign', models.ForeignKey(to='accounts.Campaign')),
            ],
            options={
                'verbose_name_plural': 'Dominios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facebook_access',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('namespace', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('facebook_app_id', models.CharField(max_length=100)),
                ('facebook_app_secret_key', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Accesos a Facebook',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='app_record',
            name='source',
            field=models.ForeignKey(to='apps.App_source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app_hit',
            name='core_app',
            field=models.ForeignKey(to='apps.Core_app'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app_hit',
            name='hit',
            field=models.ForeignKey(blank=True, to='stats.Hit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app_hit',
            name='source',
            field=models.ForeignKey(to='apps.App_source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='facebook_access',
            field=models.ForeignKey(blank=True, to='apps.Facebook_access', null=True),
            preserve_default=True,
        ),
    ]
