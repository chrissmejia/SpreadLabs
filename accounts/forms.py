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

from django import forms
#from django.contrib.auth.models import User
#from django.forms import ModelForm
#from drinker.models import Drinker

#class RegistrationForm(ModelForm):
#        username        = forms.CharField(label=(u'User Name'))
#        email           = forms.EmailField(label=(u'Email Address'))
#        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
#        password1       = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

#        class Meta:
#                model = Drinker
#                exclude = ('user',)

#        def clean_username(self):
#                username = self.cleaned_data['username']
#                try:
#                        User.objects.get(username=username)
#                except User.DoesNotExist:
#                        return username
#                raise forms.ValidationError("That username is already taken, please select another.")

#        def clean(self):
#                if self.cleaned_data['password'] != self.cleaned_data['password1']:
#                        raise forms.ValidationError("The passwords did not match.  Please try again.")
#                return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))