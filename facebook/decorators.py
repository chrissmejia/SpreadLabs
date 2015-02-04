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

import sys
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.conf import settings

from facepy import GraphAPI

from functools import wraps


def facebook_access(permission = None):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            
#            print >>sys.stderr, "if"
            if ('facebook_access_token' in request.session):
#                try:
                    graph = GraphAPI(request.session['facebook_access_token'])
                    try:
#                        print >>sys.stderr, request.session['facebook_access_token']
                        current_permission = graph.get('me/permissions')
                    except:
#                        print >>sys.stderr, "except"
                        request.session['facebook_redirect_url'] = request.build_absolute_uri()
                        return redirect(reverse('facebook:get_code'))
                    
#                    if not settings.FACEBOOK_INITIAL_SCOPE:
 #                       print >>sys.stderr, "not"
                    if not permission:
                        return func(request, *args, **kwargs)
                    
                    permission_list = permission.split(', ')
                    if set(permission_list).issubset(set(current_permission['data'][0])):
                        return func(request, *args, **kwargs)
  #                  else:
   #                     print >>sys.stderr, "yes"
    #                    initial_scope = settings.FACEBOOK_INITIAL_SCOPE.split(', ')
     #                   if set(initial_scope).issubset(set(current_permission['data'][0])):
      #                      if not permission:
       #                         return func(request, *args, **kwargs)
        #                    else:
         #                       permission_list = permission.split(', ')
          #                      if set(permission_list).issubset(set(current_permission['data'][0])):
           #                         return func(request, *args, **kwargs)

                    request.session['facebook_redirect_url'] = request.build_absolute_uri()
                    return redirect(reverse('facebook:get_code'))
            else:
                request.session['facebook_redirect_url'] = request.build_absolute_uri()
                return redirect(reverse('facebook:get_code'))
            
        return wraps(func)(inner_decorator)
    return decorator
