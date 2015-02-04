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

import time
import random, sys
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from facepy import GraphAPI
from django.shortcuts import redirect
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.query import QuerySet
#from user_agents import parse

from facebook.decorators import facebook_access
from facebook.library import have_page_permission

from accounts.models import Campaign, Profile
from apps.models import App, App_hit, App_record
from records.models import Record
#from stats.models import Hit
#from stats.library import get_visits_number

@login_required
@facebook_access('manage_pages')
def index(request):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

#    print request.session.user
    print request.user.profile.facebook_id

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    for campaign in campaigns:
#        fanpage = graph.get(campaign.facebook_page_id)
#        campaign.likes = fanpage['likes']
#        campaign.talking_about_count = fanpage['talking_about_count']
#        apps = App.objects.filter(campaign_id=campaign).all()
#        campaign.apps = apps
        campaign.views = App_hit.objects.filter(app__campaign=campaign).count()
        campaign.fb_online = have_page_permission(request, campaign.facebook_page_id, 'EDIT_PROFILE')
        
    
    
    ########################### Campaign Views Graph
    ###########################
    ###########################
    views = []
    leyends = []
    for campaign in campaigns:
        if campaign.views:
            views.append(campaign.views)
            leyends.append(campaign.name)
    
#    print >> sys.stderr, views
    chartdata_campaign_views = {'x': leyends, 'y': views}
    ###########################
    ########################### Campaign Views Graph


    ########################### Campaign Records
    ###########################
    ###########################
    records = []
    leyends = []
    for campaign in campaigns:
        campaign.records = Record.objects.filter(campaign=campaign).count()
        if campaign.records:
            records.append(campaign.records)
            leyends.append(campaign.name)
    
    
    chartdata_campaign_records = {'x': leyends, 'y': records}
    
    ###########################
    ########################### Campaign Records
    

    ########################### Devices Graph
    ###########################
    ###########################
#    user_agent_list = App_hit.objects.filter(app__campaign__agency=agency).values('hit__user_agent')

#    leyends = []
#    data = []
#    mobile = 0
#    tablet = 0
#    pc = 0
#    bot = 0
#    unknown = 0
#    if user_agent_list:
#        for user_agent in user_agent_list:
#            try:
#                key = parse(user_agent['hit__user_agent'])
#                if key.is_mobile:
#                    mobile = mobile + 1
#                elif key.is_tablet:
#                    tablet = tablet + 1
#                elif key.is_pc:
#                    pc = pc + 1
#                elif key.is_bot:
##                    bot = bot + 1
#                else:
#                    unknown = unknown + 1
#            except:
#                unknown = unknown + 1
        
#        if mobile:
#            leyends.append("Móvil")
#            data.append(mobile)
##        if tablet:
#            leyends.append("Tablet")
#            data.append(tablet)
#        if pc:
#            leyends.append("PC")
#            data.append(pc)
#        if bot:
#            leyends.append("Bots")
#            data.append(bot)
#        if unknown:
#            leyends.append("Desconocido")
#            data.append(unknown)  
#            error = 1          
#    else:
#        leyends = ['Ninguno']   
#        data = [0]

#    chartdata_devices = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Devices Graph
    
    
#    ########################### Resolution Graph
#    ###########################
#    ###########################
#    hits = App_hit.objects.filter(app__campaign__agency=agency).all()#

#    leyends = []
#    data = []
#    resolutions = {}
#    if hits:
#        for hit in hits:
#            resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] = 1 if not str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height) in resolutions else resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] + 1
        
#        for resolution in resolutions:
#            if resolution == "NonexNone":
#                leyends.append("Desconocida")
#            else:
#                leyends.append(resolution)
#            data.append(resolutions[resolution])
#    else:
#        leyends = ['Ninguna']   
#        data = [0]

#    chartdata_resolution = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Resolution Graph
    
    
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
    
    return render_to_response('dashboard/index.html', context, context_instance=RequestContext(request))

    
@login_required
@facebook_access('read_insights')
def details(request, campaign_id=None):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    last_month = timezone.now() - timedelta(days=30)
    
    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        return redirect('/error/1001')
        
    if not have_page_permission(request, campaign.facebook_page_id, 'BASIC_ADMIN'):
        return redirect('/error/1507')


    apps_count = App.objects.filter(campaign=campaign).count()

    views_count = App_hit.objects.filter(app__campaign=campaign).count()
    visitors_count = App_hit.objects.filter(app__campaign=campaign).values("remote_addr").distinct().count()
    records_count = App_record.objects.filter(app__campaign=campaign).count()



    ########################### Facebook Graph
    ###########################
    ########################### Facebook
    
    graph = GraphAPI(request.session['facebook_access_token'])
    
    fanpage = graph.get(campaign.facebook_page_id)
    campaign.likes = fanpage['likes']
