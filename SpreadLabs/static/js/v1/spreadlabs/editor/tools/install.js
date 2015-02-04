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
    // StartUp
    //////////////////////////////////////////////////	
	$('#properties #general_object').click();

    //////////////////////////////////////////////////
    // OnClick installation
    //////////////////////////////////////////////////	
    $('#background').bind('mousedown', function(event) {
    	event.preventDefault();
    	event.stopPropagation();
    	
        $( "#preview .object" ).removeClass('ui-selected ui-selecting');
    	var $pretarget = $(event.target);
    	var $target = $pretarget.closest('.object');
        $target.addClass('ui-selected ui-selecting');
        
        $('#properties .block').hide();
        
        if ($target.hasClass('background')){
        	$( "#background-object" ).show();
        	$('#properties #this_object .name').html("Fondo");
        } else 
        if ($target.hasClass('image-link')) {
        	loadImageLink($target);
        	$( "#image-link-object" ).show();
        	$('#properties #this_object .name').html("Botón");
        } else 
        if ($target.hasClass('youtube')) {
            video = $target.find('input');
            $( "#youtube-object #id" ).val( $target.attr('id') );
            $( "#youtube-object #id_del" ).val( $target.attr('id') );
            $( "#youtube-object #video" ).text( video.val() );
        	$( "#youtube-object" ).show();
        	$('#properties #this_object .name').html("Video");
        } else 
        if ($target.hasClass('input')) {
        	loadInput($target);
        	$( "#input-object" ).show();
        	$('#properties #this_object .name').html("Formulario");
        }

        $('#properties #this_object').show();
        $('#properties #this_object').click();      
    });
    $('#background').bind('click',false);

    //////////////////////////////////////////////////
    // Hide properties
    //////////////////////////////////////////////////	
    function close_tools()
    {
        $( "#preview .object" ).removeClass('ui-selected ui-selecting');
        $('#properties #this_object').hide();
        $('#properties #general_object').click();
    }
    
    $(".border").click(function(event) {
    	event.preventDefault();
    	close_tools();
    });
    
    $("#tool-panel #delete").click(function(event) {
    	close_tools();
    });



});