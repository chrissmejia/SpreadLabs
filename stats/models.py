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
from accounts.models import User

# Create your models here.
class Hit(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True,null=True)

    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    referer = models.CharField(max_length=2000,blank=True,null=True)
    origin = models.CharField(max_length=2000,blank=True,null=True)
    status_code = models.IntegerField()
    user_agent = models.CharField(max_length=1000,blank=True,null=True)
    remote_addr = models.IPAddressField()
    remote_addr_fwd = models.IPAddressField(blank=True,null=True)
    meta = models.TextField()
    cookies = models.TextField(blank=True,null=True)
    get = models.TextField(blank=True,null=True)
    post = models.TextField(blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    is_secure = models.BooleanField(default=False)
    is_ajax = models.BooleanField(default=False)
    user = models.ForeignKey(User,blank=True,null=True)  
    
    #env
    window_height = models.IntegerField(blank=True,null=True)
    window_width = models.IntegerField(blank=True,null=True)
    screen_height = models.IntegerField(blank=True,null=True)
    screen_width = models.IntegerField(blank=True,null=True)

    color = models.CharField(max_length=10, blank=True,null=True)
    
    flash = models.CharField(max_length=20, blank=True,null=True)
    java = models.BooleanField(default=False)
    silverlight = models.CharField(max_length=20, blank=True,null=True)
    
    html5_canvas = models.BooleanField(default=False)
    html5_video = models.BooleanField(default=False)
    html5_audio = models.BooleanField(default=False)
    html5_storage = models.BooleanField(default=False)
    svg = models.BooleanField(default=False)
    webgl = models.BooleanField(default=False)
    
#    user_agent_is_mobile  = models.BooleanField(default=False)
#    user_agent_is_tablet  = models.BooleanField(default=False)
#    user_agent_is_touch_capable  = models.BooleanField(default=False)
#    user_agent_is_pc  = models.BooleanField(default=False)
#    user_agent_is_bot  = models.BooleanField(default=False)

#    user_agent_browser  = models.CharField(max_length=2000)
#    user_agent_browser.family  = models.CharField(max_length=200)
#    user_agent_browser.version  = models.CharField(max_length=6)
#    user_agent_browser.version_string  = models.CharField(max_length=6)

#    user_agent_os  = models.CharField(max_length=200)
#    user_agent_os.family  = models.CharField(max_length=200)
#    user_agent_os.version  = models.CharField(max_length=6)
#    user_agent_os.version_string  = models.CharField(max_length=6)

#    user_agent_device  = models.CharField(max_length=200)
#    user_agent_device.family  = models.CharField(max_length=200)    
    class Meta:
        verbose_name_plural = "Visitas SpreadLabs"
    
    def __unicode__(self):
        return str(self.created) + " - " + self.remote_addr + " - " + self.uri
