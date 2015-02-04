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
import time
import json, sys
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.template import RequestContext
from user_agents import parse
from django.db.models import Count
from operator import itemgetter
from stats.library import limit_results_dict

from stats.models import Hit

from accounts.models import Campaign, Profile
from apps.models import App, App_hit, App_source

def dumps(value):
    return json.dumps(value, default=lambda o:None)

def hitting(request, response):
    user = request.user
    if str(user) == "AnonymousUser" : user = None

    meta = request.META.copy()
    meta.pop('QUERY_STRING',None)
    meta.pop('HTTP_COOKIE',None)
    remote_addr_fwd = None

    if 'HTTP_X_FORWARDED_FOR' in meta:
        remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
            meta.pop('HTTP_X_FORWARDED_FOR')

    new = Hit(
        host = request.get_host(),
        path = request.path,
        method = request.method,
        uri = request.build_absolute_uri(),
        referer = meta.pop('HTTP_REFERER',None),
        origin = meta.pop('HTTP_ORIGIN',None),
        status_code = response,
        user_agent = meta.pop('HTTP_USER_AGENT',None),
        remote_addr = meta.pop('REMOTE_ADDR',None),
        remote_addr_fwd = remote_addr_fwd,
        meta = None if not meta else dumps(meta),
        cookies = None if not request.COOKIES else dumps(request.COOKIES),
        get = None if not request.GET else dumps(request.GET),
        post = dumps(request.POST),
        body = request.body,
        is_secure = request.is_secure(),
        is_ajax = request.is_ajax(),
        user = user
    )
    new.save()
    
    return new


