{#   _layout/base.html : This is the top template 							  #}

{#   Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br) 		  #}

{#   This program is free software: you can redistribute it and/or modify     #}
{#   it under the terms of the GNU Affero General Public License as published #}
{#   by the Free Software Foundation, either version 3 of the License, or     #}
{#   (at your option) any later version. 									  #}

{#   This program is distributed in the hope that it will be useful, 		  #}
{#   but WITHOUT ANY WARRANTY; without even the implied warranty of 		  #}
{#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 			  #}
{#   GNU Affero General Public License for more details.					  #}

{#   You should have received a copy of the GNU Affero General Public License #}
{#   along with this program. If not, see <http://www.gnu.org/licenses/>. 	  #}


$('#species_list li').on('click', function(){
  $("#species_name").html($(this).text());
  $('#species_id').val($(this).index());
});

let form_snapshot = new SliderForm("simulation_model_snapshot", "Model snapshot switch", 1, null);


$('#toggle_options').on('click', function(){

  if($("#options").hasClass("in")) {
    $("#options").removeClass("in");
    $("#options_2").removeClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-down\"> More");

  } else {
    $("#options").addClass("in");
    $("#options_2").addClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-up\"> Less");
  }
});

$('#experiment_list li').on('click', function(){
  $("#experiment_name").html($(this).text());
  $('#experiment_id').val($(this).index());
  $("#experiment_selected").addClass("in");

});

{% if form.showObservations == True %}
	let form_observations = new SliderForm("show_observations", "Show observation switch", 1, null);
{% else %}
	let form_observations = new SliderForm("show_observations", "Show observation switch", 0, null);
{% endif %}