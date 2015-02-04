/////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                             //
//    SpreadLabs - Social media suite                                                          //
//    Copyright (C) 2015  Christopher Mejia Montoya - me@chrissmejia.com - chrissmejia.com     //
//                                                                                             //
//    This program is free software: you can redistribute it and/or modify                     //
//    it under the terms of the GNU Affero General Public License as published                 //
//    by the Free Software Foundation, either version 3 of the License, or                     //
//    (at your option) any later version.                                                      //
//                                                                                             //
//    This program is distributed in the hope that it will be useful,                          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                           //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                            //
//    GNU Affero General Public License for more details.                                      //
//                                                                                             //
//    You should have received a copy of the GNU Affero General Public License                 //
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.                    //
//                                                                                             //
/////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// NEW
//////////////////////////////////////////////////
//////////////////////////////////////////////////
$(document).ready(function()
{
	$('#url-add').validate({
		rules: {
			name: {
                            required: true,
                            maxlength: 100
			},
			token: {
                            required: true,
                            maxlength: 50
			}
		},
		messages: {
			name: {
				required: "Por favor introduce un nombre",
				notDefault: "Por favor introduce un nombre",
				maxlength: "Tu nombre debe de tener como máximo 100 letras"
			},
			token: {
				required: "Por favor introduce un token",
				notDefault: "Por favor introduce un token",
				maxlength: "Tu token deben de tener como máximo 50 letras"
			}
		}
	});
	
    $('#send_url').click(function(event) {
    	event.preventDefault();
        if ($('#url-add').valid())
        {
            $.post(_url_save_url, { 
            	name: $('#url-add .name').val(),
                token: $('#url-add .token').val(),
                csrfmiddlewaretoken: _csrf_token
            }).done(function(data) {
            	if (data.substring(0,2) != 'e~')
            	{
            		$('#url-add')[0].reset();
        	      	data=data.split("^");
		    	    {% if app.campaign.membership.own_domain and domain and domain.app = app %}
		    	        $('#privacity ul .mCSB_container').append('<li><span><b>'+data[0]+': </b>http://{{domain.domain}}/s/'+data[1]+'/</span></li>');
    	   		    {% else %}
                       	{% if app.campaign.membership.own_domain and domain %}
           				    $('#privacity ul .mCSB_container').append('<li><span><b>'+data[0]+': </b>http://{{domain.domain}}/app/{{ app.id }}/'+data[1]+'/</span></li>');
            	    	{% else %}					
                 		    $('#privacity ul .mCSB_container').append('<li><span><b>'+data[0]+': </b>https://spreadlabs.com/e/app/{{ app.id }}/'+data[1]+'/</span></li>');
				    	{% endif %}
        		    {% endif %}
                } else {
            		if (data == 'e~1509') {
                 	    alert('La palabra token ya existe, por favor seleccione otra dirección para seguimiento');
                	    window.location.reload();
            		} else if (data == 'e~1510') {
                 	    alert('La palabra token que seleccionó está reservada, por favor seleccione otra dirección para seguimiento');
                	    window.location.reload();
                    } else {
                  	    alert('Un error ha ocurrido');
             	        window.location.reload();
                    }
               }
            }).fail(function() { 
           	        alert('Un error ha ocurrido');
           	        window.location.reload();
            });
        }
    });
});