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
from accounts.models import Campaign

# Create your models here.

class Record(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign)
    name = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    identification = models.CharField(max_length=100, blank=True, null=True)
    cellphone = models.IntegerField(blank=True, null=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    birth_month = models.IntegerField(blank=True, null=True)
    day_of_birth = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.created) + " - " + self.campaign.name  + " - " + str(self.id) 

class Custom_record(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    
class Input_restriction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, default="text")
    min_characters = models.IntegerField(default=1)
    max_characters = models.IntegerField(default=1)
    required = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Restricciones"
