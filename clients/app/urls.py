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

from clients.app import views

urlpatterns = patterns('',
    url(r'^$', views.app_show, name='app_show'),
    url(r'^s/(?P<source>[^/]+)/$', views.app_show, name='app_show'),

    url(r'^app/(?P<app_id>\d+)/$', views.app_show, name='app_show'),
    url(r'^app/(?P<app_id>\d+)/(?P<source>[^/]+)/$', views.app_show, name='app_show'),
    url(r'^app/(?P<app_id>\d+)/(?P<source>[^/]+)/(?P<core_app_id>[^/]+)/$', views.app_show, name='app_show'),
    url(r'^app/(?P<app_id>\d+)/(?P<source>[^/]+)/(?P<core_app_id>[^/]+)/(?P<order>[^/]+)/$', views.app_show, name='app_show'),
    
    url(r'^facebook/app_(?P<app_id>\d+)/$', views.facebook_show, name='facebook_show'),

    url(r'^io/(?P<app_id>\d+)/(?P<source>[^/]+)/save/$', views.save, name='save'),
    url(r'^io/(?P<app_id>\d+)/save/check/$', views.check, name='check'),
    
    url(r'^update_env/(?P<hit_id>\d+)/$', views.hitting_env, name='env_update'),
    url(r'^update/(?P<hit_id>\d+)/$', views.hitting_update, name='hit_update'),    
)