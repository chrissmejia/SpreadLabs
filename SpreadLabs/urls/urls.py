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

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('web.urls', namespace="index")),

    url(r'^asap/', include('asap.urls', namespace="asap")),
    
#    (r'^500/$', 'django.views.defaults.server_error', {'template': '500.html'}),
#    (r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),

    url(r'^error/', include('errors.urls', namespace="error")),

    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
    url(r'^dashboard/accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^dashboard/apps/', include('apps.urls', namespace="apps")),
    url(r'^dashboard/asap/', include('asap.urls', namespace="asap")),
    url(r'^dashboard/facebook/', include('facebook.urls', namespace="facebook")),
    url(r'^dashboard/gate/admin/', include(admin.site.urls)),
    url(r'^dashboard/records/', include('records.urls', namespace="records")),
    url(r'^dashboard/stats/', include('stats.urls', namespace="stats")),
    
    url(r'^password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name':'accounts/password_change_done.html'}),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'accounts/password_reset_done.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'accounts/password_reset_confirm.html'}),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'accounts/password_reset_complete.html'}),

    url(r'^clients/', include('SpreadLabs.urls.clients', namespace="clients")),
)
