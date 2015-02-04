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

import urllib, socket, sys
from django.conf import settings
from django.core.urlresolvers import reverse
from urlparse import parse_qs
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

@login_required
def get_code(request):
    host = request.META["HTTP_HOST"]
    
    error = request.GET.get('error', None)
    if error is not None:
        return redirect('/error/1001') #cancel permission custom error
    
    args = dict(client_id=settings.FACEBOOK_APP_ID, redirect_uri="http://"+host+reverse('facebook:get_auth'), scope=settings.FACEBOOK_INITIAL_SCOPE)
    redirect_url = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)
    print >>sys.stderr, redirect_url
    return HttpResponseRedirect(redirect_url)
    
@login_required
def get_access_token(request):
    host = request.META["HTTP_HOST"]
    if 'facebook_redirect_url' not in request.session:
        request.session['facebook_redirect_url'] = "http://"+host+'/dashboard/'
    
    error = request.GET.get('error', None)
    if error is not None:
        return redirect('/error/1001') #cancel permission custom error
    
    code = request.GET.get('code', None)
    if code is None:
        return redirect(reverse('facebook:get_code'))
    else:
        args = dict(client_id=settings.FACEBOOK_APP_ID, redirect_uri="http://"+host+reverse('facebook:get_auth'))
        args["client_secret"] = settings.FACEBOOK_APP_SECRET_KEY
        args["code"] = code
        
        token_url = "https://graph.facebook.com/oauth/access_token?"+urllib.urlencode(args)
        #request.session['access_token']
        short_access_query = urllib.urlopen(token_url).read()
#        test = urlparse(at)
        access_token = parse_qs(short_access_query)

        access_token = str(access_token['access_token'][0]);
        request.session['facebook_access_token'] = access_token
        
        go = request.session['facebook_redirect_url']
        return HttpResponseRedirect(go)