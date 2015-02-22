
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

$( document ).ready(function() {
    var rem = function (count) {
        var unit = $('html').css('font-size');

        if (typeof count !== 'undefined' && count > 0)
        {
            return (parseInt(unit) * count);
        }
        else
        {
            return parseInt(unit);
        }
    };

    $(window).scroll(function() {
        var aTop = $('#head').height();

        if($(this).scrollTop()>aTop){
            if($("#main").css("left") == rem(5) + "px"){
                $("#main").addClass("full");
            }
        } else {
            if($("#main").css("left") == '0px'){
                $("#main").removeClass("full");
               }
            }
        });
        $(window).trigger('resize');
});