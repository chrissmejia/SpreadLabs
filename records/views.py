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
import csv
from django.utils import timezone
from dateutil.rrule import rrule, DAILY
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from accounts.models import Agency, Campaign, Profile
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime, timedelta

from apps.models import App, App_hit, App_record

from stats.views import hitting


@login_required
def index(request):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    campaigns = Campaign.objects.filter(agency_id=agency).all()
    
    for campaign in campaigns:
#        campaign.likes = fanpage['likes']
#        campaign.talking_about_count = fanpage['talking_about_count']
#        apps = App.objects.filter(campaign_id=campaign).all()
#        campaign.apps = apps
        campaign.records = App_record.objects.filter(app__campaign=campaign).count()
    
    
    ########################### Campaign Records Graph
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
    
    
    xdata = ["Cédula", "Nombre", "Apellidos", "Correo", "Celular", "Día (*)", "Mes (*)", "Año (*)"]
    ydata = []
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__identification__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__name__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__lastname__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__email__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__cellphone__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__day_of_birth__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__birth_month__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign__agency_id=agency).exclude(record__year_of_birth__isnull=True).count()
    )
    
    extra_serie1 = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}
    chartdata_type = {
        'x': xdata, 
        'name1': 'Registros', 'y1': ydata, 'extra1': extra_serie1,
    }
    
    records_count = App_record.objects.filter(app__campaign__agency_id=agency).count()
    records = App_record.objects.filter(app__campaign__agency=agency).all().order_by('-created')
    
    context = {
        'records': records,
        'records_count': records_count,
        'campaigns': campaigns,
        'chartdata_campaign_records': chartdata_campaign_records,
        'chartdata_type': chartdata_type,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        },
        'extra_discrete': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }
    
    return render_to_response('records/index.html', context, context_instance=RequestContext(request))


@login_required
def export_all(request):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

#    for record in records:
    # Create the HttpResponse object with the appropriate CSV header.
    now = datetime.now()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+agency.name.encode('utf-8')+'_global_'+str(now)+'.csv"'

    writer = csv.writer(response)
    writer.writerow([agency.name.encode('utf-8'), '', '', '', '', '', '', '', '', '', '', now.strftime('%d-%m-%Y')])
    writer.writerow(['Lista total de registros', '', '', '', '', '', '', '', '', '', '', now.strftime('%X')])
    writer.writerow(['', '', '', '', '', '', '', '', '', '', '', ''])
    writer.writerow(['Creación', 'Campaña', 'Aplicación', 'Fuente', 'Cédula', 'Nombre', 'Apellidos', 'Correo', 'Celular', 'Día de nacimiento', 'Mes de nacimiento', 'Año de nacimiento'])
    
    records = App_record.objects.filter(app__campaign__agency=agency).all().order_by('-created')
    for record in records:
        if record.record.created:
            created = str(record.record.created)
        else:
            created = ''
            
        if record.app.campaign.name:
            campaign = record.app.campaign.name
            campaign = campaign.encode('utf-8')
        else:
            campaign = ''
        if record.app.name:
            app_name = record.app.name
            app_name = app_name.encode('utf-8')
        else:
            app_name = ''
                
        if record.source:
            source = record.source
            source = source.encode('utf-8')
        else:
            source = ''
                
        if record.record.identification:
            identification = record.record.identification
            identification = identification.encode('utf-8')
        else:
            identification = ''
                
        if record.record.name:
            name = record.record.name
            name = name.encode('utf-8')
        else:
            name = ''
                
        if record.record.lastname:
            lastname = record.record.lastname
            lastname = lastname.encode('utf-8')
        else:
            lastname = ''
                
        if record.record.email:
            email = record.record.email
            email = email.encode('utf-8')
        else:
            email = ''
                
        if record.record.cellphone:
            cellphone = str(record.record.cellphone)
        else:
            cellphone = ''
                
        if record.record.day_of_birth:
            day = str(record.record.day_of_birth)
        else:
            day = ''
                
        if record.record.birth_month:
            month = str(record.record.birth_month)
        else:
            month = ''
                
        if record.record.year_of_birth:
            year = str(record.record.year_of_birth)
        else:
            year = ''
            
        writer.writerow([created, campaign, app_name, source, identification, name, lastname, email, cellphone, day, month, year])

    return response        

