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

class Membership(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    max_apps = models.IntegerField(default=0)
    white_mark = models.BooleanField(default=False)
    like_page = models.BooleanField(default=False)
    own_domain = models.BooleanField(default=False)
    button_tool = models.BooleanField(default=False)
    youtube_tool = models.BooleanField(default=False)
    form_tool = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Membresías"
    
    def __unicode__(self):
        return self.name