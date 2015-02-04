# -*- encoding: utf-8 -*-
"""
    SpreadLabs - Social media suite
    Copyright (C) 2015  Christopher Mejia Montoya - me@chrissmejia.com - chrissmejia.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os, random, string
from django.db import models
from accounts.models import Campaign
from stats.models import Hit
from records.models import Record, Input_restriction

# Create your models here.

class Facebook_access(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    namespace = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    facebook_app_id  = models.CharField(max_length=100)
    facebook_app_secret_key  = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Accesos a Facebook"
    
    def __unicode__(self):
        return self.name

def upload_to_app(instance, filename):
    token = '%s%s' % (
        string.join(random.sample(string.ascii_letters + string.digits, 30), ''),
        os.path.splitext(filename)[-1],
    )
    return 'icos/' + token

def upload_pattern(instance, filename):
    token = '%s%s' % (
        string.join(random.sample(string.ascii_letters + string.digits, 30), ''),
        os.path.splitext(filename)[-1],
    )
    return 'pattern/' + token

class App(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign)
    facebook_access = models.ForeignKey(Facebook_access, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=upload_to_app)
    like_page = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    premium = models.BooleanField(default=False)
    height = models.IntegerField(default=800)
    width = models.IntegerField(default=810)
    pattern = models.ImageField(upload_to=upload_pattern)
    
    class Meta:
        verbose_name_plural = "Aplicaciones"
    
    def __unicode__(self):
        return str(self.id) + ' - ' + self.campaign.name + ' - ' + self.name

#    def save(self, *args, **kwargs):
#        self.picture_slug = self.picture.name
#        super(App, self).save(*args, **kwargs)
    
class Core_app(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    namespace = models.CharField(max_length=100)
#    development = models.IntegerField(default=0)  # 0 alpha | 1 beta | 2 rc | 3 live
#    membership = models.IntegerField(default=0)
    order = models.IntegerField(null=True)
    
    class Meta:
        verbose_name_plural = "Micro-aplicaciones"
    
    def __unicode__(self):
        return self.name

def upload_to_background(instance, filename):
    token = '%s%s' % (
        string.join(random.sample(string.ascii_letters + string.digits, 30), ''),
        os.path.splitext(filename)[-1],
    )
    return 'backgrounds/' + token
#        if os.path.exists(settings.MEDIA_ROOT+self.image.name):
#            os.remove(settings.MEDIA_ROOT+self.image.name)

class Core_object_background(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    core_app = models.ForeignKey(Core_app)
    image = models.ImageField(upload_to=upload_to_background)
#    slug = models.SlugField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Objetos de Fondo"
    
    def __unicode__(self):
        return self.image.name

#    def save(self, *args, **kwargs):
#        self.slug = self.image.name
#        super(Core_object_background, self).save(*args, **kwargs)

def upload_to_image_link(instance, filename):
    token = '%s%s' % (
        string.join(random.sample(string.ascii_letters + string.digits, 30), ''),
        os.path.splitext(filename)[-1],
    )
    return 'image_links/' + token

class Core_object_image_links(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    core_app = models.ForeignKey(Core_app, related_name='core_app')
    image = models.ImageField(upload_to=upload_to_image_link)
    type = models.CharField(max_length=255, default="external")
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    link = models.CharField(max_length=255)
    internal_page = models.ForeignKey(Core_app, blank=True, null=True, related_name='internal_page')
    
    class Meta:
        verbose_name_plural = "Objetos de Enlace"
    
    def __unicode__(self):
        return self.link

#    def save(self, *args, **kwargs):
#        self.slug = self.image.name
#        super(Core_object_image_links, self).save(*args, **kwargs)

class Core_object_youtube(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    core_app = models.ForeignKey(Core_app)
    video = models.CharField(max_length=255)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Objetos de Video Youtube"
    
    def __unicode__(self):
        return self.core_app.name + " - " + self.video

class Core_object_input(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    core_app = models.ForeignKey(Core_app)
    name = models.CharField(max_length=100, blank=True, null=True)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    width = models.IntegerField(default=300)
    type = models.CharField(max_length=255)
    size = models.IntegerField(default=12)
    color = models.CharField(max_length=7,default='#000000')
    default = models.CharField(max_length=255, default='')
    default_color = models.CharField(max_length=7,default='#C0C0C0')
    error_color = models.CharField(max_length=7,default='#DD1010')
    transparent = models.BooleanField(default=False)
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    restriction = models.ForeignKey(Input_restriction, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name_plural = "Objetos de Formulario"
    
    def __unicode__(self):
        return self.core_app.name + " - " + self.type
    
#class App_structure(models.Model):
#    created = models.DateTimeField(auto_now_add=True)
#    app = models.ForeignKey(App)
#    core_app = models.ForeignKey(Core_app)
#    order = models.IntegerField()
    
#    class Meta:
#        verbose_name_plural = "Estructutas de aplicación"
    
#    def __unicode__(self):
#        return self.app.campaign.name + " - " + self.app.name + " [" + str(self.order) + "]" + " => " + self.core_app.name

class Domain(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign)
    app = models.ForeignKey(App, null=True, blank=True, on_delete=models.SET_NULL)
    domain = models.CharField(max_length=150, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Dominios"
    
    def __unicode__(self):
        return self.domain

class App_source(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Fuentes de acceso"

    def __unicode__(self):
        return self.name + " - " + self.token  + " - " + self.app.name 
    
class App_hit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    remote_addr = models.IPAddressField()
    app = models.ForeignKey(App)
    core_app = models.ForeignKey(Core_app)
    source = models.ForeignKey(App_source)
    hit = models.ForeignKey(Hit,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Visitas a la aplicación"
    
    def __unicode__(self):
        return str(self.created) + " - " + self.remote_addr + " - " + self.app.name + " - " + self.core_app.name

    
class App_record(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)
    source = models.ForeignKey(App_source)
    record = models.ForeignKey(Record,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Registros desde aplicación"

    def __unicode__(self):
        return str(self.created) + " - " + self.app.name  + " - " + str(self.id) 
    