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
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime

from stats.models import Hit

from facepy import SignedRequest

from stats.views import hitting
from apps.models import Facebook_access, App, App_hit, App_record, Core_app, Domain, App_source,\
    Core_object_background, Core_object_image_links, Core_object_youtube, Core_object_input
from accounts.models import Profile, Campaign
from records.models import Record
from django.conf import settings


@csrf_exempt
def facebook_show(request, app_id): 
    try:
        fb_Access = Facebook_access.objects.get(facebook_app_id=app_id)
    except:
        hitting(request, 1501) # Stats
        return redirect('/error/1501')

    if 'signed_request' in request.REQUEST:
        signed_request = SignedRequest.parse(request.REQUEST.get('signed_request'), str(fb_Access.facebook_app_secret_key))
        ################ Get Structure

        try: 
            app = App.objects.get(facebook_access=fb_Access.id, campaign__facebook_page_id=signed_request['page']['id'])
            campaign = Campaign.objects.get(id=app.campaign_id)
        except:
            hitting(request, 1502) # Stats
            return redirect('/error/1502')

        liked = signed_request['page']['liked']
        if not liked:
            if app.like_page == 1 and campaign.membership.like_page:
                return redirect(reverse('clients:app_show', args=[app.id, 'facebook', -1, -1]))
            
            
            
        return redirect(reverse('clients:app_show', args=[app.id,  'facebook']))

    else:
        hitting(request, 1504) # Stats
        return redirect('/error/1504')

#    hit_response = hitting(request, 200) # Stats
#    App_hit(app_id=app.id, core_app=go.core_app, hit_id=hit_response).save() # Stats 
    
#    try:
#        background = Core_object_background.objects.get(core_app=go.core_app)
#    except:
#        background = None
    
#    try:
#        image_links = Core_object_image_links.objects.filter(core_app=go.core_app).all()
#    except:
#        image_links = None
                
#    try:
#        youtube = Core_object_youtube.objects.filter(core_app=go.core_app).all()
#    except:
#        youtube = None
#               
#    try:
#        inputs = Core_object_input.objects.filter(core_app=go.core_app).order_by('top', 'left').all()
#    except:
#        inputs = None
#        
#    context = {'app': app,
#               'background': background,
#               'image_links': image_links,
#               'youtube': youtube,
#               'inputs': inputs,
#               'external': True}
    
#    return render_to_response('apps/facebook_render.html', context, context_instance=RequestContext(request))
    
@csrf_exempt
def app_show(request, app_id=None, source='direct', core_app_id=-1, order=0):
    host = request.META["HTTP_HOST"]
    if (host.startswith('www.')):
        host = host[4:]

    if not host == 'spreadlabs.com' and settings.ONLINE:
        try:
            domain = Domain.objects.get(domain=host)
        except:
            hitting(request, 1005) # Stats
            return redirect('/error/1005')
        
        if not app_id:
            app = domain.app
            campaign = domain.campaign
        
            if not app:
                hitting(request, 1006) # Stats
                return redirect('/error/1006')
        else:
            try:
                app = App.objects.get(id=app_id, active=True, campaign=domain.campaign)
                campaign = app.campaign
            except:
                hitting(request, 1502) # Stats
                return redirect('/error/1502')
                    
    else:
        if not app_id:
            hitting(request, 1003) # Stats
            return redirect('/error/1003')
            
        try:
            app = App.objects.get(id=app_id, active=True)
            campaign = app.campaign
        except:
            hitting(request, 1502) # Stats
            return redirect('/error/1502')
        
        
    try:
        if int(core_app_id) >= 0:
            core = Core_app.objects.get(app=app, id=core_app_id)
#            go = App_structure.objects.get(app=app.id, core_app=core_app_id)
        else:
            core = Core_app.objects.get(app=app, order=order)
#            go = App_structure.objects.get(app=app.id, order=order)
    except:
        hitting(request, 1503) # Stats
        return redirect('/error/1503')

    hit_response = hitting(request, 200) # Stats
    hit = App_hit(app_id=app.id, remote_addr=hit_response.remote_addr, core_app=core, hit=hit_response)
    
    try:
        source_obj = App_source.objects.get(app=app, token=source)
    except:
        if source == 'facebook':
            source_obj = App_source(app=app, name="Facebook", token='facebook')
            source_obj.save()
        else:
            try:
                source_obj = App_source.objects.get(app=app, token='direct')
            except:
                source_obj = App_source(app=app, name="Directo", token='direct')
                source_obj.save()
        
    hit.source = source_obj
    hit.save() # Stats 
    
    
    try:
        background = Core_object_background.objects.get(core_app=core)
    except:
        background = None
    
    try:
        image_links = Core_object_image_links.objects.filter(core_app=core).all()
    except:
        image_links = None
                
    try:
        youtube = Core_object_youtube.objects.filter(core_app=core).all()
    except:
        youtube = None
               
    try:
        inputs = Core_object_input.objects.filter(core_app=core).order_by('top', 'left').all()
    except:
        inputs = None
        
    print >>sys.stderr, inputs
    
    context = {'app': app,
               'hit': hit_response,
               'source':source,
               'background': background,
               'image_links': image_links,
               'campaign': campaign,
               'youtube': youtube,
               'inputs': inputs,
               'external': True}
    
    return render_to_response('clients/app/render.html', context, context_instance=RequestContext(request))

