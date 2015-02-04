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

import time
from django.conf import settings
from django.utils.cache import patch_vary_headers

class MultiHostMiddleware:

    def process_request(self, request):
        try:
            request.META["LoadingStart"] = time.time()
            host = request.META["HTTP_HOST"]
            #if host[-3:] == ":80":
            #    host = host[:-3] # ignore default port number, if present

            # best way to do this.
            host_port = host.split(':')
            if len(host_port)==2:                    
                host = host_port[0]
                
            if (host.startswith('www.')):
                host = host[4:]

            if settings.HOST_MIDDLEWARE_URLCONF_MAP.has_key(host):
                request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
                request.META["MultiHost"] = str(request.urlconf)
            else:
                request.META["MultiHost"] = str(settings.ROOT_URLCONF)

        except KeyError:
            pass # use default urlconf (settings.ROOT_URLCONF)

    def process_response(self, request, response):
        if request.META.has_key('MultiHost'):
            response['MultiHost'] = request.META.get("MultiHost")

        if request.META.has_key('LoadingStart'):
            _loading_time = time.time() - int(request.META["LoadingStart"])
            response['LoadingTime'] = "%.2fs" % ( _loading_time, )

        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response