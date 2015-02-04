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

from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.forms import LoginForm
from django.core.urlresolvers import reverse
#from accounts.forms import RegistrationForm, LoginForm
#from accounts.models import Account
from django.contrib.auth import authenticate, login, logout

from django.forms.util import ErrorList

#def AccountRegistration(request):
#        if request.user.is_authenticated():
#                return HttpResponseRedirect('/profile/')
#        if request.method == 'POST':
#                form = RegistrationForm(request.POST)
#                if form.is_valid():
#                        user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
#                        user.save()
#                        drinker = Drinker(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
#                        drinker.save()
#                        return HttpResponseRedirect('/profile/')
#                else:
#                        return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
#        else:
#                ''' user is not submitting the form, show them a blank registration form '''
#                form = RegistrationForm()
#                context = {'form': form}
#                return render_to_response('register.html', context, context_instance=RequestContext(request))

def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts:profile'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            if account is not None:
                login(request, account)
                return HttpResponseRedirect(reverse('accounts:profile'))
            else:
                form._errors["field_name"] = ErrorList([u"Usuario y/o contraseña incorrecto"])
                return render_to_response('accounts/login.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('accounts/login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show the login form '''
        form = LoginForm()
        context = {'form': form} 
        return render_to_response('accounts/login.html', context, context_instance=RequestContext(request))

@login_required    
def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')
    
@login_required    
def profile(request):
        return HttpResponseRedirect(reverse('dashboard:index'))    