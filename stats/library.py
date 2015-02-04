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

import sys
from datetime import timedelta
from collections import OrderedDict


'''
Created on Dec 18, 2013

@author: chrids
'''

def get_visits_number(hits):
    if hits:
        ips = {}
        date = {}
        for hit in hits:
            if hit.remote_addr in ips:
                if hit.created > date[hit.remote_addr]  + timedelta(hours=1):
                    ips[hit.remote_addr] = ips[hit.remote_addr] + 1
                    date[hit.remote_addr] = hit.created
            else:
                ips[hit.remote_addr] = 1
                date[hit.remote_addr] = hit.created

        total = 0
        for ip in ips:
            total = total + ips[ip]
            
        return total
    
    return 0

def limit_results_dict(entries, limit):
    entries_temp = OrderedDict(sorted(entries.items(), key=lambda x: x[1]))
    items = entries_temp.items()
    items.reverse()
    entries_ordered = OrderedDict(items)
        
    dict = {}   
    xdata = []   
    ydata = [] 
    i = 1
    other_count = 0
    for (key, value) in entries_ordered.items():
        if (str(key) != "Other") and (str(key).lower().startswith("none") != True) and (str(key).lower().startswith("unknown") != True):
            if i < limit:
                xdata.append(str(key))
                ydata.append(int(value))
                dict[str(key)] = int(value)
            else :
                other_count = other_count + int(value)
            i = i + 1
        else :
            other_key = str(key)
            other_count = other_count + int(value)
        
    if other_count:
        key = "Otro"
        if other_key.lower() == "none": key = "No disponible"
        if other_key.lower() == "unknown": key = "Desconocido"
        xdata.append(key)
        ydata.append(other_count)
        dict["Otro"] = int(other_count)
    
    data = {}
    data["xdata"] = xdata
    data["ydata"] = ydata
    data["dict"] = dict
    return data

#def get_visits_number(hits):
#    if hits:
#        ips = {}
#        date = {}
#        for hit in hits:
#            if hit.hit.remote_addr in ips:
#                if hit.hit.created > date[hit.hit.remote_addr]  + timedelta(hours=1):
#                    ips[hit.hit.remote_addr] = ips[hit.hit.remote_addr] + 1
#                    date[hit.hit.remote_addr] = hit.hit.created
#            else:
#                ips[hit.hit.remote_addr] = 1
#                date[hit.hit.remote_addr] = hit.hit.created

#        total = 0
#        for ip in ips:
#            total = total + ips[ip]
#            
#        return total
#    
#    return 0