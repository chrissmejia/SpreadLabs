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

from django.conf.urls import patterns, url, include

from stats import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^environment/$', views.environment, name='environment'),
    url(r'^system/$', views.system, name='system'),
    url(r'^advanced/$', views.advanced, name='advanced'),

    url(r'^campaign/(?P<campaign_id>\d+)/$', views.campaign, name='campaign'),
    url(r'^environment/campaign/(?P<campaign_id>\d+)/$', views.campaign_environment, name='campaign_environment'),
    url(r'^system/campaign/(?P<campaign_id>\d+)/$', views.campaign_system, name='campaign_system'),
    url(r'^advanced/campaign/(?P<campaign_id>\d+)/$', views.campaign_advanced, name='campaign_advanced'),

    url(r'^app/(?P<app_id>\d+)/$', views.app, name='app'),
    url(r'^environment/app/(?P<app_id>\d+)/$', views.app_environment, name='app_environment'),
    url(r'^system/app/(?P<app_id>\d+)/$', views.app_system, name='app_system'),
    url(r'^advanced/app/(?P<app_id>\d+)/$', views.app_advanced, name='app_advanced'),
    
    url(r'^extended/', include('statsExtended.urls', namespace="extended")),        
)