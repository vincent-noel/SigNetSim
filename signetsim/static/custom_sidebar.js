/******************************************************************************
 *                                                                            *
 *   Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)           *
 *                                                                            *
 *   plsa is free software: you can redistribute it and/or modify             *
 *   it under the terms of the GNU Affero General Public License as published *
 *   by the Free Software Foundation, either version 3 of the License, or     *
 *   (at your option) any later version.                                      *
 *                                                                            *
 *   plsa is distributed in the hope that it will be useful,                  *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of           *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            *
 *   GNU Affero General Public License for more details                       *
 *                                                                            *
 *   You should have received a copy of the GNU General Affero Public License *
 *   along with plsa. If not, see <http://www.gnu.org/licenses/>.             *
 *                                                                            *
 ******************************************************************************/
$("#sidebar-toggle").click(function(e)
{
	$("#wrapper").toggleClass("toggled");

	if ($("#wrapper").hasClass("toggled")) {
		if ($(window).width() < 500){

		  $(".content").css({ "display": "none" });
		} else {
		  $(".content").css({ "width": ($(window).width() - $("#sidebar").width() - 1) + "px" });
		}
	} else {
	  if ($(window).width() < 500){

		$(".content").css({ "display": "inherit" });
	  } else {
		$(".content").css({ "width": "100%" });
	  }
	}
});


if (document.getElementById("sidebar").scrollHeight > document.getElementById("content").scrollHeight){
  $("#sidebar").css({ "height": (Math.max(document.getElementById("wrapper").scrollHeight, ($(document).height() - $("#navbar-fixed-top").height())) - $("#navbar-fixed-top").height() - 1) + "px" });

} else {
  $("#sidebar").css({ "height": (Math.max(document.getElementById("wrapper").scrollHeight, $(document).height()) - $("#navbar-fixed-top").height() - 1) + "px" });

}

$(window).on('resize', function () {

  $("#cy").css({ height: $(window).height() - $(".navbar-header").height() - 150 + "px" });
  $("#stoichiometry_graph").css({ height: $(window).height() - $(".navbar-header").height() - 150 + "px" });

  if (document.getElementById("sidebar").scrollHeight > document.getElementById("content").scrollHeight){
	$("#sidebar").css({ "height": (Math.max(document.getElementById("wrapper").scrollHeight, ($(document).height() - $("#navbar-fixed-top").height())) - 1) + "px" });

  } else {
	$("#sidebar").css({ "height": (Math.max(document.getElementById("wrapper").scrollHeight, $(document).height()) - $("#navbar-fixed-top").height() - 1) + "px" });

  }
});
