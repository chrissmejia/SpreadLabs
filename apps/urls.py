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

from django.conf.urls import patterns, include, url
from apps import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
#    url(r'^migrate/$', views.migrate, name='migrate'),

    url(r'^campaign/(?P<campaign_id>\d+)$', views.campaign, name='campaign'),

    url(r'^app/edit/(?P<app_id>[^/]+)/deactivate$', views.deactivate, name='deactivate'),
    url(r'^app/edit/(?P<app_id>[^/]+)/reactivate$', views.reactivate, name='reactivate'),
    url(r'^app/edit/(?P<app_id>[^/]+)/promote', views.promote, name='promote'),
    url(r'^app/edit/(?P<app_id>[^/]+)/bump', views.bump, name='bump'),

#    url(r'^app/(?P<app_id>[^/]+)/$', views.details, name='details'),
#    url(r'^app/(?P<app_id>[^/]+)/records/$', views.app_records, name='records'),
#    url(r'^app/(?P<app_id>[^/]+)/platform/$', views.app_platform_details, name='platform_details'),
#    url(r'^facebook/app/(?P<app_id>[^/]+)/(?P<next_id>\d+)$', views.facebook_details, name='facebook_details_search'),

    url(r'^create/(?P<campaign_id>\d+)$', views.create, name='app_create'),
    url(r'^edit/(?P<app_id>[^/]+)/$', views.edit, name='app_edit'),
    url(r'^edit/(?P<app_id>[^/]+)/(?P<core_app_id>[^/]+)/$', views.edit, name='app_edit'),
    url(r'^edit/(?P<app_id>[^/]+)/(?P<core_app_id>[^/]+)/(?P<order>[^/]+)/$', views.edit, name='app_edit'),
    url(r'^core/edit/create/(?P<app_id>[^/]+)/$', views.create_new_core, name='app_create_core'),
    
    url(r'^install/(?P<app_id>[^/]+)/$', views.fb_install, name='fb_install'),
    url(r'^save_icon/(?P<app_id>[^/]+)/$', views.save_icon, name='save_icon'),
    
    url(r'^save_description/(?P<app_id>[^/]+)/$', views.save_description, name='save_description'),

    url(r'^save_background/(?P<app_id>[^/]+)/$', views.save_background, name='save_background'),
    url(r'^delete_background/(?P<app_id>[^/]+)/$', views.delete_background, name='delete_background'),

    url(r'^save_pattern/(?P<app_id>[^/]+)/$', views.save_app_settings, name='save_app_settings'),
    url(r'^delete_pattern/(?P<app_id>[^/]+)/$', views.delete_pattern, name='delete_pattern'),

    url(r'^save_image_link/(?P<app_id>[^/]+)/$', views.save_image_link_picture, name='save_image_link'),
    url(r'^save_image_link_position/(?P<app_id>[^/]+)/$', views.save_image_link_position, name='save_image_link_position'),
    url(r'^save_image_link_attrs/(?P<app_id>[^/]+)/$', views.save_image_link_attrs, name='save_image_link_attrs'),
    url(r'^delete_image_link/(?P<app_id>[^/]+)/$', views.delete_image_link, name='delete_image_link'),

    url(r'^save_youtube/(?P<app_id>[^/]+)/$', views.save_youtube_video, name='save_youtube'),
    url(r'^save_youtube_position/(?P<app_id>[^/]+)/$', views.save_youtube_position, name='save_youtube_position'),
    url(r'^save_youtube_attrs/(?P<app_id>[^/]+)/$', views.save_youtube_attrs, name='save_youtube_attrs'),
    url(r'^delete_youtube/(?P<app_id>[^/]+)/$', views.delete_youtube, name='delete_youtube'),

    url(r'^save_input/(?P<app_id>[^/]+)/$', views.save_input, name='save_input'),
    url(r'^save_input_position/(?P<app_id>[^/]+)/$', views.save_input_position, name='save_input_position'),
    url(r'^save_input_attrs/(?P<app_id>[^/]+)/$', views.save_input_attrs, name='save_input_attrs'),
    url(r'^delete_input/(?P<app_id>[^/]+)/$', views.delete_input, name='delete_input'),

    url(r'^save_page_attrs/(?P<app_id>[^/]+)/$', views.save_page_attrs, name='save_page_attrs'),

    url(r'^save_url/(?P<app_id>[^/]+)/$', views.save_url, name='save_url'),

    url(r'^extended/', include('appsExtended.urls', namespace="extended")),
)