def save(request, app_id, source):
    app = App.objects.get(id=app_id)
    
    record_object = Record(campaign=app.campaign)
    if (request.POST.get('name')):
        record_object.name = request.POST.get('name')
    if (request.POST.get('lastname')):
        record_object.lastname = request.POST.get('lastname')
    if (request.POST.get('email')):
        record_object.email = request.POST.get('email')
    if (request.POST.get('id')):
        record_object.identification = request.POST.get('id')
    if (request.POST.get('cellphone')):
        record_object.cellphone = request.POST.get('cellphone')
    if (request.POST.get('year_of_birth')):
        record_object.year_of_birth = request.POST.get('year_of_birth')
    if (request.POST.get('birth_month')):
        record_object.birth_month = request.POST.get('birth_month')
    if (request.POST.get('day_of_birth')):
        record_object.day_of_birth = request.POST.get('day_of_birth')
    
    record_object.save()

    record_app = App_record(app=app, record=record_object)
    
    
    try:
        source_obj = App_source.objects.get(app=app, token=source)
    except:
        if source == 'facebook':
            source_obj = App_source(app=app, name="Facebook", token='facebook')
            source_obj.save()
        else:
            try:
                source_obj = App_source.objects.get(app=app, token='direct')
            except:
                source_obj = App_source(app=app, name="Directo", token='direct')
                source_obj.save()
        
    record_app.source = source_obj
    record_app.save()
    
    return HttpResponse(1)

def check(request, app_id): 
    app = App.objects.get(id=app_id)
    
    if (request.POST.get('id')):
        exists = App_record.objects.filter(app=app, record__identification=request.POST.get('id')).count()
        if exists:
            return HttpResponse("false")
    elif (request.POST.get('cellphone')):
        exists = App_record.objects.filter(app=app, record__cellphone=request.POST.get('cellphone')).count()
        if exists:
            return HttpResponse("false")
    elif (request.POST.get('email')):
        exists = App_record.objects.filter(app=app, record__email=request.POST.get('email')).count()
        if exists:
            return HttpResponse("false")
        
    return HttpResponse("true")


def hitting_env(request, hit_id):
    
    try:
        hit = Hit.objects.get(id=hit_id)
    except:
        hitting(request, 1003) # Stats
        return redirect('/error/1003')
        
    if (request.POST.get('window_height')):
        hit.window_height = request.POST.get('window_height')
    if (request.POST.get('window_width')):
        hit.window_width = request.POST.get('window_width')
    if (request.POST.get('screen_height')):
        hit.screen_height = request.POST.get('screen_height')
    if (request.POST.get('screen_width')):
        hit.screen_width = request.POST.get('screen_width')
    if (request.POST.get('color_depth')):
        hit.color = request.POST.get('color_depth')
        
    if (request.POST.get('flash')):
        hit.flash = request.POST.get('flash')
    if (request.POST.get('java_enabled')):
        hit.java = request.POST.get('java_enabled')
    if (request.POST.get('silverlight')):
        hit.silverlight = request.POST.get('silverlight')
        
    if (request.POST.get('html5_canvas')):
        hit.html5_canvas = request.POST.get('html5_canvas')
    if (request.POST.get('html5_video')):
        hit.html5_video = request.POST.get('html5_video')
    if (request.POST.get('html5_audio')):
        hit.html5_audio = request.POST.get('html5_audio')
    if (request.POST.get('html5_storage')):
        hit.html5_storage = request.POST.get('html5_storage')
        
    if (request.POST.get('svg')):
        hit.svg = request.POST.get('svg')
    if (request.POST.get('webgl')):
        hit.webgl = request.POST.get('webgl')
        
    hit.save()
    
    return HttpResponse(hit.id)


def hitting_update(request, hit_id):
    
    try:
        hit = Hit.objects.get(id=hit_id)
    except:
        hitting(request, 1003) # Stats
        return redirect('/error/1003')

    hit.updated = datetime.utcnow()
    hit.save()
    
    return HttpResponse(hit.id)
