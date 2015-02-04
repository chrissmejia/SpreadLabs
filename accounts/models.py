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

from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Membership

class Agency(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Agencies"
    
    def __unicode__(self):
        return self.name    
            
class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)
    agency = models.ForeignKey(Agency)
    facebook_id  = models.CharField(max_length=100, blank=True)
    facebook_token  = models.CharField(max_length=400, blank=True)
    facebook_token_expiration  = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{0}".format(self.user.username)
    
class Campaign(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(Agency)
    created_by = models.ForeignKey(User)
    facebook_page_id = models.CharField(max_length=100, blank=True)
    membership = models.ForeignKey(Membership)
    
    class Meta:
        verbose_name_plural = "Campañas"
    
    def __unicode__(self):
        return self.name       
    
    def membership_name(self):
        if self.membership == 0:
            return "Gratuita"
        else:
            return self.membership