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

from django.conf.urls import patterns, url

from statsExtended import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^campaign/(?P<campaign_id>\d+)$', views.main_campaign, name='main_campaign'),
    url(r'^app/(?P<app_id>\d+)$', views.main_app, name='main_app'),

    url(r'^enviroment/$', views.main_environment, name='main_enviroment'),
    url(r'^campaign/enviroment/(?P<campaign_id>\d+)$', views.main_campaign_enviroment, name='main_campaign_enviroment'),
    url(r'^app/enviroment/(?P<app_id>\d+)$', views.main_app_enviroment, name='main_app_enviroment'),

    url(r'^system/$', views.main_system, name='main_system'),
    url(r'^campaign/system/(?P<campaign_id>\d+)$', views.main_campaign_system, name='main_campaign_system'),
    url(r'^app/system/(?P<app_id>\d+)$', views.main_app_system, name='main_app_system'),

    url(r'^advanced/$', views.main_advanced, name='main_advanced'),
    url(r'^campaign/advanced/(?P<campaign_id>\d+)$', views.main_campaign_advanced, name='main_campaign_advanced'),
    url(r'^app/advanced/(?P<app_id>\d+)$', views.main_app_advanced, name='main_app_advanced'),
)