@login_required
def index(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    user_agent_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__user_agent').order_by().annotate(total=Count('id'))

    for campaign in campaigns:
        campaign.views = App_hit.objects.filter(app_id__campaign=campaign).count()
        

    apps_count = App.objects.filter(campaign__agency=agency).count()

    views_count = App_hit.objects.filter(app__campaign__agency=agency).count()
    visitors_count = App_hit.objects.filter(app__campaign__agency=agency).values("remote_addr").distinct().count()

    
    ########################### Campaign Graph
    ###########################
    ###########################
    records = []
    leyends = []
    for campaign in campaigns:
        if campaign.views:
            records.append(campaign.views)
            leyends.append(campaign.name)
    
    
    chartdata_campaign_views = {'x': leyends, 'y': records}
    ###########################
    ########################### Campaign Views Graph
    

    ########################### Devices Graph
    ###########################
    ###########################

    leyends = []
    data = []
    mobile = 0
    tablet = 0
    pc = 0
    bot = 0
    unknown = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_mobile:
                    mobile = mobile + user_agent['total']
                elif key.is_tablet:
                    tablet = tablet + user_agent['total']
                elif key.is_pc:
                    pc = pc + user_agent['total']
                elif key.is_bot:
                    bot = bot + user_agent['total']
                else:
                    unknown = unknown + user_agent['total']
            else:
                unknown = unknown + user_agent['total']
        
        if mobile:
            leyends.append("Móvil")
            data.append(mobile)
        if tablet:
            leyends.append("Tablet")
            data.append(tablet)
        if pc:
            leyends.append("PC")
            data.append(pc)
        if bot:
            leyends.append("Bots")
            data.append(bot)
        if unknown:
            leyends.append("Desconocido")
            data.append(unknown)            
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_devices = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Devices Graph
    
    ########################### Source Graph
    ###########################
    ###########################
    sources = App_hit.objects.filter(app__campaign__agency=agency).values('source__name').annotate(total=Count('id'))
    
    xdata = []
    ydata = []
    if sources:
        for source in sources:            
            if source in xdata:
                ydata[xdata.index(source)] = int(ydata[xdata.index(source)]) + int(source["total"])                
            else:
                xdata.append(source["source__name"])
                ydata.append(int(source["total"]))
    else:
        xdata = ['Ninguna']
        ydata = [0]     


#    for data in xdata:    
#        source_name = App_source.objects.get(app__campaign__agency=agency, id=data["source"])
#        data["source"] = source_name.name

    chartdata_source = {'x': xdata, 'y': ydata}

    ###########################
    ########################### Source Graph


    ########################### Secure Connection Graph
    ###########################
    ###########################
    leyends = []
    data = []
    secure = App_hit.objects.filter(hit__is_secure=True, app__campaign__agency=agency).count()
    if secure:
        leyends.append("Utilizada")
        data.append(secure)
    if views_count - secure > 0:
        leyends.append("No utilizada")
        data.append(views_count - secure)
        
    chartdata_secure = {'x': leyends, 'y': data}
    ###########################
    ########################### Secure Connection Graph
    
    
    context = {
        'apps_count': apps_count,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'records': records,
        'campaigns': campaigns,
        'chartdata_campaign_views': chartdata_campaign_views,
        'chartdata_devices': chartdata_devices,
        'chartdata_source': chartdata_source,
        'chartdata_secure': chartdata_secure,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/index.html', context, context_instance=RequestContext(request))

@login_required
def environment(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    user_agent_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__user_agent').order_by().annotate(total=Count('id'))

    for campaign in campaigns:
#        fanpage = graph.get(campaign.facebook_page_id)
#        campaign.likes = fanpage['likes']
#        campaign.talking_about_count = fanpage['talking_about_count']
#        apps = App.objects.filter(campaign_id=campaign).all()
#        campaign.apps = apps
        campaign.views = App_hit.objects.filter(app_id__campaign=campaign).count()
        

    ########################### OS Graph
    ###########################
    ###########################    
    user_agents = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.os.family] = user_agent['total'] if not key.os.family in user_agents else user_agents[key.os.family] + user_agent['total']
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0] 

    chartdata_os = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Os Graph

    apps_count = App.objects.filter(campaign__agency=agency).count()

    ########################### Browser Graph
    ###########################
    ###########################    
    user_agents = {};
    user_agents_versions = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.browser.family] = user_agent['total'] if not key.browser.family in user_agents else user_agents[key.browser.family] + user_agent['total']
                try:
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total']
                except:
                    user_agents_versions[key.browser.family] = {}# if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string]
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total'] 
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']                
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
                
    else:
        xdata = ['Ninguno']   
        ydata = [0]         
        

    chartdata_browsers = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Browser Graph

    ########################### Chrome Graph
    ###########################
    ###########################
    xdata = []
    ydata = []
    
    if "Chrome" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Chrome'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     
        
    chartdata_chrome = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Chrome Graph

    
    ########################### Firefox Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Firefox" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Firefox'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_firefox = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Firefox Graph
    
    
    ########################### Safari Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Safari" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Safari'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_safari = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Safari Graph


    ########################### IE Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "IE" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['IE'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_ie = {'x': xdata, 'y': ydata}
    ###########################
    ########################### IE Graph
    
    context = {
        'apps_count': apps_count,
        'user_agents': user_agents,
        'campaigns': campaigns,
        'chartdata_os': chartdata_os,
        'chartdata_browsers': chartdata_browsers,
        'chartdata_chrome': chartdata_chrome,
        'chartdata_firefox': chartdata_firefox,
        'chartdata_safari': chartdata_safari,
        'chartdata_ie': chartdata_ie,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/environment.html', context, context_instance=RequestContext(request))


@login_required
def system(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()

    for campaign in campaigns:
#        fanpage = graph.get(campaign.facebook_page_id)
#        campaign.likes = fanpage['likes']
#        campaign.talking_about_count = fanpage['talking_about_count']
#        apps = App.objects.filter(campaign_id=campaign).all()
#        campaign.apps = apps
        campaign.views = App_hit.objects.filter(app_id__campaign=campaign).count()


    apps_count = App.objects.filter(campaign__agency=agency).count()

    views_count = App_hit.objects.filter(app__campaign__agency=agency).count()

    hits = App_hit.objects.filter(app__campaign__agency=agency).all()    
        
    resolutions = App_hit.objects.filter(app__campaign__agency=agency).values('hit__screen_width','hit__screen_height').order_by('hit__screen_width', 'hit__screen_height').annotate(total=Count('id'))

    ########################### Resolution Graph
    ###########################
    ###########################
    leyends = []
    data = []
    resolutions_dict = {}
    sorted_resolutions = {}
    if resolutions:
        for resolution in resolutions:
#            leyends.append(str(resolution["hit__screen_width"]) + "x" + str(resolution["hit__screen_height"]))
#            data.append(resolution["total"])
            resolutions_dict[str(resolution["hit__screen_width"]) + "x" + str(resolution["hit__screen_height"])] = resolution["total"]

        result = limit_results_dict(resolutions_dict, 5)
        leyends = result["xdata"]   
        data = result["ydata"]                 

        sorted_resolutions = result["dict"]

    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_resolution = {'x': leyends, 'y': data}
    ###########################
    ########################### Resolution Graph
    

    ########################### Touch Graph
    ###########################
    ###########################
    
    user_agent_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__user_agent').order_by().annotate(total=Count('id'))    

    leyends = []
    data = []
    touch = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_touch_capable:
                    touch = touch + user_agent['total']
        
        if touch:
            leyends.append("Disponible")
            data.append(touch)
        
        if views_count - touch > 0:
            leyends.append("No disponible")
            data.append(views_count - touch)
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_touch = {'x': leyends, 'y': data}
    ###########################
    ########################### Touch Graph


    ########################### Java Graph
    ###########################
    ###########################
    leyends = []
    data = []
    java = App_hit.objects.filter(hit__java=True, app__campaign__agency=agency).count()
    if java:
        leyends.append("Disponible")
        data.append(java)
    if views_count - java > 0:
        leyends.append("No disponible")
        data.append(views_count - java)
        
    chartdata_java = {'x': leyends, 'y': data}
    ###########################
    ########################### Java Graph


    silverlight_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__silverlight').order_by().annotate(total=Count('id'))    
    ########################### Silverlight Graph
    ###########################
    ###########################
    leyends = []
    data = []
    silverlight_versions = {}
    if silverlight_list:
        for silverlight in silverlight_list:
            silverlight_versions[str(silverlight['hit__silverlight'])] = silverlight['total'] if not str(silverlight['hit__silverlight']) in silverlight_versions else silverlight_versions[str(silverlight['hit__silverlight'])] + silverlight['total']
        
        result = limit_results_dict(silverlight_versions, 5)
        leyends = result["xdata"]   
        data = result["ydata"]                 
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_silverlight = {'x': leyends, 'y': data}
    ###########################
    ########################### Silverlight Graph
    

    color_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__color').order_by().annotate(total=Count('id'))    
    ########################### Color Graph
    ###########################
    ###########################
    leyends = []
    data = []
    colors = {}
    if color_list:
        for color in color_list:
            colors[str(color['hit__color']) + " bits"] = color['total'] if not str(color['hit__color']) + " bits" in colors else colors[str(color['hit__color']) + " bits"] + color['total']
        
        result = limit_results_dict(colors, 5)
        leyends = result["xdata"]   
        data = result["ydata"]            

#        for color in colors:
#            if str(color) == "None bits":
#                leyends.append("Desconocido")
#            else:
#                leyends.append(str(color))
#            data.append(colors[color])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_color = {'x': leyends, 'y': data}
    ###########################
    ########################### Color Graph
    

    flash_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__flash').order_by().annotate(total=Count('id'))    
    ########################### Flash Graph
    ###########################
    ###########################
    leyends = []
    data = []
    flash_versions = {}
    if flash_list:
        for flash in flash_list:
            flash_versions[str(flash['hit__flash'])] = flash['total'] if not str(flash['hit__flash']) in flash_versions else flash_versions[str(flash['hit__flash'])] + flash['total']
        
        result = limit_results_dict(flash_versions, 5)
        leyends = result["xdata"]   
        data = result["ydata"]            
#        for flash_version in flash_versions:
#            if str(flash_version) == "None":
#                leyends.append("No disponible")
#            else:
#                leyends.append(str(flash_version))
#            data.append(flash_versions[flash_version])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_flash = {'x': leyends, 'y': data}
    ###########################
    ########################### Flash Graph
    
    context = {
        'apps_count': apps_count,
        'sorted_resolutions': sorted_resolutions,
        'campaigns': campaigns,
        'chartdata_touch': chartdata_touch,
        'chartdata_resolution': chartdata_resolution,
        'chartdata_silverlight': chartdata_silverlight,
        'chartdata_color': chartdata_color,
        'chartdata_java': chartdata_java,
        'chartdata_flash': chartdata_flash,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/system.html', context, context_instance=RequestContext(request))


@login_required
def advanced(request):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    for campaign in campaigns:
        campaign.views = App_hit.objects.filter(app_id__campaign=campaign).count()
        

    apps_count = App.objects.filter(campaign__agency=agency).count()
    views_count = App_hit.objects.filter(app__campaign__agency=agency).count()

    webgl_count = App_hit.objects.filter(app__campaign__agency=agency, hit__webgl=True).count()
    svg_count = App_hit.objects.filter(app__campaign__agency=agency, hit__svg=True).count()
    canvas_count = App_hit.objects.filter(app__campaign__agency=agency, hit__html5_canvas=True).count()   
    audio_count = App_hit.objects.filter(app__campaign__agency=agency, hit__html5_audio=True).count() 
    video_count = App_hit.objects.filter(app__campaign__agency=agency, hit__html5_video=True).count()


    ########################### Canvas Graph
    ###########################
    ###########################
    leyends = []
    data = []
    canvas = App_hit.objects.filter(hit__html5_canvas=True, app__campaign__agency=agency).count()
    if canvas:
        leyends.append("Disponible")
        data.append(canvas)
    if views_count - canvas > 0:
        leyends.append("No disponible")
        data.append(views_count - canvas)
        
    chartdata_canvas = {'x': leyends, 'y': data}
    ###########################
    ########################### Canvas Graph


    ########################### Video Graph
    ###########################
    ###########################
    leyends = []
    data = []
    video = App_hit.objects.filter(hit__html5_video=True, app__campaign__agency=agency).count()
    if video:
        leyends.append("Disponible")
        data.append(video)
    if views_count - video > 0:
        leyends.append("No disponible")
        data.append(views_count - video)
        
    chartdata_video = {'x': leyends, 'y': data}
    ###########################
    ########################### Video Graph


    ########################### Audio Graph
    ###########################
    ###########################
    leyends = []
    data = []
    audio = App_hit.objects.filter(hit__html5_audio=True, app__campaign__agency=agency).count()
    if audio:
        leyends.append("Disponible")
        data.append(audio)
    if views_count - audio > 0:
        leyends.append("No disponible")
        data.append(views_count - audio)
        
    chartdata_audio = {'x': leyends, 'y': data}
    ###########################
    ########################### Audio Graph


    ########################### Storage Graph
    ###########################
    ###########################
    leyends = []
    data = []
    storage = App_hit.objects.filter(hit__html5_storage=True, app__campaign__agency=agency).count()
    if storage:
        leyends.append("Disponible")
        data.append(storage)
    if views_count - storage > 0:
        leyends.append("No disponible")
        data.append(views_count - storage)
        
    chartdata_storage = {'x': leyends, 'y': data}
    ###########################
    ########################### Storage Graph


    ########################### WebGL Graph
    ###########################
    ###########################
    leyends = []
    data = []
    webgl = App_hit.objects.filter(hit__webgl=True, app__campaign__agency=agency).count()
    if webgl:
        leyends.append("Disponible")
        data.append(webgl)
    if views_count - webgl > 0:
        leyends.append("No disponible")
        data.append(views_count - webgl)
        
    chartdata_webgl = {'x': leyends, 'y': data}
    ###########################
    ########################### WebGL Graph    


    ########################### SVG Graph
    ###########################
    ###########################
    leyends = []
    data = []
    svg = App_hit.objects.filter(hit__svg=True, app__campaign__agency=agency).count()
    if svg:
        leyends.append("Disponible")
        data.append(svg)
    if views_count - svg > 0:
        leyends.append("No disponible")
        data.append(views_count - svg)
        
    chartdata_svg = {'x': leyends, 'y': data}
    ###########################
    ########################### SVG Graph

        
    context = {
        'apps_count': apps_count,
        'webgl_count': webgl_count,
        'svg_count': svg_count,
        'canvas_count': canvas_count,
        'audio_count': audio_count,
        'video_count': video_count,
        'campaigns': campaigns,
        'chartdata_canvas': chartdata_canvas,
        'chartdata_video': chartdata_video,
        'chartdata_audio': chartdata_audio,
        'chartdata_storage': chartdata_storage,
        'chartdata_webgl': chartdata_webgl,
        'chartdata_svg': chartdata_svg,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/advanced.html', context, context_instance=RequestContext(request))


@login_required
def campaign(request, campaign_id):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()
    
     
    user_agent_list = App_hit.objects.filter(app__campaign=campaign).values('hit__user_agent').order_by().annotate(total=Count('id'))


    apps_count = App.objects.filter(campaign=campaign).count()

    views_count = App_hit.objects.filter(app__campaign=campaign).count()
    visitors_count = App_hit.objects.filter(app__campaign=campaign).values("remote_addr").distinct().count()



    
    ########################### Apps Graph
    ###########################
    ###########################
    records = []
    leyends = []
    for app in active_apps:
        app.records = App_hit.objects.filter(app__campaign=campaign, app=app).count()
        if app.records:
            records.append(app.records)
            leyends.append(app.name)
    
    chartdata_apps_views = {'x': leyends, 'y': records}
    ###########################
    ########################### Apps Views Graph
    

    ########################### Devices Graph
    ###########################
    ###########################

    leyends = []
    data = []
    mobile = 0
    tablet = 0
    pc = 0
    bot = 0
    unknown = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_mobile:
                    mobile = mobile + user_agent['total']
                elif key.is_tablet:
                    tablet = tablet + user_agent['total']
                elif key.is_pc:
                    pc = pc + user_agent['total']
                elif key.is_bot:
                    bot = bot + user_agent['total']
                else:
                    unknown = unknown + user_agent['total']
            else:
                unknown = unknown + user_agent['total']
        
        if mobile:
            leyends.append("Móvil")
            data.append(mobile)
        if tablet:
            leyends.append("Tablet")
            data.append(tablet)
        if pc:
            leyends.append("PC")
            data.append(pc)
        if bot:
            leyends.append("Bots")
            data.append(bot)
        if unknown:
            leyends.append("Desconocido")
            data.append(unknown)            
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_devices = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Devices Graph
    
    ########################### Source Graph
    ###########################
    ###########################
    sources = App_hit.objects.filter(app__campaign=campaign).values('source__name').annotate(total=Count('id'))
    
    xdata = []
    ydata = []
    if sources:
        for source in sources:            
            if source in xdata:
                ydata[xdata.index(source)] = int(ydata[xdata.index(source)]) + int(source["total"])                
            else:
                xdata.append(source["source__name"])
                ydata.append(int(source["total"]))
    else:
        xdata = ['Ninguna']
        ydata = [0]     

    chartdata_source = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Source Graph


    ########################### Secure Connection Graph
    ###########################
    ###########################
    leyends = []
    data = []
    secure = App_hit.objects.filter(hit__is_secure=True, app__campaign=campaign).count()
    if secure:
        leyends.append("Utilizada")
        data.append(secure)
    if views_count - secure > 0:
        leyends.append("No utilizada")
        data.append(views_count - secure)
        
    chartdata_secure = {'x': leyends, 'y': data}
    ###########################
    ########################### Secure Connection Graph
    
    
    context = {
        'apps_count': apps_count,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'campaign': campaign,
        'records': records,
        'active_apps': active_apps,
        'inactive_apps': inactive_apps,
        'chartdata_apps_views': chartdata_apps_views,
        'chartdata_devices': chartdata_devices,
        'chartdata_source': chartdata_source,
        'chartdata_secure': chartdata_secure,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/campaign.html', context, context_instance=RequestContext(request))

@login_required
def campaign_environment(request, campaign_id):
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()
    
    user_agent_list = App_hit.objects.filter(app__campaign=campaign).values('hit__user_agent').order_by().annotate(total=Count('id'))


    ########################### OS Graph
    ###########################
    ###########################    
    user_agents = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.os.family] = user_agent['total'] if not key.os.family in user_agents else user_agents[key.os.family] + user_agent['total']
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0] 

    chartdata_os = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Os Graph

    apps_count = App.objects.filter(campaign__agency=agency).count()

    ########################### Browser Graph
    ###########################
    ###########################    
    user_agents = {};
    user_agents_versions = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.browser.family] = user_agent['total'] if not key.browser.family in user_agents else user_agents[key.browser.family] + user_agent['total']
                try:
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total']
                except:
                    user_agents_versions[key.browser.family] = {}# if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string]
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total'] 
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']                
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
                
    else:
        xdata = ['Ninguno']   
        ydata = [0]         
        

    chartdata_browsers = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Browser Graph

    ########################### Chrome Graph
    ###########################
    ###########################
    xdata = []
    ydata = []
    
    if "Chrome" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Chrome'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     
        
    chartdata_chrome = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Chrome Graph

    
    ########################### Firefox Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Firefox" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Firefox'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_firefox = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Firefox Graph
    
    
    ########################### Safari Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Safari" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Safari'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_safari = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Safari Graph


    ########################### IE Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "IE" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['IE'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_ie = {'x': xdata, 'y': ydata}
    ###########################
    ########################### IE Graph

    
    context = {
        'apps_count': apps_count,
        'user_agents': user_agents,
        'active_apps': active_apps,
        'inactive_apps': inactive_apps,
        'campaign': campaign,
        'chartdata_os': chartdata_os,
        'chartdata_browsers': chartdata_browsers,
        'chartdata_chrome': chartdata_chrome,
        'chartdata_firefox': chartdata_firefox,
        'chartdata_safari': chartdata_safari,
        'chartdata_ie': chartdata_ie,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/campaign_environment.html', context, context_instance=RequestContext(request))


@login_required
def campaign_system(request, campaign_id):    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()


    apps_count = App.objects.filter(campaign=campaign).count()

    views_count = App_hit.objects.filter(app__campaign=campaign).count()

    hits = App_hit.objects.filter(app__campaign=campaign).all()    
        

    ########################### Resolution Graph
    ###########################
    ###########################
    leyends = []
    data = []
    resolutions = {}
    if hits:
        for hit in hits:
            resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] = 1 if not str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height) in resolutions else resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] + 1
        
        for resolution in resolutions:
            if resolution == "NonexNone":
                leyends.append("Desconocida")
            else:
                leyends.append(resolution)
            data.append(resolutions[resolution])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_resolution = {'x': leyends, 'y': data}
    ###########################
    ########################### Resolution Graph

    sorted_resolutions = dict(sorted(resolutions.iteritems(), key=itemgetter(1), reverse=True)[:5])


    
    ########################### Touch Graph
    ###########################
    ###########################
    
    user_agent_list = App_hit.objects.filter(app__campaign=campaign).values('hit__user_agent').order_by().annotate(total=Count('id'))    

    leyends = []
    data = []
    touch = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_touch_capable:
                    touch = touch + user_agent['total']
        
        if touch:
            leyends.append("Disponible")
            data.append(touch)
        
        if views_count - touch > 0:
            leyends.append("No disponible")
            data.append(views_count - touch)
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_touch = {'x': leyends, 'y': data}
    ###########################
    ########################### Touch Graph



    ########################### Java Graph
    ###########################
    ###########################
    leyends = []
    data = []
    java = App_hit.objects.filter(hit__java=True, app__campaign=campaign).count()
    if java:
        leyends.append("Disponible")
        data.append(java)
    if views_count - java > 0:
        leyends.append("No disponible")
        data.append(views_count - java)
        
    chartdata_java = {'x': leyends, 'y': data}
    ###########################
    ########################### Java Graph


    ########################### Silverlight Graph
    ###########################
    ###########################
    leyends = []
    data = []
    silverlight_versions = {}
    if hits:
        for hit in hits:
            silverlight_versions[str(hit.hit.silverlight)] = 1 if not str(hit.hit.silverlight) in silverlight_versions else silverlight_versions[str(hit.hit.silverlight)] + 1
        
        for silverlight_version in silverlight_versions:
            if str(silverlight_version) == "None":
                leyends.append("No disponible")
            else:
                leyends.append(str(silverlight_version))
            data.append(silverlight_versions[silverlight_version])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_silverlight = {'x': leyends, 'y': data}
    ###########################
    ########################### Silverlight Graph
    

    ########################### Color Graph
    ###########################
    ###########################
    leyends = []
    data = []
    colors = {}
    if hits:
        for hit in hits:
            colors[str(hit.hit.color) + " bits"] = 1 if not str(hit.hit.color) + " bits" in colors else colors[str(hit.hit.color) + " bits"] + 1
        
        for color in colors:
            if str(color) == "None bits":
                leyends.append("Desconocido")
            else:
                leyends.append(str(color))
            data.append(colors[color])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_color = {'x': leyends, 'y': data}
    ###########################
    ########################### Color Graph
    

    ########################### Flash Graph
    ###########################
    ###########################
    leyends = []
    data = []
    flash_versions = {}
    if hits:
        for hit in hits:
            flash_versions[str(hit.hit.flash)] = 1 if not str(hit.hit.flash) in flash_versions else flash_versions[str(hit.hit.flash)] + 1
        
        for flash_version in flash_versions:
            if str(flash_version) == "None":
                leyends.append("No disponible")
            else:
                leyends.append(str(flash_version))
            data.append(flash_versions[flash_version])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_flash = {'x': leyends, 'y': data}
    ###########################
    ########################### Flash Graph
    
    context = {
        'apps_count': apps_count,
        'sorted_resolutions': sorted_resolutions,
        'campaign': campaign,
        'active_apps': active_apps,
        'inactive_apps': inactive_apps,
        'chartdata_touch': chartdata_touch,
        'chartdata_resolution': chartdata_resolution,
        'chartdata_silverlight': chartdata_silverlight,
        'chartdata_color': chartdata_color,
        'chartdata_java': chartdata_java,
        'chartdata_flash': chartdata_flash,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/campaign_system.html', context, context_instance=RequestContext(request))


@login_required
def campaign_advanced(request, campaign_id):
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
    

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()
        
    apps_count = App.objects.filter(campaign=campaign).count()
    views_count = App_hit.objects.filter(app__campaign=campaign).count()

    webgl_count = App_hit.objects.filter(app__campaign=campaign, hit__webgl=True).count()
    svg_count = App_hit.objects.filter(app__campaign=campaign, hit__svg=True).count()
    canvas_count = App_hit.objects.filter(app__campaign=campaign, hit__html5_canvas=True).count()   
    audio_count = App_hit.objects.filter(app__campaign=campaign, hit__html5_audio=True).count() 
    video_count = App_hit.objects.filter(app__campaign=campaign, hit__html5_video=True).count()


    ########################### Canvas Graph
    ###########################
    ###########################
    leyends = []
    data = []
    canvas = App_hit.objects.filter(hit__html5_canvas=True, app__campaign=campaign).count()
    if canvas:
        leyends.append("Disponible")
        data.append(canvas)
    if views_count - canvas > 0:
        leyends.append("No disponible")
        data.append(views_count - canvas)
        
    chartdata_canvas = {'x': leyends, 'y': data}
    ###########################
    ########################### Canvas Graph


    ########################### Video Graph
    ###########################
    ###########################
    leyends = []
    data = []
    video = App_hit.objects.filter(hit__html5_video=True, app__campaign=campaign).count()
    if video:
        leyends.append("Disponible")
        data.append(video)
    if views_count - video > 0:
        leyends.append("No disponible")
        data.append(views_count - video)
        
    chartdata_video = {'x': leyends, 'y': data}
    ###########################
    ########################### Video Graph


    ########################### Audio Graph
    ###########################
    ###########################
    leyends = []
    data = []
    audio = App_hit.objects.filter(hit__html5_audio=True, app__campaign=campaign).count()
    if audio:
        leyends.append("Disponible")
        data.append(audio)
    if views_count - audio > 0:
        leyends.append("No disponible")
        data.append(views_count - audio)
        
    chartdata_audio = {'x': leyends, 'y': data}
    ###########################
    ########################### Audio Graph


    ########################### Storage Graph
    ###########################
    ###########################
    leyends = []
    data = []
    storage = App_hit.objects.filter(hit__html5_storage=True, app__campaign=campaign).count()
    if storage:
        leyends.append("Disponible")
        data.append(storage)
    if views_count - storage > 0:
        leyends.append("No disponible")
        data.append(views_count - storage)
        
    chartdata_storage = {'x': leyends, 'y': data}
    ###########################
    ########################### Storage Graph


    ########################### WebGL Graph
    ###########################
    ###########################
    leyends = []
    data = []
    webgl = App_hit.objects.filter(hit__webgl=True, app__campaign=campaign).count()
    if webgl:
        leyends.append("Disponible")
        data.append(webgl)
    if views_count - webgl > 0:
        leyends.append("No disponible")
        data.append(views_count - webgl)
        
    chartdata_webgl = {'x': leyends, 'y': data}
    ###########################
    ########################### WebGL Graph    


    ########################### SVG Graph
    ###########################
    ###########################
    leyends = []
    data = []
    svg = App_hit.objects.filter(hit__svg=True, app__campaign=campaign).count()
    if svg:
        leyends.append("Disponible")
        data.append(svg)
    if views_count - svg > 0:
        leyends.append("No disponible")
        data.append(views_count - svg)
        
    chartdata_svg = {'x': leyends, 'y': data}
    ###########################
    ########################### SVG Graph

        
    context = {
        'apps_count': apps_count,
        'webgl_count': webgl_count,
        'svg_count': svg_count,
        'canvas_count': canvas_count,
        'audio_count': audio_count,
        'video_count': video_count,
        'campaign': campaign,
        'active_apps': active_apps,
        'inactive_apps': inactive_apps,
        'chartdata_canvas': chartdata_canvas,
        'chartdata_video': chartdata_video,
        'chartdata_audio': chartdata_audio,
        'chartdata_storage': chartdata_storage,
        'chartdata_webgl': chartdata_webgl,
        'chartdata_svg': chartdata_svg,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/campaign_advanced.html', context, context_instance=RequestContext(request))


@login_required
def app(request, app_id):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
     
    user_agent_list = App_hit.objects.filter(app=app).values('hit__user_agent').order_by().annotate(total=Count('id'))


    views_count = App_hit.objects.filter(app=app).count()
    visitors_count = App_hit.objects.filter(app=app).values("remote_addr").distinct().count()

    
#    print >>sys.stderr, chartdata_hits
        

    ########################### Devices Graph
    ###########################
    ###########################

    leyends = []
    data = []
    mobile = 0
    tablet = 0
    pc = 0
    bot = 0
    unknown = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_mobile:
                    mobile = mobile + user_agent['total']
                elif key.is_tablet:
                    tablet = tablet + user_agent['total']
                elif key.is_pc:
                    pc = pc + user_agent['total']
                elif key.is_bot:
                    bot = bot + user_agent['total']
                else:
                    unknown = unknown + user_agent['total']
            else:
                unknown = unknown + user_agent['total']
        
        if mobile:
            leyends.append("Móvil")
            data.append(mobile)
        if tablet:
            leyends.append("Tablet")
            data.append(tablet)
        if pc:
            leyends.append("PC")
            data.append(pc)
        if bot:
            leyends.append("Bots")
            data.append(bot)
        if unknown:
            leyends.append("Desconocido")
            data.append(unknown)            
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_devices = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Devices Graph
    
    ########################### Source Graph
    ###########################
    ###########################
    sources = App_hit.objects.filter(app=app).values('source__name').annotate(total=Count('id'))
    
    xdata = []
    ydata = []
    if sources:
        for source in sources:            
            if source in xdata:
                ydata[xdata.index(source)] = int(ydata[xdata.index(source)]) + int(source["total"])                
            else:
                xdata.append(source["source__name"])
                ydata.append(int(source["total"]))
    else:
        xdata = ['Ninguna']
        ydata = [0]     

    chartdata_source = {'x': xdata, 'y': ydata}

    ###########################
    ########################### Source Graph


    ########################### Secure Connection Graph
    ###########################
    ###########################
    leyends = []
    data = []
    secure = App_hit.objects.filter(hit__is_secure=True, app=app).count()
    if secure:
        leyends.append("Utilizada")
        data.append(secure)
    if views_count - secure > 0:
        leyends.append("No utilizada")
        data.append(views_count - secure)
        
    chartdata_secure = {'x': leyends, 'y': data}
    ###########################
    ########################### Secure Connection Graph
    
    
    context = {
        'app': app,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'campaign': app.campaign,
        'chartdata_devices': chartdata_devices,
        'chartdata_source': chartdata_source,
        'chartdata_secure': chartdata_secure,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/app.html', context, context_instance=RequestContext(request))

@login_required
def app_environment(request, app_id):    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    user_agent_list = App_hit.objects.filter(app=app).values('hit__user_agent').order_by().annotate(total=Count('id'))
       

    ########################### OS Graph
    ###########################
    ###########################    
    user_agents = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.os.family] = user_agent['total'] if not key.os.family in user_agents else user_agents[key.os.family] + user_agent['total']
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0] 

    chartdata_os = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Os Graph


    apps_count = App.objects.filter(campaign__agency=agency).count()

    ########################### Browser Graph
    ###########################
    ###########################    
    user_agents = {};
    user_agents_versions = {};
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                user_agents[key.browser.family] = user_agent['total'] if not key.browser.family in user_agents else user_agents[key.browser.family] + user_agent['total']
                try:
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total']
                except:
                    user_agents_versions[key.browser.family] = {}# if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string]
                    user_agents_versions[key.browser.family][key.browser.version_string] = user_agent['total'] if not key.browser.version_string in user_agents_versions[key.browser.family] else user_agents_versions[key.browser.family][key.browser.version_string] + user_agent['total'] 
            else:
                user_agents['other'] = user_agent['total'] if not 'other' in user_agents else user_agents['other'] + user_agent['total']                
                
        data = limit_results_dict(user_agents, 5)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
                
    else:
        xdata = ['Ninguno']   
        ydata = [0]         
        

    chartdata_browsers = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Browser Graph

    ########################### Chrome Graph
    ###########################
    ###########################
    xdata = []
    ydata = []
    
    if "Chrome" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Chrome'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     
        
    chartdata_chrome = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Chrome Graph

    
    ########################### Firefox Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Firefox" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Firefox'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_firefox = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Firefox Graph
    
    
    ########################### Safari Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "Safari" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['Safari'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_safari = {'x': xdata, 'y': ydata}
    ###########################
    ########################### Safari Graph


    ########################### IE Graph
    ###########################
    ###########################
    xdata = []
    ydata = [] 
    if "IE" in user_agents_versions:
        data = limit_results_dict(user_agents_versions['IE'], 3)
        xdata = data["xdata"]   
        ydata = data["ydata"]                 
    else:
        xdata = ['Ninguno']   
        ydata = [0]     

    chartdata_ie = {'x': xdata, 'y': ydata}
    ###########################
    ########################### IE Graph

    
    context = {
        'app': app,
        'apps_count': apps_count,
        'user_agents': user_agents,
        'campaign': app.campaign,
        'chartdata_os': chartdata_os,
        'chartdata_browsers': chartdata_browsers,
        'chartdata_chrome': chartdata_chrome,
        'chartdata_firefox': chartdata_firefox,
        'chartdata_safari': chartdata_safari,
        'chartdata_ie': chartdata_ie,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/app_environment.html', context, context_instance=RequestContext(request))


@login_required
def app_system(request, app_id):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    views_count = App_hit.objects.filter(app=app).count()

    hits = App_hit.objects.filter(app=app).all()    
        

    ########################### Resolution Graph
    ###########################
    ###########################
    leyends = []
    data = []
    resolutions = {}
    if hits:
        for hit in hits:
            resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] = 1 if not str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height) in resolutions else resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] + 1
        
        for resolution in resolutions:
            if resolution == "NonexNone":
                leyends.append("Desconocida")
            else:
                leyends.append(resolution)
            data.append(resolutions[resolution])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_resolution = {'x': leyends, 'y': data}
    ###########################
    ########################### Resolution Graph

    sorted_resolutions = dict(sorted(resolutions.iteritems(), key=itemgetter(1), reverse=True)[:5])



    
    ########################### Touch Graph
    ###########################
    ###########################
    
    user_agent_list = App_hit.objects.filter(app=app).values('hit__user_agent').order_by().annotate(total=Count('id'))    

    leyends = []
    data = []
    touch = 0
    if user_agent_list:
        for user_agent in user_agent_list:
            if user_agent['hit__user_agent']:
                key = parse(user_agent['hit__user_agent'])
                if key.is_touch_capable:
                    touch = touch + user_agent['total']
        
        if touch:
            leyends.append("Disponible")
            data.append(touch)
        
        if views_count - touch > 0:
            leyends.append("No disponible")
            data.append(views_count - touch)
    else:
        leyends = ['Ninguno']   
        data = [0]

    chartdata_touch = {'x': leyends, 'y': data}
    ###########################
    ########################### Touch Graph


    ########################### Java Graph
    ###########################
    ###########################
    leyends = []
    data = []
    java = App_hit.objects.filter(hit__java=True, app=app).count()
    if java:
        leyends.append("Disponible")
        data.append(java)
    if views_count - java > 0:
        leyends.append("No disponible")
        data.append(views_count - java)
        
    chartdata_java = {'x': leyends, 'y': data}
    ###########################
    ########################### Java Graph


    ########################### Silverlight Graph
    ###########################
    ###########################
    leyends = []
    data = []
    silverlight_versions = {}
    if hits:
        for hit in hits:
            silverlight_versions[str(hit.hit.silverlight)] = 1 if not str(hit.hit.silverlight) in silverlight_versions else silverlight_versions[str(hit.hit.silverlight)] + 1
        
        for silverlight_version in silverlight_versions:
            if str(silverlight_version) == "None":
                leyends.append("No disponible")
            else:
                leyends.append(str(silverlight_version))
            data.append(silverlight_versions[silverlight_version])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_silverlight = {'x': leyends, 'y': data}
    ###########################
    ########################### Silverlight Graph
    

    ########################### Color Graph
    ###########################
    ###########################
    leyends = []
    data = []
    colors = {}
    if hits:
        for hit in hits:
            colors[str(hit.hit.color) + " bits"] = 1 if not str(hit.hit.color) + " bits" in colors else colors[str(hit.hit.color) + " bits"] + 1
        
        for color in colors:
            if str(color) == "None bits":
                leyends.append("Desconocido")
            else:
                leyends.append(str(color))
            data.append(colors[color])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_color = {'x': leyends, 'y': data}
    ###########################
    ########################### Color Graph
    

    ########################### Flash Graph
    ###########################
    ###########################
    leyends = []
    data = []
    flash_versions = {}
    if hits:
        for hit in hits:
            flash_versions[str(hit.hit.flash)] = 1 if not str(hit.hit.flash) in flash_versions else flash_versions[str(hit.hit.flash)] + 1
        
        for flash_version in flash_versions:
            if str(flash_version) == "None":
                leyends.append("No disponible")
            else:
                leyends.append(str(flash_version))
            data.append(flash_versions[flash_version])
    else:
        leyends = ['Ninguna']   
        data = [0]

    chartdata_flash = {'x': leyends, 'y': data}
    ###########################
    ########################### Flash Graph
    
    context = {
        'app': app,
        'sorted_resolutions': sorted_resolutions,
        'campaign': app.campaign,
        'chartdata_touch': chartdata_touch,
        'chartdata_resolution': chartdata_resolution,
        'chartdata_silverlight': chartdata_silverlight,
        'chartdata_color': chartdata_color,
        'chartdata_java': chartdata_java,
        'chartdata_flash': chartdata_flash,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/app_system.html', context, context_instance=RequestContext(request))


@login_required
def app_advanced(request, app_id):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')   


    views_count = App_hit.objects.filter(app=app).count()

    webgl_count = App_hit.objects.filter(app=app, hit__webgl=True).count()
    svg_count = App_hit.objects.filter(app=app, hit__svg=True).count()
    canvas_count = App_hit.objects.filter(app=app, hit__html5_canvas=True).count()   
    audio_count = App_hit.objects.filter(app=app, hit__html5_audio=True).count() 
    video_count = App_hit.objects.filter(app=app, hit__html5_video=True).count()


    ########################### Canvas Graph
    ###########################
    ###########################
    leyends = []
    data = []
    canvas = App_hit.objects.filter(hit__html5_canvas=True, app=app).count()
    if canvas:
        leyends.append("Disponible")
        data.append(canvas)
    if views_count - canvas > 0:
        leyends.append("No disponible")
        data.append(views_count - canvas)
        
    chartdata_canvas = {'x': leyends, 'y': data}
    ###########################
    ########################### Canvas Graph


    ########################### Video Graph
    ###########################
    ###########################
    leyends = []
    data = []
    video = App_hit.objects.filter(hit__html5_video=True, app=app).count()
    if video:
        leyends.append("Disponible")
        data.append(video)
    if views_count - video > 0:
        leyends.append("No disponible")
        data.append(views_count - video)
        
    chartdata_video = {'x': leyends, 'y': data}
    ###########################
    ########################### Video Graph


    ########################### Audio Graph
    ###########################
    ###########################
    leyends = []
    data = []
    audio = App_hit.objects.filter(hit__html5_audio=True, app=app).count()
    if audio:
        leyends.append("Disponible")
        data.append(audio)
    if views_count - audio > 0:
        leyends.append("No disponible")
        data.append(views_count - audio)
        
    chartdata_audio = {'x': leyends, 'y': data}
    ###########################
    ########################### Audio Graph


    ########################### Storage Graph
    ###########################
    ###########################
    leyends = []
    data = []
    storage = App_hit.objects.filter(hit__html5_storage=True, app=app).count()
    if storage:
        leyends.append("Disponible")
        data.append(storage)
    if views_count - storage > 0:
        leyends.append("No disponible")
        data.append(views_count - storage)
        
    chartdata_storage = {'x': leyends, 'y': data}
    ###########################
    ########################### Storage Graph


    ########################### WebGL Graph
    ###########################
    ###########################
    leyends = []
    data = []
    webgl = App_hit.objects.filter(hit__webgl=True, app=app).count()
    if webgl:
        leyends.append("Disponible")
        data.append(webgl)
    if views_count - webgl > 0:
        leyends.append("No disponible")
        data.append(views_count - webgl)
        
    chartdata_webgl = {'x': leyends, 'y': data}
    ###########################
    ########################### WebGL Graph    


    ########################### SVG Graph
    ###########################
    ###########################
    leyends = []
    data = []
    svg = App_hit.objects.filter(hit__svg=True, app=app).count()
    if svg:
        leyends.append("Disponible")
        data.append(svg)
    if views_count - svg > 0:
        leyends.append("No disponible")
        data.append(views_count - svg)
        
    chartdata_svg = {'x': leyends, 'y': data}
    ###########################
    ########################### SVG Graph

        
    context = {
        'app': app,
        'webgl_count': webgl_count,
        'svg_count': svg_count,
        'canvas_count': canvas_count,
        'audio_count': audio_count,
        'video_count': video_count,
        'campaign': app.campaign,
        'chartdata_canvas': chartdata_canvas,
        'chartdata_video': chartdata_video,
        'chartdata_audio': chartdata_audio,
        'chartdata_storage': chartdata_storage,
        'chartdata_webgl': chartdata_webgl,
        'chartdata_svg': chartdata_svg,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }

    return render_to_response('stats/app_advanced.html', context, context_instance=RequestContext(request))
