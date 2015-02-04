
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

$(document).ready(function()
{
    //////////////////////////////////////////////////
    // GateWay Activation
    //////////////////////////////////////////////////	
    $('#fan_page_restrict').change(function () {
            if ($(this).is(':checked'))
            {
                $( "#pages .facebook #link" ).html("<a href='"+_url_app_edit+"' title='{{like_core.name}}'>{{like_core.name}}</a>");
                $( "#pages .facebook" ).removeClass('disabled');
            } else
            {
                $( "#pages .facebook #link" ).html("No seguidores");
                $( "#pages .facebook" ).addClass('disabled');
            }
            $.post(_url_save_page_attrs, { id: "like_core_enabled", target: _like_core_id, core: _core_id, value: $(this).is(':checked'), csrfmiddlewaretoken: _csrf_token })
            .done(function(data) {
                	if (data.substring(0,2) == 'e~')
                	{
           	            alert('Un error ha ocurrido');
           	            window.location.reload();
                    } 
                })
                .fail(function() { 
           	        alert('Un error ha ocurrido');
           	        window.location.reload();
                });
    });
    
    
    //////////////////////////////////////////////////
    // Name
    //////////////////////////////////////////////////	
    $("#page_name").editable(_url_save_page_attrs, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata : function(value, settings) {
            return {core: _core_id, csrfmiddlewaretoken: _csrf_token };
        },
        charcounter : {
            characters : 255
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) != 'e~')
        	{
                $( "#" + $('#input-delete #id_del').val()  + " .input").val(value);
            } else {
            	if (value == 'e~1508') {
               	    alert('Los nombres de las páginas no se pueden repetir');
              	    window.location.reload();
                } else {
               	    alert('Un error ha ocurrido');
              	    window.location.reload();             	
                }
            }
        }
    });



    ///////////////////////////////////////////////// Delete page
    $('#page-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	window.location = _url_app_edit;
            } else {
           	    alert('Un error ha ocurrido' + data);
           	    window.location.reload();
            }
        }
    });
    
    
    
    
    
});