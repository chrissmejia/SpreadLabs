
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

    $(window).scroll(function(){
        var aTop = $('#head').height();

        if($(this).scrollTop()>aTop){
            	if($("#main").css("margin-left") == rem(5) + "px"){
            		$("#breadcrumb").css({position: "fixed", top: "0px", "border-bottom-style":"solid", "z-index": "1000"});
            		$("#breadcrumb #mini_logo").css({"z-index": "1"});
                    $("#left_menu").css({"z-index": "-1"});
                    $("#breadcrumb").animate({ backgroundColor: '#fff'}, 1000).dequeue();
                    $("#main").animate({ marginLeft: '0px'}, 500, function function_name (arg) {
                        $(window).trigger('resize');
                    }).dequeue();
                    $("#mini_logo").animate({ marginLeft:  "-" + rem(0.9375) + "px"}, 500).dequeue(); // 0.9375 column padding
                }
            } else {
            	if($("#main").css("margin-left") == '0px'){
            		$("#breadcrumb").css({position: "relative", top: "0px", "border-bottom-style":"none", "z-index": "auto"});
                    $("#breadcrumb").animate({ backgroundColor: '#f3f3f3'}, 500).dequeue();
                    $("#breadcrumb #mini_logo").animate({ marginLeft: "-" + rem(10) + "px"}, 400, function function_name (arg) {
                		$("#breadcrumb #mini_logo").css({"z-index": "-1"});
                        $("#breadcrumb #mini_logo").css({ marginLeft: "-" + rem(6) + "px"});
                    }).dequeue();
                    $("#main").animate({ marginLeft: '5rem'}, 400, function function_name (arg) {
                        $("#left_menu").css({"z-index": "0"});
                        $(window).trigger('resize');
                    }).dequeue();
               }
            }
            $(window).trigger('resize');
        });


});