@login_required
def details(request, campaign_id=None):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')
    
    ########################### Apps Records Graph
    ###########################
    ########################### Apps
    
    active_apps = App.objects.filter(campaign=campaign).exclude(facebook_access=None).all()
    inactive_apps = App.objects.filter(campaign=campaign, facebook_access=None).all()
    
    records = []
    leyends = []
    for app in active_apps:
        app.records = App_record.objects.filter(app__campaign=campaign, app=app).count()
        if app.records:
            records.append(app.records)
            leyends.append(app.name)
    
    
    chartdata_apps_records = {'x': leyends, 'y': records}

    ###########################
    ########################### Apps Records Graph    
    
    xdata = ["Cédula", "Nombre", "Apellidos", "Correo", "Celular", "Día (*)", "Mes (*)", "Año (*)"]
    ydata = []
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__identification__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__name__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__lastname__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__email__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__cellphone__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__day_of_birth__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__birth_month__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app__campaign=campaign).exclude(record__year_of_birth__isnull=True).count()
    )

    extra_serie1 = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}
    chartdata_type = {
        'x': xdata, 
        'name1': 'Registros', 'y1': ydata, 'extra1': extra_serie1,
    }
    
    records_count = App_record.objects.filter(app__campaign=campaign).count()
    records = App_record.objects.filter(app__campaign=campaign).all().order_by('-created')
    
    context = {
        'active_apps':active_apps,
        'inactive_apps':inactive_apps,
        'campaign': campaign,
        'records': records,
        'records_count': records_count,
        'chartdata_apps_records': chartdata_apps_records,
        'chartdata_type': chartdata_type,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        },
        'extra_discrete': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },

    }
    
    return render_to_response('records/details.html', context, context_instance=RequestContext(request))


@login_required
def export_campaign(request, campaign_id=None):
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        campaign = Campaign.objects.get(agency_id=agency, id=campaign_id)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

#    for record in records:
    # Create the HttpResponse object with the appropriate CSV header.
    now = datetime.now()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+agency.name.encode('utf-8')+'_'+campaign.name.encode('utf-8')+'_'+str(now)+'.csv"'

    writer = csv.writer(response)
    writer.writerow([agency.name.encode('utf-8'), '', '', '', '', '', '', '', '', '', now.strftime('%d-%m-%Y')])
    writer.writerow(['Lista total de registros de ' + campaign.name.encode('utf-8'), '', '', '', '', '', '', '', '', '', now.strftime('%X')])
    writer.writerow(['', '', '', '', '', '', '', '', '', '', ''])
    writer.writerow(['Creación', 'Aplicación', 'Fuente', 'Cédula', 'Nombre', 'Apellidos', 'Correo', 'Celular', 'Día de nacimiento', 'Mes de nacimiento', 'Año de nacimiento'])
    
    records = App_record.objects.filter(app__campaign=campaign).all().order_by('-created')
    for record in records:
        if record.record.created:
            created = str(record.record.created)
        else:
            created = ''
            
        if record.app.name:
            app_name = record.app.name
            app_name = app_name.encode('utf-8')
        else:
            app_name = ''
                
        if record.source:
            source = record.source
            source = source.encode('utf-8')
        else:
            source = ''
                
        if record.record.identification:
            identification = record.record.identification
            identification = identification.encode('utf-8')
        else:
            identification = ''
                
        if record.record.name:
            name = record.record.name
            name = name.encode('utf-8')
        else:
            name = ''
                
        if record.record.lastname:
            lastname = record.record.lastname
            lastname = lastname.encode('utf-8')
        else:
            lastname = ''
                
        if record.record.email:
            email = record.record.email
            email = email.encode('utf-8')
        else:
            email = ''
                
        if record.record.cellphone:
            cellphone = str(record.record.cellphone)
        else:
            cellphone = ''
                
        if record.record.day_of_birth:
            day = str(record.record.day_of_birth)
        else:
            day = ''
                
        if record.record.birth_month:
            month = str(record.record.birth_month)
        else:
            month = ''
                
        if record.record.year_of_birth:
            year = str(record.record.year_of_birth)
        else:
            year = ''
            
        writer.writerow([created, app_name, source, identification, name, lastname, email, cellphone, day, month, year])

    return response        


