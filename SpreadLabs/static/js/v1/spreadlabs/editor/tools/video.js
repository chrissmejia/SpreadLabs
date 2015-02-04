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
// DRAGGABLE
//////////////////////////////////////////////////
//////////////////////////////////////////////////
function draggable_youtube()
{
    $(document).ready(function()
    {
        $( ".drag_youtube" ).draggable({ 
	        containment: "#background", 
		    scroll: false,
		    stop: function(event, ui) {
          	    $.post(_url_save_youtube_position, { id: this.id, left: $(this).position().left, top: $(this).position().top, core: _core_id, csrfmiddlewaretoken: _csrf_token  })
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
            }
  	    });
  	});
}
draggable_youtube();


//////////////////////////////////////////////////
//////////////////////////////////////////////////
// NEW
//////////////////////////////////////////////////
//////////////////////////////////////////////////

$(document).ready(function()
{
    $('#tool-youtube').click(function(){
    	event.preventDefault();
    	$.post(_url_save_youtube, { core: _core_id, csrfmiddlewaretoken: _csrf_token  })
        .done(function(data) {
            if (data.substring(0,2) == 'e~')
            {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            } else {
                $('#background').append('<div id="youtube_'+data+'" class="drag_youtube object tool youtube" >'+
                                            '<input class="hidden" type="hidden" name="video" value="O6OnY_8l6Us">'+
                                            '<object width="400" height="225"><param name="movie" value="http://www.youtube.com/v/O6OnY_8l6Us?version=3&amp;hl=es_ES&amp;rel=0"></param><param name="allowFullScreen" value="true"></param><param name="wmode" value="transparent" /><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/O6OnY_8l6Us?version=3&amp;hl=es_ES&amp;rel=0" type="application/x-shockwave-flash" width="400" height="225" allowscriptaccess="always" allowfullscreen="true"></embed></object>'+
                                        '</div>');
                $("#youtube_"+ data).mousedown();
                draggable_youtube();
            }
        });
	});
}); 


//////////////////////////////////////////////////
//////////////////////////////////////////////////
// CHANGE
//////////////////////////////////////////////////
//////////////////////////////////////////////////
$(document).ready(function()
{


    //////////////////////////////////////////////////
    // Video
    //////////////////////////////////////////////////	
    $(".edit_youtube").editable(_url_save_youtube_attrs, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata : function(value, settings) {
            return {video:  $( "#youtube-object #id" ).val(), core: _core_id, csrfmiddlewaretoken: _csrf_token };
        },
        charcounter : {
            characters : 255
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) != 'e~')
        	{
                $( "#" + $( "#youtube-object #id" ).val() ).html('<input class="hidden" type="hidden" name="video" value="'+value+'">'+
                                                             '<object width="400" height="225"><param name="movie" value="http://www.youtube.com/v/'+value+'?version=3&amp;hl=es_ES&amp;rel=0"></param><param name="allowFullScreen" value="true"></param><param name="wmode" value="transparent" /><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/'+value+'?version=3&amp;hl=es_ES&amp;rel=0" type="application/x-shockwave-flash" width="400" height="225" allowscriptaccess="always" allowfullscreen="true"></embed></object>');
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });


    ///////////////////////////////////////////////// Delete Youtube
    $('#youtube-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#" + $( "#youtube-delete #id_del" ).val() ).remove();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
});