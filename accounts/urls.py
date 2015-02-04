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

urlpatterns = patterns('',
#    url(r'^register/$', 'accounts.views.AccountRegistration'),
    url(r'^login/$', 'accounts.views.LoginRequest', name='login'),
    url(r'^logout/$', 'accounts.views.LogoutRequest', name='logout'),
    url(r'^password/$', 'django.contrib.auth.views.password_change', {'template_name':'accounts/password_change_form.html'}, name='password'),  
      
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset', {'template_name':'accounts/password_reset_form.html'}, name='new_password'),

    url(r'^profile/$', 'accounts.views.profile', name='profile'),
)