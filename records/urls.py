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

from records import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<campaign_id>\d+)$', views.details, name='details'),
    url(r'^app/(?P<app_id>\d+)$', views.app, name='app'),

    url(r'^export/$', views.export_all, name='export_all'),
    url(r'^export/campaign/(?P<campaign_id>\d+)$', views.export_campaign, name='export_campaign'),
    url(r'^export/app/(?P<app_id>\d+)$', views.export_app, name='export_app'),
    
    url(r'^extended/', include('recordsExtended.urls', namespace="extended")),    
)