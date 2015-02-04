# -*- encoding: utf-8 -*-
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

# Create your views here.
#import itertools 
import time, os, sys
import random
from django.http import HttpResponse
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from datetime import datetime, timedelta
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Count
from user_agents import parse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files import File
from facepy import GraphAPI
from stats.library import get_visits_number

from facebook.decorators import facebook_access
from facebook.library import have_page_permission

from stats.views import hitting
from apps.models import Facebook_access, App, App_hit, Core_app, App_record, Domain, App_source,\
    Core_object_background, Core_object_image_links, Core_object_youtube, Core_object_input
from records.models import Input_restriction
from accounts.models import Profile, Campaign

#@login_required
#@facebook_access('manage_pages')
#def migrate(request):
#    profile = Profile.objects.get(user_id=request.user)
#    agency = profile.agency

#    hits = App_hit.objects.filter(app_id__campaign_id__agency_id=agency).all().select_related('hit')
#    for hit in hits:
#        hit.remote_addr = hit.hit.remote_addr
#        hit.save()
#    return HttpResponse("hecho") 
    
@login_required
@facebook_access('manage_pages')
def index(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    for campaign in campaigns:
        campaign.views = App_hit.objects.filter(app_id__campaign=campaign).count()
        campaign.fb_online = have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE')
        
    records = []
    leyends = []
    for campaign in campaigns:
        if campaign.views:
            records.append(campaign.views)
            leyends.append(campaign.name)
    
    
    chartdata_campaign_views = {'x': leyends, 'y': records}
    ###########################
    ########################### Campaign Views Graph


    ########################### Main Graph
    ###########################
    ###########################
    records = []
    leyends = []
    for campaign in campaigns:
        campaign.records = App_record.objects.filter(app__campaign=campaign).count()
        if campaign.records:
            records.append(campaign.records)
            leyends.append(campaign.name)
    
    
    chartdata_campaign_records = {'x': leyends, 'y': records}
    
    ###########################
    ########################### Campaign Views Graph
    
    
    records = App_record.objects.filter(app__campaign__agency=agency).all().order_by('-created')[:5]
    
    
    apps_count = App.objects.filter(campaign_id__agency_id=agency).count()

    views_count = App_hit.objects.filter(app_id__campaign_id__agency_id=agency).count()
    visitors_count = App_hit.objects.filter(app_id__campaign_id__agency_id=agency).values("remote_addr").distinct().count()
    records_count = App_record.objects.filter(app__campaign__agency_id=agency).count()
    
    context = {
        'apps_count': apps_count,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'records_count': records_count,
        'records': records,
        'campaigns': campaigns,
        'chartdata_campaign_views': chartdata_campaign_views,
        'chartdata_campaign_records': chartdata_campaign_records,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }
    
    return render_to_response('apps/index.html', context, context_instance=RequestContext(request))


@login_required
def campaign(request, campaign_id=None):
    last_month = timezone.now() - timedelta(days=30)

    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
    
#    last_month = datetime.today() - timedelta(days=30)
    
    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
        fb_apps = Facebook_access.objects.all() #limit quantity
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    if not have_page_permission(request, campaign.facebook_page_id, 'BASIC_ADMIN'):
        hitting(request, 1507) # Stats
        return redirect('/error/1507')

    try:
        domain = Domain.objects.get(campaign=campaign)
        domain.views = App_hit.objects.filter(app_id__campaign=campaign, app=domain.app).count()
    except:
        domain = None
       

    apps_count = App.objects.filter(campaign=campaign).count()

    views_count = App_hit.objects.filter(app__campaign=campaign).count()
    visitors_count = App_hit.objects.filter(app__campaign=campaign).values("remote_addr").distinct().count()
    records_count = App_record.objects.filter(app__campaign=campaign).count()


    ########################### Apps Graph
    ###########################
    ########################### Apps
    
#    apps = App.objects.filter(campaign_id__agency_id=agency, campaign_id=campaign_id).all()
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()
    
    records = []
    leyends = []
    for app in active_apps:
        app.views = App_hit.objects.filter(app_id__campaign=campaign, app=app).count()
        if app.views:
            records.append(app.views)
            leyends.append(app.name)
    
    
    chartdata_apps = {'x': leyends, 'y': records}

    ###########################
    ########################### Apps Graph

    records = App_record.objects.filter(app__campaign=campaign).all().order_by('-created')[:5]
    
    context = {
        'apps_count': apps_count,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'records_count': records_count,
        'campaign': campaign,
        'fb_apps': fb_apps,
        'records': records,
        'domain': domain,
        'inactive_apps': inactive_apps,
        'active_apps': active_apps,
        'chartdata_apps': chartdata_apps,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }
    
    return render_to_response('apps/campaign.html', context, context_instance=RequestContext(request))

@login_required
@facebook_access('manage_pages')
def create(request, campaign_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    try:
#        fb_Access = App.objects.filter(campaign_id=campaign_id).values_list('id', flat=True)
        fb_Access = Facebook_access.objects.exclude(id__in = App.objects.filter(campaign_id=campaign_id).exclude(facebook_access=None).values_list('facebook_access', flat=True))
    except:
        hitting(request, 1506) # Stats
        return redirect('/error/1506')
    
    if not fb_Access:
        hitting(request, 1506) # Stats
        return redirect('/error/1506')
    
    
    if not have_page_permission(request, campaign.facebook_page_id, 'BASIC_ADMIN'):
        hitting(request, 1507) # Stats
        return redirect('/error/1507')    
        
    app_name = "Nueva Aplicación"
    app = App(campaign_id=campaign_id, facebook_access_id=fb_Access[0].id, name=app_name, description="", active=1, premium=0)
    picture = open(settings.STATIC_ROOT + 'images/apps/ico.jpg')
    app.picture.save('original.jpg', File(picture))
    pattern = open(settings.STATIC_ROOT + 'images/apps/pattern.jpg')
    app.pattern.save('pattern.jpg', File(pattern))
    app.save()
    picture.close()
    pattern.close()
        
    core_app = Core_app(app_id=app.pk, name="Inicio", description="Página inicial", namespace="", order=0)
    core_app.save()
#    app_structure = App_structure(app_id=app.pk, core_app_id=core_app.pk, order=0)
#    app_structure.save()
    
    background_object = Core_object_background(core_app_id=core_app.id)
    background = open(settings.STATIC_ROOT + 'images/apps/spback.jpg')
    background_object.image.save('original.jpg', File(background))
    background_object.save()
    background.close()
    
    like_core_app = Core_app(app_id=app.pk, name="No seguidores", description="Página para no seguidores", namespace="", order=-1)
    like_core_app.save()
#    app_structure = App_structure(app_id=app.pk, core_app_id=like_core_app.pk, order=-1)
#    app_structure.save()
     
    background_object = Core_object_background(core_app=like_core_app)
    background = open(settings.STATIC_ROOT + 'images/apps/spback.jpg')
    background_object.image.save('original.jpg', File(background))
    background_object.save()
    background.close()
    
    return redirect(reverse('apps:app_edit', args=[app.pk]))


@login_required
def create_new_core(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
    
    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    try:
        cores = Core_app.objects.filter(app=app).exclude(order=-1).count()
    except:
        hitting(request, 1503) # Stats
        return redirect('/error/1503')

    core_app = Core_app(app_id=app.pk, name="Nueva página " + str(cores), description="Página adicional", namespace="", order=cores)
    core_app.save()
     
    background_object = Core_object_background(core_app_id=core_app.id)

    background = open(settings.STATIC_ROOT + 'images/apps/spback.jpg')
    background_object.image.save('original.jpg', File(background))
    background_object.save()
    background.close()
    
    return redirect(reverse('apps:app_edit', args=[app.id, core_app.id]))

@login_required
@facebook_access('manage_pages')
def edit(request, app_id, core_app_id=-1, order=0):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
#    last_month = datetime.today() - timedelta(days=30)

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    try:
        domain = Domain.objects.get(campaign=app.campaign)
    except:
        domain = None
    
    try:
        fb_app = Facebook_access.objects.get(id=app.facebook_access_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    try:
        campaign = Campaign.objects.get(id=app.campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    try:
        urls = App_source.objects.filter(app=app).exclude(token='facebook').exclude(token='direct').all()
    except:
        urls = None
    
    if not have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE'):
        hitting(request, 1507) # Stats
        return redirect('/error/1507')
        
        
    ########################### Facebook
    ###########################
    ###########################
    me_graph = GraphAPI(request.session['facebook_access_token'])
    page_at = me_graph.get(str(campaign.facebook_page_id)+'?fields=access_token') 
    page_graph = GraphAPI(page_at['access_token'])
    facebook_page = page_graph.get(
        path = str(campaign.facebook_page_id)+'/tabs/'+str(fb_app.facebook_app_id)
    )
        
    facebook_tab_installed = facebook_page["data"]
    ###########################
    ###########################
        
    ########################## App
        
    try:
        if int(core_app_id) >= 0:
            core = Core_app.objects.get(app=app.id, id=core_app_id)
#            go = App_structure.objects.get(app=app.id, core_app=core_app_id)
        else:
            core = Core_app.objects.get(app=app.id, order=order)
#            go = App_structure.objects.get(app=app.id, order=order)
        like_core = Core_app.objects.get(app=app.id, order=-1)
#        like_core = App_structure.objects.get(app=app.id, order=-1)
        cores = Core_app.objects.filter(app=app).exclude(order=-1).all()
    except:
        hitting(request, 1503) # Stats
        return redirect('/error/1503')
    
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
        inputs = Core_object_input.objects.filter(core_app=core).all()
    except:
        inputs = None
        
    ####################### Data
    data = {
        'app': app,
        'source':'builder',
        'facebook_tab_installed': facebook_tab_installed,
        'campaign': campaign,
        'cores': cores,
        'this_core': core,
        'like_core': like_core,
        'fb_app': fb_app,
        'domain': domain,
        'urls': urls,
        'background': background,
        'image_links': image_links,
        'youtube': youtube,
        'inputs': inputs
    }
    ####################### Render
    return render_to_response('apps/edit.html', data, context_instance=RequestContext(request))

@login_required
@facebook_access('manage_pages')
def deactivate(request, app_id): 
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        fb_app = Facebook_access.objects.get(id=app.facebook_access_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    if not have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE'):
        hitting(request, 1507) # Stats
        return redirect('/error/1507')

    try:
        me_graph = GraphAPI(request.session['facebook_access_token'])
        page_at = me_graph.get(str(campaign.facebook_page_id)+'?fields=access_token') 
        page_graph = GraphAPI(page_at['access_token'])
        page_graph.delete(
            path = str(campaign.facebook_page_id)+'/tabs/app_'+str(fb_app.facebook_app_id),
        )
    except:
        installed = False #dummy
        
    app.facebook_access_id = None
    app.active = False
    app.save()
        
    return redirect(reverse('apps:campaign', args=[app.campaign.id]))

@login_required
def promote(request, app_id): 
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        domain = Domain.objects.get(campaign=campaign)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    domain.app = app
    domain.save()
        
    return redirect(reverse('apps:campaign', args=[app.campaign.id]))

@login_required
def bump(request, app_id): 
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        domain = Domain.objects.get(campaign=campaign)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    domain.app = None
    domain.save()
        
    return redirect(reverse('apps:campaign', args=[app.campaign.id]))

@login_required
@facebook_access('manage_pages')
def reactivate(request, app_id): 
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    try:
        fb_Access = Facebook_access.objects.exclude(id__in = App.objects.filter(campaign_id=app.campaign).exclude(facebook_access=None).values_list('facebook_access', flat=True)).all()
    except:
        hitting(request, 1506) # Stats
        return redirect('/error/1506')
    
    if not fb_Access:
        hitting(request, 1506) # Stats
        return redirect('/error/1506')
    
    app.facebook_access_id = fb_Access[0].id
    app.active = True
    app.save()
        
    return redirect(reverse('apps:index', args=[app.campaign.id]))

@login_required
#@csrf_exempt
@facebook_access('manage_pages')
def fb_install(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        fb_app = Facebook_access.objects.get(id=app.facebook_access_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    if not have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE'):
        hitting(request, 1507) # Stats
        return redirect('/error/1507')

    me_graph = GraphAPI(request.session['facebook_access_token'])
    page_at = me_graph.get(str(campaign.facebook_page_id)+'?fields=access_token') 
    page_graph = GraphAPI(page_at['access_token'])
    page_graph.post(
        path = str(campaign.facebook_page_id)+'/tabs/',
        app_id = str(fb_app.facebook_app_id)
    )
    
    if settings.ONLINE:
        try:
            page_graph.post(
                path = str(campaign.facebook_page_id)+'/tabs/app_'+str(fb_app.facebook_app_id),
                custom_name = app.name,
                custom_image_url = settings.MEDIA_URL + app.picture.name #only works on production
            )
        except:
            return redirect('http://www.facebook.com/'+campaign.facebook_page_id+'?sk=app_'+fb_app.facebook_app_id)
    else:
        page_graph.post(
            path = str(campaign.facebook_page_id)+'/tabs/app_'+str(fb_app.facebook_app_id),
            custom_name = app.name
        )            
    return redirect('http://www.facebook.com/'+campaign.facebook_page_id+'?sk=app_'+fb_app.facebook_app_id)

@login_required
def save_background(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
#    last_month = datetime.today() - timedelta(days=30)

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
        ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
        
    try:
        background_object = Core_object_background.objects.get(core_app=core)
        
        if os.path.exists(settings.MEDIA_ROOT+background_object.image.name):
            os.remove(settings.MEDIA_ROOT+background_object.image.name)
    except:
        background_object = Core_object_background(core_app_id=core.id)
    
    if request.method == 'POST':
        file = request.FILES['file']
        if file.content_type == "image/jpeg":
            file_content = ContentFile(file.read())
            background_object.image.save(file.name, file_content)
            background_object.save()
            return HttpResponse(settings.MEDIA_URL+background_object.image.name)
        hitting(request, 1002) # Stats
        return HttpResponse('e~1002')
   
    hitting(request, 404) # Stats
    return HttpResponse('e~404')

@login_required
#@csrf_exempt
def delete_background(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        background_object = Core_object_background.objects.get(core_app=core)
        background_object.delete()
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    return HttpResponse(1)


@login_required
def save_app_settings(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
#    last_month = datetime.today() - timedelta(days=30)

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    if request.POST.get('target') == "resolution":
        size = request.POST.get('value')
        size = size.split('x')
        
        app.width = size[0]
        app.height = size[1]
        app.save()
        
        return HttpResponse(1)
    
    elif request.POST.get('target') == "pattern_background":
        ########################## App    
        if request.method == 'POST':
            file = request.FILES['file']
            if file.content_type == "image/jpeg":
                file_content = ContentFile(file.read())
                app.pattern.save(file.name, file_content)
                app.save()
                return HttpResponse(settings.MEDIA_URL+app.pattern.name)
            hitting(request, 1002) # Stats
            return HttpResponse('e~1002')
   
    hitting(request, 404) # Stats
    return HttpResponse('e~404')

@login_required
#@csrf_exempt
def delete_pattern(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        background_object = Core_object_background.objects.get(core_app=core)
        background_object.delete()
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    return HttpResponse(1)

@login_required
#@csrf_exempt
def save_image_link_picture(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    if (request.POST.get('id') == 'new'):
        image_link_object = Core_object_image_links(core_app=core)
        image_link_object.link = 'https://spreadlabs.com'
        image_link_object.top = 120
        image_link_object.left= 0
        image_link_object.internal_page = core
        #picture
        image_link = open(settings.STATIC_ROOT + 'images/image_link.png')
        image_link_object.image.save('original.png', File(image_link))

        image_link_object.save()
        image_link.close()
        
        return HttpResponse(str(image_link_object.id)+"^"+image_link_object.image.name) 
    else:
        image_link_id = request.POST.get('id').split("_")
        try: 
            image_link_object = Core_object_image_links.objects.get(id=image_link_id[2])
            if os.path.exists(settings.MEDIA_ROOT+image_link_object.image.name):
                os.remove(settings.MEDIA_ROOT+image_link_object.image.name)
        except:
            hitting(request, 404) # Stats
            return HttpResponse('e~404')
    
        if request.method == 'POST':
            file = request.FILES['file']
            if (file.content_type == "image/jpeg") or (file.content_type == "image/png"):
                file_content = ContentFile(file.read())
                image_link_object.image.save(file.name, file_content)
                image_link_object.save()
                return HttpResponse(settings.MEDIA_URL+image_link_object.image.name)       
    hitting(request, 404) # Stats
    return HttpResponse('e~404')

@login_required
#@csrf_exempt
def save_image_link_attrs(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        image_link_id = request.POST.get('target').split("_")
        image_link_object = Core_object_image_links.objects.get(id=image_link_id[2], core_app=core)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
        
    if (request.POST.get('id') == 'link'):
        image_link_object.link = request.POST.get('value')
    elif (request.POST.get('id') == 'type'):
        image_link_object.type = request.POST.get('value')
    elif (request.POST.get('id') == 'internal_page'):
        try:
            core = Core_app.objects.get(id=request.POST.get('value'))
            image_link_object.internal_page = core
        except:
            hitting(request, 1004) # Stats
            return HttpResponse('e~1004')
    else:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    image_link_object.save()
    return HttpResponse(request.POST.get('value'))
    

@login_required
#@csrf_exempt
def save_image_link_position(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        image_link_id = request.POST.get('id').split("_")
        image_link_object = Core_object_image_links.objects.get(id=image_link_id[2], core_app=core)
        image_link_object.left = request.POST.get('left')
        image_link_object.top = request.POST.get('top')
        image_link_object.save()
        return HttpResponse(1)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')


@login_required
#@csrf_exempt
def delete_image_link(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        image_link_id = request.POST.get('id').split("_")
        image_link_object = Core_object_image_links.objects.get(id=image_link_id[2], core_app=core)
        image_link_object.delete()
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    return HttpResponse(1)
    
@login_required
#@csrf_exempt
def save_youtube_video(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    youtube_object = Core_object_youtube(core_app=core)
    youtube_object.video = 'O6OnY_8l6Us'
    youtube_object.top = 120
    youtube_object.left= 0
    youtube_object.save()
        
    return HttpResponse(youtube_object.id) 

@login_required
#@csrf_exempt
def save_youtube_position(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        youtube_id = request.POST.get('id').split("_")
        youtube_object = Core_object_youtube.objects.get(id=youtube_id[1], core_app=core)
        youtube_object.left = request.POST.get('left')
        youtube_object.top = request.POST.get('top')
        youtube_object.save()
        return HttpResponse(1)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')

@login_required
#@csrf_exempt
def save_youtube_attrs(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try:
        youtube_id = request.POST.get('video').split("_")
        youtube_object = Core_object_youtube.objects.get(id=youtube_id[1], core_app=core)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
        
    if (request.POST.get('id') == 'video'):
        youtube_object.video = request.POST.get('value')
    else:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
        
    youtube_object.save()
    return HttpResponse(request.POST.get('value'))

@login_required
#@csrf_exempt
def delete_youtube(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        youtube_id = request.POST.get('id').split("_")
        youtube_object = Core_object_youtube.objects.get(id=youtube_id[1], core_app=core)
        youtube_object.delete()
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    return HttpResponse(1)

@login_required
#@csrf_exempt
def save_input(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
    
    if not request.POST.get('type'):
        hitting(request, 1002) # Stats
        return HttpResponse('e~1002')

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    type = Core_object_input.objects.filter(core_app=core, type=request.POST.get('type')).count()
    if type:
        hitting(request, 1003) # Stats
        return HttpResponse('e~1003')
    
    input_object = Core_object_input(core_app=core)
    input_object.top = 120
    input_object.type = request.POST.get('type')
    input_object.save()
        
    return HttpResponse(input_object.id) 

@login_required
#@csrf_exempt
def save_input_position(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        input_id = request.POST.get('id').split("_")
        input_object = Core_object_input.objects.get(id=input_id[1], core_app=core)
        input_object.left = request.POST.get('left')
        input_object.top = request.POST.get('top')
        input_object.save()
        return HttpResponse(1)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')

@login_required
#@csrf_exempt
def save_input_attrs(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try:
        input_id = request.POST.get('target').split("_")
        input_object = Core_object_input.objects.get(id=input_id[1], core_app=core)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    if (request.POST.get('id') == 'type'):
        input_object.type = request.POST.get('value')
    elif (request.POST.get('id') == 'size'):
        input_object.size = request.POST.get('value')
    elif (request.POST.get('id') == 'color'):
        input_object.color = request.POST.get('value')
    elif (request.POST.get('id') == 'default_color'):
        input_object.default_color = request.POST.get('value')
    elif (request.POST.get('id') == 'error_color'):
        input_object.error_color = request.POST.get('value')
    elif (request.POST.get('id') == 'default'):
        input_object.default = request.POST.get('value')
    elif (request.POST.get('id') == 'transparent'):
        if (request.POST.get('value') == "false"): value = False
        else: value = True
        input_object.transparent = value
    elif (request.POST.get('id') == 'width'):
        input_object.width = request.POST.get('value')
    elif (request.POST.get('id') == 'custom_name'):
        input_object.custom_name = request.POST.get('value')
    else:
        #restrictions
        if input_object.restriction == None:
            input_restriction = Input_restriction()
            input_restriction.save()
            input_object.restriction = input_restriction

        if (request.POST.get('id') == 'required'):
            if (request.POST.get('value') == "false"): value = False
            else: value = True
            input_object.restriction.required = value
            input_object.restriction.save()
        elif (request.POST.get('id') == 'custom_type'):
            input_object.restriction.type = request.POST.get('value')
            input_object.restriction.save()
        elif (request.POST.get('id') == 'characters'):
            value = request.POST.get('value')
            characters = value.split("-")
            input_object.restriction.min_characters = characters[0]
            input_object.restriction.max_characters = characters[1]
            input_object.restriction.save()
        else:
            hitting(request, 404) # Stats
            return HttpResponse('e~404')
    
    input_object.save()
    return HttpResponse(request.POST.get('value'))


@login_required
#@csrf_exempt
def delete_input(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    ########################## App        
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
    
    try: 
        input_id = request.POST.get('id').split("_")
        input_object = Core_object_input.objects.get(id=input_id[1], core_app=core)
        input_object.delete()
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
    
    return HttpResponse(1)


@login_required
#@csrf_exempt
def save_page_attrs(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')

    ########################## Core
    try: 
        core = Core_app.objects.get(app=app.id, id=request.POST.get('core'))
    except:
        hitting(request, 1503) # Stats
        return HttpResponse('e~1503')
            
    if (request.POST.get('id') == 'like_core_enabled'):
        if (request.POST.get('value') == 'true'): active = True
        else: active = False
        app.like_page = active
        app.save()
    elif (request.POST.get('id') == 'delete'):
        if core.order >= 1:
            core.delete()
        else:
            hitting(request, 1003) # Stats
            return HttpResponse('e~1003')
    elif (request.POST.get('id') == 'page_name'):
        try:
            if not core.name == request.POST.get('value'):
                exist = Core_app.objects.get(app_id=app, name=request.POST.get('value'))
                hitting(request, 1508) # Stats
                return HttpResponse('e~1508')
        except:
            core.name = request.POST.get('value')
            core.save()
    else:
        hitting(request, 404) # Stats
        return HttpResponse('e~404')
        
    return HttpResponse(request.POST.get('value'))


@login_required
#@csrf_exempt
@facebook_access('manage_pages')
def save_icon(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
#    last_month = datetime.today() - timedelta(days=30)

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        fb_app = Facebook_access.objects.get(id=app.facebook_access_id)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
        
    
    if not have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE'):
        hitting(request, 1507) # Stats
        return HttpResponse('e~1507')
        
    if request.method == 'POST':
        file = request.FILES['file']
        if file.content_type == "image/jpeg":
            file_content = ContentFile(file.read())
            app.picture.save(file.name, file_content)
            app.save()
            # Facebook update
            me_graph = GraphAPI(request.session['facebook_access_token'])
            page_at = me_graph.get(str(campaign.facebook_page_id)+'?fields=access_token') 
            page_graph = GraphAPI(page_at['access_token'])
            
            if settings.ONLINE:
                page_graph.post(
                    path = str(campaign.facebook_page_id)+'/tabs/app_'+str(fb_app.facebook_app_id),
                    custom_image_url = settings.MEDIA_URL+app.picture.name #only works on production
                )
            
            return HttpResponse(settings.MEDIA_URL+app.picture.name)

    hitting(request, 404) # Stats
    return HttpResponse('e~404')

@login_required
#@csrf_exempt
@facebook_access('manage_pages')
def save_description(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
        campaign = Campaign.objects.get(id=app.campaign_id)
        fb_app = Facebook_access.objects.get(id=app.facebook_access_id)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    if not have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE'):
        hitting(request, 1507) # Stats
        return HttpResponse('e~1507')

    if request.POST.get('id') == 'name':
        me_graph = GraphAPI(request.session['facebook_access_token'])
        page_at = me_graph.get(str(campaign.facebook_page_id)+'?fields=access_token') 
        page_graph = GraphAPI(page_at['access_token'])
        
        try:
            page_graph.post(
                path = str(campaign.facebook_page_id)+'/tabs/app_'+str(fb_app.facebook_app_id),
                custom_name = request.POST.get('value')
            )
        except:
            none = None
            
        app.name = request.POST.get('value')
        
    if request.POST.get('id') == 'description':
        app.description = request.POST.get('value')

    app.save()
    
    return HttpResponse(request.POST.get('value'))
        
        
@login_required
def save_url(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return HttpResponse('e~1001')
    
    if request.POST.get('name') and request.POST.get('token'):
        if request.POST.get('token') == 'facebook' or request.POST.get('token') == 'direct':
            hitting(request, 1510) # Stats
            return HttpResponse('e~1510')            
        try:
            exist = App_source.objects.get(app_id=app, token=request.POST.get('token')) ### required
            hitting(request, 1509) # Stats
            return HttpResponse('e~1509')
        except:
            source = App_source(app=app, name=request.POST.get('name'), token=request.POST.get('token'))
            source.save()
        return HttpResponse(source.name+'^'+source.token)
     
    hitting(request, 404) # Stats
    return HttpResponse('e~404')
