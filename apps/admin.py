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

from django.contrib import admin
from apps.models import Facebook_access, App, Core_app, Core_object_background, Core_object_image_links, App_hit,\
    Core_object_youtube, Core_object_input, App_record, Domain, App_source
# App_structure,
admin.site.register(Facebook_access)
admin.site.register(App)
admin.site.register(Core_app)
admin.site.register(Core_object_background)
admin.site.register(Core_object_image_links)
admin.site.register(Core_object_youtube)
admin.site.register(Core_object_input)
admin.site.register(Domain)
admin.site.register(App_record)
admin.site.register(App_hit)
admin.site.register(App_source)
