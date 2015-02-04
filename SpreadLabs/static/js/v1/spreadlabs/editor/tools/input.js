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
$(document).ready(function()
{
    jQuery.fn.exists = function(){return this.length>0;};
});    

function loadInput(tag)
{
    $(document).ready(function()
    {        
    	$("#input-object #type").html("");
    	if (!$(".input #name").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "name").val("name").text("Nombre"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "name").val("name").text("Nombre"));    		
    	}
    	if (!$(".input #lastname").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "lastname").val("lastname").text("Apellidos"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "lastname").val("lastname").text("Apellidos"));
    	}
    	if (!$(".input #email").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "email").val("email").text("Correo"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "email").val("email").text("Correo"));
    	}
    	if (!$(".input #id").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "id").val("id").text("Cédula"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "id").val("id").text("Cédula"));
    	}
    	if (!$(".input #cellphone").exists())
    	{	
    		$("#input-object #type").append($("<option />").attr("id", "cellphone").val("cellphone").text("Celular"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "cellphone").val("cellphone").text("Celular"));
    	}
    	if (!$(".input #year_of_birth").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "year_of_birth").val("year_of_birth").text("Año de nacimiento"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "year_of_birth").val("year_of_birth").text("Año de nacimiento"));
    	}
    	if (!$(".input #birth_month").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "birth_month").val("birth_month").text("Mes de nacimiento"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "birth_month").val("birth_month").text("Mes de nacimiento"));
    	}
    	if (!$(".input #day_of_birth").exists())
    	{
    		$("#input-object #type").append($("<option />").attr("id", "day_of_birth").val("day_of_birth").text("Día de nacimiento"));
    	} else {
    		$("#input-object #type").append($("<option disabled />").attr("id", "day_of_birth").val("day_of_birth").text("Día de nacimiento"));
    	}
        $("#input-object #type").append($("<option />").attr("id", "custom").val("custom").text("Personalizado"));
    	
    	
    	$("#input-object #type").find('#'+ tag.find('input').attr('id') ).attr('selected',true);
    	$("#input-object #type").find('#'+ tag.find('input').attr('id')).removeAttr("disabled");
    	
        $('#type').trigger("liszt:updated");
    	
    	$('#input-object #slider').slider('value', parseInt(tag.find('input').css("font-size")));

        $("#input-object #color").spectrum("set", tag.find('.color').val());
        default_text = tag.find('input').val();
        if (!default_text) { default_text = "Click para editar"; }
    	$("#input-object #default").text( default_text );
        $("#input-object #default_color").spectrum("set", tag.find('.default_color').val());
        $("#input-object #error_color").spectrum("set", tag.find('.error_color').val());
        
        $("#input-object #transparent").prop('checked', tag.find('input').hasClass('transparent'));

    	$("#input-delete #id_del").val(tag.attr('id'));

        loadInputRestrictions(tag);
    });    
    	
}


function loadInputRestrictions(tag)
{
    $(document).ready(function()
    {

        $(".custom-name").hide();
        $(".custom-type").hide();
        $(".custom-size").hide();
//        $(".custom-required").hide();

        if (tag.find('.type').val() == "cellphone"){
        	$(".custom-size").show();
        } else if (tag.find('.type').val() == "custom"){
            $(".custom-name").show();
            $(".custom-type").show();
            $(".custom-size").show();
        }
        
        if (tag.find('.required').val() == "True") {
        	required = true;
        } else {
        	required = false;
        }
        $("#input-object #required").prop('checked', required);
        $("#input-object #custom_name").text(tag.find('.custom_name').val());
        
    	$("#input-object #select_type").find('#'+ tag.find('.custom_type').val() ).attr('selected',true);
    	$("#input-object #select_type").find('#'+ tag.find('.custom_type').val() ).attr("disabled");
    	$('#select_type').trigger("liszt:updated");

        $("#input-object #custom_size_slider").slider('values',0,tag.find('.min_characters').val());
        $("#input-object #custom_size_slider").slider('values',1,tag.find('.max_characters').val());
        $( "#custom_size_amount" ).text( "Entre " +  $( "#custom_size_slider" ).slider( "values", 0 ) + " y " + $( "#custom_size_slider" ).slider( "values", 1 ) + " carácteres" );

//        $("#input-object #custom_name").text(tag.find('.custom_name').val());
        
    });    
    	
}



