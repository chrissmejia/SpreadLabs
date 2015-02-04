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
// LOAD
//////////////////////////////////////////////////
//////////////////////////////////////////////////
function loadImageLink(tag)
{   
    $(document).ready(function()
    {
	    image = tag.find('img');
	    imgSrc = image.attr("src");
	    $('#image-link-object #image-link-thumb img').attr("src", imgSrc);
	
	    aHref = tag.find('.image_link_external').val();
	    $('#image-link-object .external p').text(aHref);

    	$('#image-link-upload #id').val(tag.attr('id'));
    	$('#image-link-delete #del_id').val(tag.attr('id'));
    	
    	
        $("#link_type option").removeAttr('disabled');
        $("#image-link-object .attrs").hide();

    	if (tag.find('input').val() == "external")
    	{
            $("#link_type").val('external');
            $("#link_type #external").attr('disabled', true);
    		$("#image-link-object .external").show();
    	} else if (tag.find('input').val() == "internal")
    	{
            $("#link_type").val('internal');
            $("#link_type #internal").attr('disabled', true);
            $("#image-link-object .internal h2").text('Página interna');
    		$("#image-link-object .internal").show();
    	} else {
            $("#link_type").val('send');
            $("#link_type #send").attr('disabled', true);
            $("#image-link-object .internal h2").text('Enviar a');
    		$("#image-link-object .internal").show();
    	}
    	    
    	    
    	$('#link_type').trigger("liszt:updated");
    	

	    internal = tag.find('.image_link_internal').val();
	    $('#internal_page').val(internal);

    	$('#internal_page').trigger("liszt:updated");
	
    
    });    
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// DRAGGABLE
//////////////////////////////////////////////////
//////////////////////////////////////////////////
function draggable_image_link()
{
    $(document).ready(function()
    {
    	$( ".drag_image_link" ).draggable({ 
	    	containment: "#background", 
		    scroll: false,
		    stop: function(event, ui) {
          	    $.post(_url_save_image_link_position, { id: this.id, left: $(this).position().left, top: $(this).position().top, core: _core_id, csrfmiddlewaretoken: _csrf_token  })
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
draggable_image_link();

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// NEW
//////////////////////////////////////////////////
//////////////////////////////////////////////////

$(document).ready(function()
{
    $('#tool-image-link').click(function(){
    	event.preventDefault();
    	$.post(_url_save_image_link, { id: "new", core: _core_id, csrfmiddlewaretoken: _csrf_token })
        .done(function(data) {
            if (data.substring(0,2) == 'e~')
            {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            } else {
            	data=data.split("^");
                $('#background').append('<div id="image_link_'+data[0]+'" class="drag_image_link object tool image-link">'+
                                            '<input id="image_link_type_'+data[0]+'" class="hidden type" type="hidden" name="type" value="external">'+
                                            '<input id="image_link_external_'+data[0]+'" class="hidden image_link_external" type="hidden" name="type" value="https://spreadlabs.com">'+
                                            '<input id="image_link_internal_'+data[0]+'" class="hidden image_link_internal" type="hidden" name="type" value="{{this_core.id}}">'+
                                            '<a href="https://spreadlabs.com">'+
                                                '<img src="'+_media+data[1]+'">'+
                                            '</a>'+
                                        '</div>');
                $("#image_link_"+ data[0]).mousedown();
                draggable_image_link();
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
    // Type
    //////////////////////////////////////////////////
    $('#link_type').chosen({
    	width:"100%",
    	no_results_text:'Opción no disponible'
    }).change(function(event) 
    {
        $("#link_type option").removeAttr('disabled');
        $("#image-link-object .attrs").hide();
    	
    	if ($("#link_type option:selected").val() == "external")
    	{
            $("#link_type #external").attr('disabled', true);
      		$("#image-link-object .external").show();
      		$("#" + $('#image-link-upload #id').val() + " .type").val("external");
    	} else if ($("#link_type option:selected").val() == "internal")
    	{
            $("#link_type #internal").attr('disabled', true);
            $("#image-link-object .internal h2").text('Página interna');
      		$("#image-link-object .internal").show();
      		$("#" + $('#image-link-upload #id').val() + " .type").val("internal");
    	} else {
            $("#link_type #send").attr('disabled', true);
            $("#image-link-object .internal h2").text('Enviar a');
      		$("#image-link-object .internal").show();
      		$("#" + $('#image-link-upload #id').val() + " .type").val("send");
    	}
    	$('#link_type').trigger("liszt:updated");
    	
    	$.post(_url_save_image_link_attrs, { 
    		id: "type", 
    		target:  $('#image-link-upload #id').val(), 
    		core: _core_id, 
    		value: $("#link_type option:selected").val(), 
    		csrfmiddlewaretoken: _csrf_token 
    	})
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
    // Internal page type
    //////////////////////////////////////////////////
    $('#internal_page').chosen({
    	width:"100%",
    	no_results_text:'Opción no disponible'
    }).change(function(event) 
    {
    	$("#" + $('#image-link-upload #id').val() + " .image_link_internal").val($("#internal_page option:selected").val());
    	$.post(_url_save_image_link_attrs, { 
    		id: "internal_page", 
    		target:  $('#image-link-upload #id').val(), 
    		core: _core_id, 
    		value: $("#internal_page option:selected").val(), 
    		csrfmiddlewaretoken: _csrf_token 
    	})
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
    // Image
    //////////////////////////////////////////////////
    $("#image-link-thumb").click(function(event) {
    	event.preventDefault();
    	$( "#image-link-file" ).click();
    });

    $('#image-link-upload').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#" + $( "#image-link-upload #id" ).val() + " img" ).attr("src", data);
            	$( "#image-link-thumb img" ).attr("src", data);
            	$('#image-link-upload').get(0).reset();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
    $('#image-link-file').change(function() {
        $('#image-link-upload').submit();
    });
    
    ///////////////////////////////////////////////// Delete Image

    $('#image-link-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#" + $( "#image-link-upload #id" ).val() ).remove();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    

    //////////////////////////////////////////////////
    // External Link
    //////////////////////////////////////////////////    
    $(".edit_image_link").editable(_url_save_image_link_attrs, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata : function(value, settings) {
            return {target:  $('#image-link-upload #id').val(), core: _core_id, csrfmiddlewaretoken: _csrf_token };
        },
        charcounter : {
            characters : 255
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) != 'e~')
        	{
                $("#" + $("#image-link-upload #id").val() + " a" ).attr("href", value);
             	$("#" + $('#image-link-upload #id').val() + " .image_link_external").val(value);
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
    
});