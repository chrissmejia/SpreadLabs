
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
	// Bar Style
    $(window).load(function(){
        $("#privacity ul").mCustomScrollbar();
        $("#pages .box").mCustomScrollbar();
    });


    $("#edit_box").mouseenter(function(event) {
        $('#edit_box').animate({ height: "280px" }, { duration: 'normal', complete: function () {
        	event.preventDefault();
        	$('#edit_box').css('overflow','');
        }}).dequeue();
    });
    
    
    $( "#edit_box" ).mouseleave(function() {
        $("#edit_box").animate({ height: "50px" }, 'normal').dequeue();
    });
    
    $( "#properties .menu a" ).click(function(event) {
    	event.preventDefault();
    	$( "#properties .menu .item" ).removeClass("current");
    	$(this).find(".item").addClass("current");
    	$("#panels").animate({ top: "-" + $(this).attr('href') + "px" }, 'normal').dequeue();
    });





    //////////////////////////////////////////////////
    // Resolution
    //////////////////////////////////////////////////	
    $('#resolution').chosen({
    	width:"100%",
    	no_results_text:'Opción no disponible'
    }).trigger("liszt:updated").change(function(event) 
    { 
    	$.post(_url_save_app_settings, { 
    		target: 'resolution',  
    		value: $("#resolution option:selected").val(), 
    		csrfmiddlewaretoken: _csrf_token 
    	})          	    
    	.done(function(data) {
            if (data.substring(0,2) == 'e~')
            {
           	    alert('Un error ha ocurrido' + data);
           	    window.location.reload();
            } 
            size = $("#resolution option:selected").val();
            size = size.split("x");
            $( "#background" ).css("width", size[0]);
            $( "#background" ).css("height", size[1]);
        })
        .fail(function() { 
           	alert('Un error ha ocurrido');
           	window.location.reload();
        });
    });
	
	
    //////////////////////////////////////////////////
    // Name
    //////////////////////////////////////////////////	
    $(".editname").editable(_url_save_description, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata: function(value, settings){
        	return {csrfmiddlewaretoken: _csrf_token };
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) == 'e~')
        	{
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        },
        charcounter : {
            characters : 100
        }
    });
	
	
    //////////////////////////////////////////////////
    // Description
    //////////////////////////////////////////////////	
    $(".editdescription").editable(_url_save_description, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata: function(value, settings){
        	return {csrfmiddlewaretoken: _csrf_token };
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) == 'e~')
        	{
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        },
        charcounter : {
            characters : 200
        }
    });



    //////////////////////////////////////////////////
    // Icon
    //////////////////////////////////////////////////	
    $("#icon-thumb").click(function(event) {
    	event.preventDefault();
    	$( "#icon-file" ).click();
    });

    $('#icon-upload').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#icon-thumb img" ).attr("src", data);
            	$('#icon-upload').get(0).reset();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
    $('#icon-file').change(function() {
        $('#icon-upload').submit();
    });
	
	
    //////////////////////////////////////////////////
    // Background
    //////////////////////////////////////////////////	
    $("#background-thumb").click(function(event) {
    	event.preventDefault();
    	$( "#background-file" ).click();
    });

    $('#background-upload').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#preview #background" ).css('background-image','url("'+data+'")');
            	$( "#background-thumb img" ).attr("src", data);
            	$('#background-upload').get(0).reset();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
    $('#background-file').change(function() {
        $('#background-upload').submit();
    });
    
    ///////////////////////////////////////////////// Delete background

    $('#background-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#preview #background" ).css('background-image','');
            	$( "#background-thumb img" ).attr("src", '/');
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
	
	
    //////////////////////////////////////////////////
    // Pattern
    //////////////////////////////////////////////////	
    $("#pattern-thumb").click(function(event) {
    	event.preventDefault();
    	$( "#pattern-file" ).click();
    });

    $('#pattern-upload').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#preview .border" ).css('background-image','url("'+data+'")');
            	$( "#pattern-thumb img" ).attr("src", data);
            	$('#pattern-upload').get(0).reset();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });
    
    $('#pattern-file').change(function() {
        $('#pattern-upload').submit();
    });
    
    ///////////////////////////////////////////////// Delete pattern

    $('#pattern-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#preview #pattern" ).css('background-image','');
            	$( "#pattern-thumb img" ).attr("src", '/');
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });    
    
    
    
    
});

