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

import time, sys
from datetime import date
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import timedelta
from user_agents import parse

from stats.views import hitting

from stats.library import get_visits_number

from accounts.models import Campaign, Profile
from apps.models import App, App_hit, App_record


@login_required
def main(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
        

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

    ########################### Views
    views = []
    for leyend in leyends_date:
        views.append(App_hit.objects.filter(app__campaign__agency=agency,\
                                            created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

#    print >>sys.stderr, views
    ########################### Visits
    visits = []
    for leyend in leyends_date:
        visits.append(get_visits_number(App_hit.objects.filter(app__campaign__agency=agency,\
                                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).all())
                      )

#    print >>sys.stderr, visits

    ########################### Visitors
    visitors = []
    for leyend in leyends_date:
        visitors.append(App_hit.objects.filter(app__campaign__agency=agency,\
                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values("hit__remote_addr").distinct().count())
#    print >>sys.stderr, visitors

    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app__campaign__agency=agency,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
#    print >>sys.stderr, records
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}
    extra_serie_visits = {"tooltip": {"y_start": "Existen ", "y_end": " visitas"}}
    extra_serie_visitors = {"tooltip": {"y_start": "Existen ", "y_end": " visitantes"}}
    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Vistas', 'y1': views, 'extra1': extra_serie_views,
        'name2': 'Visitas', 'y2': visits, 'extra2': extra_serie_visits,
        'name3': 'Visitantes', 'y3': visitors, 'extra3': extra_serie_visitors,
        'name4': 'Registros', 'y4': records, 'extra4': extra_serie_records,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


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

    ########################### Views
    views = []
    for leyend in leyends_date:
        views.append(App_hit.objects.filter(app__campaign__agency=agency, app__campaign=campaign,\
                                            created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

#    print >>sys.stderr, views
    ########################### Visits
    visits = []
    for leyend in leyends_date:
        visits.append(get_visits_number(App_hit.objects.filter(app__campaign__agency=agency, app__campaign=campaign,\
                                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).all())
                      )

#    print >>sys.stderr, visits

    ########################### Visitors
    visitors = []
    for leyend in leyends_date:
        visitors.append(App_hit.objects.filter(app__campaign__agency=agency, app__campaign=campaign,\
                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values("hit__remote_addr").distinct().count())
#    print >>sys.stderr, visitors

    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app__campaign__agency=agency, app__campaign=campaign,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
#    print >>sys.stderr, records

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}
    extra_serie_visits = {"tooltip": {"y_start": "Existen ", "y_end": " visitas"}}
    extra_serie_visitors = {"tooltip": {"y_start": "Existen ", "y_end": " visitantes"}}
    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Vistas', 'y1': views, 'extra1': extra_serie_views,
        'name2': 'Visitas', 'y2': visits, 'extra2': extra_serie_visits,
        'name3': 'Visitantes', 'y3': visitors, 'extra3': extra_serie_visitors,
        'name4': 'Registros', 'y4': records, 'extra4': extra_serie_records,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


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

    ########################### Views
    views = []
    for leyend in leyends_date:
        views.append(App_hit.objects.filter(app=app,\
                                            created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

#    print >>sys.stderr, views
    ########################### Visits
    visits = []
    for leyend in leyends_date:
        visits.append(get_visits_number(App_hit.objects.filter(app__campaign__agency=agency, app=app,\
                                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).all())
                      )

#    print >>sys.stderr, visits

    ########################### Visitors
    visitors = []
    for leyend in leyends_date:
        visitors.append(App_hit.objects.filter(app=app,\
                                               created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values("hit__remote_addr").distinct().count())
#    print >>sys.stderr, visitors
        
    ########################### Records
    records = []
    for leyend in leyends_date:
        records.append(App_record.objects.filter(app=app,\
                                                 created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
#    print >>sys.stderr, records
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}
    extra_serie_visits = {"tooltip": {"y_start": "Existen ", "y_end": " visitas"}}
    extra_serie_visitors = {"tooltip": {"y_start": "Existen ", "y_end": " visitantes"}}
    extra_serie_records = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Vistas', 'y1': views, 'extra1': extra_serie_views,
        'name2': 'Visitas', 'y2': visits, 'extra2': extra_serie_visits,
        'name3': 'Visitantes', 'y3': visitors, 'extra3': extra_serie_visitors,
        'name4': 'Registros', 'y4': records, 'extra4': extra_serie_records,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))    



@login_required
def main_environment(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
        

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

    ########################### Views
    chrome = []
    firefox = []
    safari = []
    ie = []
    other = []
    for leyend in leyends_date:
        day_hits = App_hit.objects.filter(app__campaign__agency=agency,\
                                          created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent')
        chrome_counter = 0
        firefox_counter = 0
        safari_counter = 0
        ie_counter = 0
        other_counter = 0
        
        for day_hit in day_hits:
            if day_hit['hit__user_agent']:
                key = parse(day_hit['hit__user_agent'])
                if key.browser.family == "Chrome":
                    chrome_counter = chrome_counter + 1
                elif key.browser.family == "Firefox":
                    firefox_counter = firefox_counter + 1
                elif key.browser.family == "Safari":
                    safari_counter = safari_counter + 1
                elif key.browser.family == "IE":
                    ie_counter = ie_counter + 1
                else:
                    other_counter = other_counter + 1
            else:
                other_counter = other_counter + 1
                
        chrome.append(chrome_counter)
        firefox.append(firefox_counter)
        safari.append(safari_counter)
        ie.append(ie_counter)
        other.append(other_counter)


    extra_serie_chrome = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Chrome"}}
    extra_serie_firefox = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Firefox"}}
    extra_serie_safari = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Safari"}}
    extra_serie_ie = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Internet Explorer"}}
    extra_serie_other = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Otro"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Chrome', 'y1': chrome, 'extra1': extra_serie_chrome,
        'name2': 'Firefox', 'y2': firefox, 'extra2': extra_serie_firefox,
        'name3': 'Safari', 'y3': safari, 'extra3': extra_serie_safari,
        'name4': 'Internet Explorer', 'y4': ie, 'extra4': extra_serie_ie,
        'name5': 'Otro', 'y5': other, 'extra5': extra_serie_other,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))



@login_required
def main_campaign_enviroment(request, campaign_id=None):
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

    ########################### Views
    chrome = []
    firefox = []
    safari = []
    ie = []
    other = []
    for leyend in leyends_date:
        day_hits = App_hit.objects.filter(app__campaign=campaign,\
                                          created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent')
        chrome_counter = 0
        firefox_counter = 0
        safari_counter = 0
        ie_counter = 0
        other_counter = 0
        
        for day_hit in day_hits:
            if day_hit['hit__user_agent']:
                key = parse(day_hit['hit__user_agent'])
                if key.browser.family == "Chrome":
                    chrome_counter = chrome_counter + 1
                elif key.browser.family == "Firefox":
                    firefox_counter = firefox_counter + 1
                elif key.browser.family == "Safari":
                    safari_counter = safari_counter + 1
                elif key.browser.family == "IE":
                    ie_counter = ie_counter + 1
                else:
                    other_counter = other_counter + 1
            else:
                other_counter = other_counter + 1
                
        chrome.append(chrome_counter)
        firefox.append(firefox_counter)
        safari.append(safari_counter)
        ie.append(ie_counter)
        other.append(other_counter)


    extra_serie_chrome = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Chrome"}}
    extra_serie_firefox = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Firefox"}}
    extra_serie_safari = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Safari"}}
    extra_serie_ie = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Internet Explorer"}}
    extra_serie_other = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Otro"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Chrome', 'y1': chrome, 'extra1': extra_serie_chrome,
        'name2': 'Firefox', 'y2': firefox, 'extra2': extra_serie_firefox,
        'name3': 'Safari', 'y3': safari, 'extra3': extra_serie_safari,
        'name4': 'Internet Explorer', 'y4': ie, 'extra4': extra_serie_ie,
        'name5': 'Otro', 'y5': other, 'extra5': extra_serie_other,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_app_enviroment(request, app_id=None):
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

    ########################### Views
    chrome = []
    firefox = []
    safari = []
    ie = []
    other = []
    for leyend in leyends_date:
        day_hits = App_hit.objects.filter(app=app,\
                                          created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent')
        chrome_counter = 0
        firefox_counter = 0
        safari_counter = 0
        ie_counter = 0
        other_counter = 0
        
        for day_hit in day_hits:
            if day_hit['hit__user_agent']:
                key = parse(day_hit['hit__user_agent'])
                if key.browser.family == "Chrome":
                    chrome_counter = chrome_counter + 1
                elif key.browser.family == "Firefox":
                    firefox_counter = firefox_counter + 1
                elif key.browser.family == "Safari":
                    safari_counter = safari_counter + 1
                elif key.browser.family == "IE":
                    ie_counter = ie_counter + 1
                else:
                    other_counter = other_counter + 1
            else:
                other_counter = other_counter + 1
                
        chrome.append(chrome_counter)
        firefox.append(firefox_counter)
        safari.append(safari_counter)
        ie.append(ie_counter)
        other.append(other_counter)


    extra_serie_chrome = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Chrome"}}
    extra_serie_firefox = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Firefox"}}
    extra_serie_safari = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Safari"}}
    extra_serie_ie = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Internet Explorer"}}
    extra_serie_other = {"tooltip": {"y_start": "Existen ", "y_end": " vistas desde Otro"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Chrome', 'y1': chrome, 'extra1': extra_serie_chrome,
        'name2': 'Firefox', 'y2': firefox, 'extra2': extra_serie_firefox,
        'name3': 'Safari', 'y3': safari, 'extra3': extra_serie_safari,
        'name4': 'Internet Explorer', 'y4': ie, 'extra4': extra_serie_ie,
        'name5': 'Otro', 'y5': other, 'extra5': extra_serie_other,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))    


@login_required
def main_system(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

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

    touch_array = []
    no_touch_array = []
    
    for leyend in leyends_date:
        touch = 0
        user_agent_day = App_hit.objects.filter(app__campaign__agency=agency,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent').order_by().annotate(total=Count('id'))    

        count = App_hit.objects.filter(app__campaign__agency=agency,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count()    

        if user_agent_day:
            for user_agent in user_agent_day:
                if user_agent['hit__user_agent']:
                    key = parse(user_agent['hit__user_agent'])
                    if key.is_touch_capable:
                        touch = touch + user_agent['total']

        touch_array.append(touch)
        no_touch_array.append(count - touch)
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': u'Pantalla táctil', 'y1': touch_array, 'extra1': extra_serie_views,
        'name2': u'Sin pantalla táctil', 'y2': no_touch_array, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_campaign_system(request, campaign_id=None):
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

    touch_array = []
    no_touch_array = []
    
    for leyend in leyends_date:
        touch = 0
        user_agent_day = App_hit.objects.filter(app__campaign=campaign,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent').order_by().annotate(total=Count('id'))    

        count = App_hit.objects.filter(app__campaign=campaign,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count()    

        if user_agent_day:
            for user_agent in user_agent_day:
                if user_agent['hit__user_agent']:
                    key = parse(user_agent['hit__user_agent'])
                    if key.is_touch_capable:
                        touch = touch + user_agent['total']

        touch_array.append(touch)
        no_touch_array.append(count - touch)
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': u'Pantalla táctil', 'y1': touch_array, 'extra1': extra_serie_views,
        'name2': u'Sin pantalla táctil', 'y2': no_touch_array, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_app_system(request, app_id=None):
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

    touch_array = []
    no_touch_array = []
    
    for leyend in leyends_date:
        touch = 0
        user_agent_day = App_hit.objects.filter(app=app,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).values('hit__user_agent').order_by().annotate(total=Count('id'))    

        count = App_hit.objects.filter(app=app,\
                                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count()    

        if user_agent_day:
            for user_agent in user_agent_day:
                if user_agent['hit__user_agent']:
                    key = parse(user_agent['hit__user_agent'])
                    if key.is_touch_capable:
                        touch = touch + user_agent['total']

        touch_array.append(touch)
        no_touch_array.append(count - touch)
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': u'Pantalla táctil', 'y1': touch_array, 'extra1': extra_serie_views,
        'name2': u'Sin pantalla táctil', 'y2': no_touch_array, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))    


@login_required
def main_advanced(request):
#    graph = GraphAPI(request.session['facebook_access_token'])
    last_month = timezone.now() - timedelta(days=30)
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency
        
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

    ########################### Canvas
    canvas = []
    for leyend in leyends_date:
        canvas.append(App_hit.objects.filter(app__campaign__agency=agency, hit__webgl=True,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

    ########################### No canvas
    no_canvas = []
    for leyend in leyends_date:
        no_canvas.append(App_hit.objects.filter(app__campaign__agency=agency, hit__webgl=False,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())
        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Soporte 3d', 'y1': canvas, 'extra1': extra_serie_views,
        'name2': 'Sin soporte 3d', 'y2': no_canvas, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_campaign_advanced(request, campaign_id=None):
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

    ########################### Canvas
    canvas = []
    for leyend in leyends_date:
        canvas.append(App_hit.objects.filter(app__campaign=campaign, hit__webgl=True,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

    ########################### No canvas
    no_canvas = []
    for leyend in leyends_date:
        no_canvas.append(App_hit.objects.filter(app__campaign=campaign, hit__webgl=False,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Soporte 3d', 'y1': canvas, 'extra1': extra_serie_views,
        'name2': 'Sin soporte 3d', 'y2': no_canvas, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))


@login_required
def main_app_advanced(request, app_id=None):
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

    ########################### Canvas
    canvas = []
    for leyend in leyends_date:
        canvas.append(App_hit.objects.filter(app=app, hit__webgl=True,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())

    ########################### No canvas
    no_canvas = []
    for leyend in leyends_date:
        no_canvas.append(App_hit.objects.filter(app=app, hit__webgl=False,\
                                created__startswith=date(int(leyend.strftime("%Y")),int(leyend.strftime("%m")), int(leyend.strftime("%d")))).count())        

    extra_serie_views = {"tooltip": {"y_start": "Existen ", "y_end": " vistas"}}

    chartdata_hits = {
        'x': leyends,
        'name1': 'Soporte 3d', 'y1': canvas, 'extra1': extra_serie_views,
        'name2': 'Sin soporte 3d', 'y2': no_canvas, 'extra2': extra_serie_views,
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
    
    return render_to_response('statsExtended/main.html', context, context_instance=RequestContext(request))    