#    campaign.talking_about_count = fanpage['talking_about_count']  

    days=40
    last_month = datetime.today() - timedelta(days)
    last_month_timestamp = int(time.mktime(last_month.utctimetuple()))
        
    insights = graph.get(campaign.facebook_page_id+'/insights/page_fan_adds/?since='+str(last_month_timestamp))
    values = insights['data'][0]['values']
    
    campaign.likes_28_days = {}
    campaign.likes_28_days['value'] = 0
    campaign.likes_28_days['since'] = datetime.strptime(values[int(len(values)-28)]['end_time'], '%Y-%m-%dT%H:%M:%S+0000')
    campaign.likes_28_days['until'] = datetime.strptime(values[int(len(values)-1)]['end_time'], '%Y-%m-%dT%H:%M:%S+0000')
    
    campaign.likes_7_days = {}
    campaign.likes_7_days['value'] = 0
    campaign.likes_7_days['since'] = datetime.strptime(values[int(len(values)-7)]['end_time'], '%Y-%m-%dT%H:%M:%S+0000')
    campaign.likes_7_days['until'] = datetime.strptime(values[int(len(values)-1)]['end_time'], '%Y-%m-%dT%H:%M:%S+0000')

    campaign.likes_last_day = {}
    campaign.likes_last_day['value'] = values[int(len(values)-1)]['value']
    campaign.likes_last_day['date'] = datetime.strptime(values[int(len(values)-1)]['end_time'], '%Y-%m-%dT%H:%M:%S+0000')


    for i in range(1, 29):
        if i<=7:
            campaign.likes_7_days['value'] += values[int(len(values)-i)]['value']            
        campaign.likes_28_days['value'] += values[int(len(values)-i)]['value']
    
        
    leyends = []
    records = []
    if campaign.likes:
        records.append(campaign.likes)
        leyends.append("Total")
    if campaign.likes_28_days['value']:
        records.append(campaign.likes_28_days['value'])
        leyends.append("Últimos 28 días")
    if campaign.likes_7_days['value']:
        records.append(campaign.likes_7_days['value'])
        leyends.append("Últimos 7 días")
    if campaign.likes_last_day['value']:
        records.append(campaign.likes_last_day['value'])
        leyends.append(campaign.likes_last_day['date'].strftime("%d del %m"))
    
    
    chartdata_facebook = {'x': leyends, 'y': records}

    ###########################
    ########################### Facebook Graph



    ########################### Apps Graph
    ###########################
    ########################### Apps
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    
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



    ########################### Devices Graph
    ###########################
    ###########################
#    user_agent_list = App_hit.objects.filter(app__campaign=campaign).values('hit__user_agent')

#    leyends = []
#    data = []
#    mobile = 0
#    tablet = 0
#    pc = 0
#    bot = 0
#    unknown = 0
#    if user_agent_list:
#        for user_agent in user_agent_list:
#            key = parse(user_agent['hit__user_agent'])
#            if key.is_mobile:
#                mobile = mobile + 1
#            elif key.is_tablet:
#                tablet = tablet + 1
#            elif key.is_pc:
#                pc = pc + 1
#            elif key.is_bot:
#                bot = bot + 1
#            else:
#                unknown = unknown + 1
        
#        if mobile:
#            leyends.append("Móvil")
#            data.append(mobile)
#        if tablet:
#            leyends.append("Tablet")
#            data.append(tablet)
#        if pc:
#            leyends.append("PC")
#            data.append(pc)
#        if bot:
#            leyends.append("Bots")
#            data.append(bot)
#        if unknown:
#            leyends.append("Desconocido")
#            data.append(unknown)            
#    else:
#        leyends = ['Ninguno']   
#        data = [0]

#    chartdata_devices = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Devices Graph
    
    
    ########################### Resolution Graph
    ###########################
    ###########################
#    hits = App_hit.objects.filter(app__campaign=campaign).all()

#    leyends = []
#    data = []
#    resolutions = {}
#    if hits:
#        for hit in hits:
#            resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] = 1 if not str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height) in resolutions else resolutions[str(hit.hit.screen_width) + "x" + str(hit.hit.screen_height)] + 1
#        
#        for resolution in resolutions:
#            if resolution == "NonexNone":
#                leyends.append("Desconocida")
#            else:
#                leyends.append(resolution)
#            data.append(resolutions[resolution])
#    else:
#        leyends = ['Ninguna']   
#        data = [0]

#    chartdata_resolution = {'x': leyends, 'y': data}
    
    ###########################
    ########################### Resolution Graph
    


    records = App_record.objects.filter(app__campaign=campaign).all().order_by('-created')[:5]

    context = {        
        'apps_count': apps_count,
        'views_count': views_count,
        'visitors_count': visitors_count,
        'records_count': records_count,
        'records': records,
        'campaign': campaign,
        'chartdata_facebook': chartdata_facebook, 
        'chartdata_apps': chartdata_apps,
#        'chartdata_devices': chartdata_devices,
#        'chartdata_resolution': chartdata_resolution,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        }
    }
    
    return render_to_response('dashboard/details.html', context, context_instance=RequestContext(request))
