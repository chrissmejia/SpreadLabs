
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

    $(window).resize(function() {
        var header = rem(6);
        var content = $('#content').height();
        var footer = rem(6.4);
        var height = $(window).height();

        var free_space = height - (header + content + footer);
        var off_top = (free_space / 2) / rem(1);
        if (off_top < 1) {
            off_top = 3;
        }

        $('#content').css("padding-top", off_top + "rem");
        $('#content').css("padding-bottom", off_top + "rem");
        
    });
    $(window).resize();
});