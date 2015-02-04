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

from facepy import GraphAPI

def have_page_permission(request, page_id, permission):
    graph = GraphAPI(request.session['facebook_access_token'])
    try:
        current_permission = graph.fql('select perms from page_admin where page_id=' + page_id +' and uid= me()')
    except:
        return False
    
    if not current_permission['data']:
        return False
    
    if permission in current_permission['data'][0]['perms']:
        return True
    
    return False