@login_required
def app(request, app_id=None):
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    campaign = app.campaign

    ###########################
    ########################### Apps Records Graph    
    
    xdata = ["Cédula", "Nombre", "Apellidos", "Correo", "Celular", "Día (*)", "Mes (*)", "Año (*)"]
    ydata = []
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__identification__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__name__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__lastname__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__email__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__cellphone__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__day_of_birth__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__birth_month__isnull=True).count()
    )
    ydata.append(
        App_record.objects.filter(app=app).exclude(record__year_of_birth__isnull=True).count()
    )

    extra_serie1 = {"tooltip": {"y_start": "Existen ", "y_end": " registros"}}
    chartdata_type = {
        'x': xdata, 
        'name1': 'Registros', 'y1': ydata, 'extra1': extra_serie1,
    }
    
    records_count = App_record.objects.filter(app=app).count()
    records = App_record.objects.filter(app=app).all().order_by('-created')
    
    context = {
        'app': app,
        'campaign': campaign,
        'records': records,
        'records_count': records_count,
        'chartdata_type': chartdata_type,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
            'height': None
        },
        'extra_discrete': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }
    
    return render_to_response('records/app.html', context, context_instance=RequestContext(request))


@login_required
def export_app(request, app_id=None):
    
    profile = Profile.objects.get(user_id=request.user)
    agency = profile.agency

    try:
        app = App.objects.get(id=app_id, campaign_id__agency_id=agency)
    except:
        hitting(request, 1001) # Stats
        return redirect('/error/1001')

    campaign = app.campaign

#    for record in records:
    # Create the HttpResponse object with the appropriate CSV header.
    now = datetime.now()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+agency.name.encode('utf-8')+'_'+campaign.name.encode('utf-8')+'_'+app.name.encode('utf-8')+'_'+str(now)+'.csv"'

    writer = csv.writer(response)
    writer.writerow([agency.name.encode('utf-8'), '', '', '', '', '', '', '', '', now.strftime('%d-%m-%Y')])
    writer.writerow(['Lista total de registros de ' + campaign.name.encode('utf-8') + ' obtenidos desde la aplicación: ' + app.name.encode('utf-8'), '', '', '', '', '', '', '', '', now.strftime('%X')])
    writer.writerow(['', '', '', '', '', '', '', '', '', ''])
    writer.writerow(['Creación', 'Fuente', 'Cédula', 'Nombre', 'Apellidos', 'Correo', 'Celular', 'Día de nacimiento', 'Mes de nacimiento', 'Año de nacimiento'])
    
    records = App_record.objects.filter(app=app).all().order_by('-created')
    for record in records:
        if record.record.created:
            created = str(record.record.created)
        else:
            created = ''
            
        if record.source:
            source = record.source
            source = source.encode('utf-8')
        else:
            source = ''
                
        if record.record.identification:
            identification = record.record.identification
            identification = identification.encode('utf-8')
        else:
            identification = ''
                
        if record.record.name:
            name = record.record.name
            name = name.encode('utf-8')
        else:
            name = ''
                
        if record.record.lastname:
            lastname = record.record.lastname
            lastname = lastname.encode('utf-8')
        else:
            lastname = ''
                
        if record.record.email:
            email = record.record.email
            email = email.encode('utf-8')
        else:
            email = ''
                
        if record.record.cellphone:
            cellphone = str(record.record.cellphone)
        else:
            cellphone = ''
                
        if record.record.day_of_birth:
            day = str(record.record.day_of_birth)
        else:
            day = ''
                
        if record.record.birth_month:
            month = str(record.record.birth_month)
        else:
            month = ''
                
        if record.record.year_of_birth:
            year = str(record.record.year_of_birth)
        else:
            year = ''
            
        writer.writerow([created, source, identification, name, lastname, email, cellphone, day, month, year])

    return response        