//////////////////////////////////////////////////
//////////////////////////////////////////////////
// DRAGGABLE
//////////////////////////////////////////////////
//////////////////////////////////////////////////
function draggable_input()
{
    $(document).ready(function()
    {
        $( ".drag_input" ).draggable({ 
	        containment: "#background", 
		    scroll: false,
		    cancel: null,
		    stop: function(event, ui) {
          	    $.post(_url_save_input_position, { id: this.id, left: $(this).position().left, top: $(this).position().top, core: _core_id, csrfmiddlewaretoken: _csrf_token  })
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
draggable_input();


//////////////////////////////////////////////////
//////////////////////////////////////////////////
// RESIZABLE
//////////////////////////////////////////////////
//////////////////////////////////////////////////
function resizable_input()
{
    $(document).ready(function()
    {
        $( ".input .input" ).resizable({ 
        	handles: "e",
        	ghost: true,
        	stop: function(event, ui) {
                $(".input .ui-wrapper").css("height", "");
                $(".input .input").css("height", "");
                $.post(_url_save_input_attrs, { id: "width", target: $('#input-delete #id_del').val(), core: _core_id, value: $(this).width(), csrfmiddlewaretoken: _csrf_token  });
            }
        });
        $(".input .ui-wrapper").css("height", "");
        $(".input .ui-wrapper").css("width", "");
        $(".input .ui-wrapper").css("padding-right", "");
        $(".input .input").css("height", "");
    });    
}
resizable_input();




//////////////////////////////////////////////////
//////////////////////////////////////////////////
// NEW
//////////////////////////////////////////////////
//////////////////////////////////////////////////

$(document).ready(function()
{
/*    function input_full_check()
    {
        if ($(".input #name").exists() && $(".input #lastname").exists() && $(".input #email").exists() && $(".input #id").exists() && $(".input #cellphone").exists() && $(".input #year_of_birth").exists() && $(".input #birth_month").exists() && $(".input #day_of_birth").exists())
        {
        	$('#tool-input img').attr("src", _static+"images/v1/menu/sub/edit_disabled.png");
        	$('#tool-input').addClass('disabled');
        } else
        {
        	$('#tool-input img').attr("src", _static+"images/v1/menu/sub/edit.png");
        	$('#tool-input').removeClass('disabled');        	
        }
    };
    input_full_check();
*/    
    // Input New
    $('#tool-input').click(function(){
    	event.preventDefault();
    	
    	if (!$('#tool-input').hasClass("disabled"))
    	{
    		
        	var type = '';
        	if (!$(".input #name").exists())
        	{
        		type = 'name';
        	} else if (!$(".input #lastname").exists())
        	{
        		type = 'lastname';
        	} else if (!$(".input #email").exists())
        	{
        		type = 'email';	
        	} else if (!$(".input #id").exists())
        	{
        		type = 'id';
        	} else if (!$(".input #cellphone").exists())
    	    {
    	    	type = 'cellphone';
        	} else if (!$(".input #year_of_birth").exists())
        	{
        		type = 'year_of_birth';  
        	} else if (!$(".input #birth_month").exists())
        	{
        		type = 'birth_month';
        	} else if (!$(".input #day_of_birth").exists())
        	{
        		type = 'day_of_birth';
        	} else {
        		type = 'custom';        		
        	}
    	
        	$.post(_url_save_input, { id: "new", core: _core_id, type: type, csrfmiddlewaretoken: _csrf_token  })
            .done(function(data) {
                if (data.substring(0,2) == 'e~')
                {
               	    alert('Un error ha ocurrido');
               	    window.location.reload();
                } else {
                    $('#background').append('<div id="input_'+data+'" class="drag_input object tool input">'+
                                                '<input id="'+type+'" class="input" type="text" name="'+type+'" value=""  style="width:300px; font-size:12px; color:#C0C0C0;">'+
                                                '<input class="hidden type" type="hidden" name="type" value="'+type+'">'+
                                                '<input class="hidden color" type="hidden" name="color" value="#000000">'+
                                                '<input class="hidden default_color" type="hidden" name="default_color" value="#C0C0C0">'+
                                                '<input class="hidden error_color" type="hidden" name="error_color" value="#DD1010">'+
                                          	    '<input class="hidden custom_name" type="hidden" name="custom_name" value="">'+
                                          	    '<input class="hidden custom_type" type="hidden" name="custom_type" value="text">'+
                                          	    '<input class="hidden min_characters" type="hidden" name="min_characters" value="1">'+
                                        	    '<input class="hidden max_characters" type="hidden" name="max_characters" value="1">'+
        	                                    '<input class="hidden required" type="hidden" name="required" value="True">'+
                                            '</div>');
                $("#input_"+ data).mousedown();
                    draggable_input();
                    resizable_input();
//            		input_full_check();
                }
            });
        
        }

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
    $('#type').chosen({
    	width:"100%",
    	no_results_text:'Opción no disponible'
    }).trigger("liszt:updated").change(function(event) 
    { 
        $("#" + $('#input-delete #id_del').val() + " .input").attr('id', $("#type option:selected").val());
    	$.post(_url_save_input_attrs, {
    		id: "type", 
    		target: $("#input-delete #id_del").val(), 
    		core: _core_id, 
    		value: $("#type option:selected").val(),
    		csrfmiddlewaretoken: _csrf_token 
    	})
    	.done(function(data) {
            if (data.substring(0,2) == 'e~')
            {
           	    alert('Un error ha ocurrido' + data);
           	    window.location.reload();
            } else {
            	$( "#" + $( "#input-delete #id_del" ).val() ).find('.type').val($("#type option:selected").val());
            	loadInputRestrictions($( "#" + $( "#input-delete #id_del" ).val() ));
            	
            }
        })
        .fail(function() { 
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
        });
    });	


    //////////////////////////////////////////////////
    // Select Type
    //////////////////////////////////////////////////	
    $('#select_type').chosen({
    	width:"100%",
    	no_results_text:'Opción no disponible'
    }).trigger("liszt:updated").change(function(event) 
    { 
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.custom_type').val($("#select_type option:selected").val());
    	$.post(_url_save_input_attrs, {
    		id: "custom_type", 
    		target: $("#input-delete #id_del").val(), 
    		core: _core_id, 
    		value: $("#select_type option:selected").val(),
    		csrfmiddlewaretoken: _csrf_token 
    	})
    	.done(function(data) {
            if (data.substring(0,2) == 'e~')
            {
           	    alert('Un error ha ocurrido' + data);
           	    window.location.reload();
            } else {
            	$( "#" + $( "#input-delete #id_del" ).val() ).find('.type').val($("#type option:selected").val());
            	loadInputRestrictions($( "#" + $( "#input-delete #id_del" ).val() ));
            	
            }
        })
        .fail(function() { 
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
        });
    });	
	
    ///////////////////////////////////////////////// Delete input
    $('#input-delete').ajaxForm({
        beforeSubmit: function() {
        },
        success: function(data) {
        	if (data.substring(0,2) != 'e~')
        	{
            	$( "#" + $( "#input-delete #id_del" ).val() ).remove();
            	input_full_check();
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });

    //////////////////////////////////////////////////
    // Text Size
    //////////////////////////////////////////////////	
    $( "#slider" ).slider({
      value:12,
      min: 8,
      max: 72,
      step: 2,
      slide: function( event, ui ) {
      	$( "#amount" ).css({'font-size':ui.value});
        $( "#amount" ).text( ui.value );
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css({'font-size':ui.value});
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.ui-wrapper').height(ui.value + (ui.value / 3) + 6);
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("padding-left", (ui.value / 3));
      },
      change: function(e, ui) {
      	$( "#amount" ).css({'font-size':ui.value});
        $( "#amount" ).text( ui.value );
        $.post(_url_save_input_attrs, { id: "size", target: $('#input-delete #id_del').val(), core: _core_id, value: ui.value, csrfmiddlewaretoken: _csrf_token  });
      }
    });
    $( "#amount" ).text( $( "#slider" ).slider( "value" ) );


    //////////////////////////////////////////////////
    // Text Colors
    //////////////////////////////////////////////////	
    $("#color").spectrum({
        color: "#000000",
        showInitial: true,
        showInput: true,
        showButtons: false,
        clickoutFiresChange: true,
        change: function(color) {
        	$( "#" + $( "#input-delete #id_del" ).val() ).find('.color').val(color.toHexString());
            $.post(_url_save_input_attrs, { id: "color", target: $('#input-delete #id_del').val(), core: _core_id, value: color.toHexString(), csrfmiddlewaretoken: _csrf_token  });
        }
    });

    $("#default_color").spectrum({
        color: "#C0C0C0",
        showInitial: true,
        showInput: true,
        showButtons: false,
        clickoutFiresChange: true,
        change: function(color) {
        	$( "#" + $( "#input-delete #id_del" ).val() ).find('.default_color').val(color.toHexString());
        	$( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("color", color.toHexString());
            $.post(_url_save_input_attrs, { id: "default_color", target: $('#input-delete #id_del').val(), core: _core_id, value: color.toHexString(), csrfmiddlewaretoken: _csrf_token  });
        }
    });

    $("#error_color").spectrum({
        color: "#DD1010",
        showInitial: true,
        showInput: true,
        showButtons: false,
        clickoutFiresChange: true,
        change: function(color) {
        	$( "#" + $( "#input-delete #id_del" ).val() ).find('.error_color').val(color.toHexString());
            $.post(_url_save_input_attrs, { id: "error_color", target: $('#input-delete #id_del').val(), core: _core_id, value: color.toHexString(), csrfmiddlewaretoken: _csrf_token  });
        }
    });


    //////////////////////////////////////////////////
    // Default Text
    //////////////////////////////////////////////////	
    $(".edit_default").editable(_url_save_input_attrs, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata : function(value, settings) {
            return {target:  $('#input-delete #id_del').val(), core: _core_id, csrfmiddlewaretoken: _csrf_token };
        },
        charcounter : {
            characters : 255
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) != 'e~')
        	{
                $( "#" + $('#input-delete #id_del').val()  + " .input").val(value);
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });


    //////////////////////////////////////////////////
    // Custom Name
    //////////////////////////////////////////////////	
    $(".edit_custom_name").editable(_url_save_input_attrs, { 
        indicator : "<img src='"+_static+"images/loader.gif'>",
        type      : "charcounter",
        tooltip   : "Click para editar...",
        onblur    : "submit",
        submitdata : function(value, settings) {
            return {target:  $('#input-delete #id_del').val(), core: _core_id, csrfmiddlewaretoken: _csrf_token };
        },
        charcounter : {
            characters : 255
        },
        callback : function(value, settings) {
        	if (value.substring(0,2) != 'e~')
        	{
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.custom_name').val(value);
            } else {
           	    alert('Un error ha ocurrido');
           	    window.location.reload();
            }
        }
    });

    //////////////////////////////////////////////////
    // Transparent
    //////////////////////////////////////////////////	
    $('#input-object #transparent').change(function () {
            if ($(this).is(':checked'))
            {
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("border", "dotted 1px");
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("background-color", "rgba(255, 255, 255, 0.3)");
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').addClass('transparent');	
            } else 
            {
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("border", "2px inset");    	
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').css("background-color", "#ffffff");    	
                $( "#" + $( "#input-delete #id_del" ).val() ).find('.input').removeClass('transparent');	
            }
            $.post(_url_save_input_attrs, { id: "transparent", target: $('#input-delete #id_del').val(), core: _core_id, value: $(this).is(':checked'), csrfmiddlewaretoken: _csrf_token })
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
    // transparent fix
    $( ".input .transparent" ).css("border", "dotted 1px");  
    $( ".input .transparent" ).css("background-color", "rgba(255, 255, 255, 0.3)");    


    //////////////////////////////////////////////////
    // Required
    //////////////////////////////////////////////////	
    $('#input-object #required').change(function () {
            $( "#" + $( "#input-delete #id_del" ).val() ).find('.required').val($(this).is(':checked'));
            $.post(_url_save_input_attrs, { id: "required", target: $('#input-delete #id_del').val(), core: _core_id, value: $(this).is(':checked'), csrfmiddlewaretoken: _csrf_token })
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
    // Text Count
    //////////////////////////////////////////////////	
    $( "#custom_size_slider" ).slider({
      range: true,
      value:0,
      min: 1,
      max: 72,
      slide: function( event, ui ) {
        $( "#custom_size_amount" ).text( "Entre " + ui.values[ 0 ] + " y " + ui.values[ 1 ] + " carácteres");
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.min_characters').val( ui.values[ 0 ]);
        $( "#" + $( "#input-delete #id_del" ).val() ).find('.max_characters').val( ui.values[ 1 ]);
      },
      change: function(e, ui) {
//        $( "#amount" ).text( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        $.post(_url_save_input_attrs, { id: "characters", target: $('#input-delete #id_del').val(), core: _core_id, value: ui.values[ 0 ] + "-" + ui.values[ 1 ], csrfmiddlewaretoken: _csrf_token  });
      }
    });
    $( "#custom_size_amount" ).text( "Entre " +  $( "#custom_size_slider" ).slider( "values", 0 ) + " y " + $( "#custom_size_slider" ).slider( "values", 1 ) + " carácteres" );
    
	
});
