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

from django.http import HttpResponse


'''

1000 | App Errors
    1001 | No Access
    1002 | No correct format
    1003 | Incorrect Query
    1004 | Unknown Core App
    1005 | Unknown Domain
    1006 | Unknown Domain App

1500 | Facebook Errors
    1501 | Unknown Facebook access
    1502 | Unknown Application
    1503 | Unknown Go Core App
    1504 | Unknown Signed Request
    1505 | Like Page
    1506 | Create app Facebook access error
    1507 | No minimal manage permissions
    1508 | Core app name duplicate
    1509 | url app token duplicate
    1510 | url app token reserved

'''

def index(request, error_id=None):
    return HttpResponse("error " + error_id) 