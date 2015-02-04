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
from datetime import date
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from stats.views import hitting

from accounts.models import Campaign, Profile
from apps.models import App, App_record

@login_required
def main(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
        

    ########################### Main Graph
    ###########################
    ########################### Records
    ###########################
    ########################### Main Graph Leyends
    leyends = []
    leyends_date = []
    leyends_date_str = []
    for day in rrule(DAILY, dtstart=last_month, until=timezone.now()):
        day_zoned = day.astimezone(timezone.get_default_timezone())
        leyends_date_str.append(day_zoned.strftime("%Y-%m-%d"))
        leyends_date.append(day_zoned)
        leyends.append(int(time.mktime(day_zoned.timetuple()) * 1000))


    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app__campaign__agency=agency,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
#    print >>sys.stderr, records
        

    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Registros', 'y1': records, 'extra1': extra_serie_records,
    }
    ###########################
    ########################### Main Graph
    
    
    context = {
        'chartdata_hits': chartdata_hits,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
        }
    }
    
    return render_to_response('recordsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_campaign(request, campaign_id=None):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
        
       
    ########################### Main Graph
    ###########################
    ########################### Views, Visits, Visitors, Records
    ###########################
    ########################### Main Graph Leyends
    leyends = []
    leyends_date = []
    leyends_date_str = []
    for day in rrule(DAILY, dtstart=last_month, until=timezone.now()):
        day_zoned = day.astimezone(timezone.get_default_timezone())
        leyends_date_str.append(day_zoned.strftime("%Y-%m-%d"))
        leyends_date.append(day_zoned)
        leyends.append(int(time.mktime(day_zoned.timetuple()) * 1000))


    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app__campaign__agency=agency, app__campaign=campaign,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Registros', 'y1': records, 'extra1': extra_serie_records,
    }
    
    
    context = {
        'chartdata_hits': chartdata_hits,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
        }
    }
    
    return render_to_response('recordsExtended/main.html', context, context_instance=RequestContext(request))




@login_required
def main_app(request, app_id=None):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
        
       
    ########################### Main Graph
    ###########################
    ########################### Views, Visits, Visitors, Records
    ###########################
    ########################### Main Graph Leyends
    leyends = []
    leyends_date = []
    leyends_date_str = []
    for day in rrule(DAILY, dtstart=last_month, until=timezone.now()):
        day_zoned = day.astimezone(timezone.get_default_timezone())
        leyends_date_str.append(day_zoned.strftime("%Y-%m-%d"))
        leyends_date.append(day_zoned)
        leyends.append(int(time.mktime(day_zoned.timetuple()) * 1000))


    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app=app,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
        

    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Registros', 'y4': records, 'extra4': extra_serie_records,
    }
    ###########################
    ########################### Main Graph
    
    
    context = {
        'chartdata_hits': chartdata_hits,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
        }
    }
    
    return render_to_response('recordsExtended/main.html', context, context_instance=RequestContext(request))    
