{% comment %}

 Copyright (C) 2016-2018 Vincent Noel (contact@vincent-noel.fr)

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.

{% endcomment %}

{% if model_id != None %}


$('#species_list li').on('click', function(){
  $("#species_name").html($(this).text());
  $('#species_id').val($(this).index());
});

{% endif %}
{{ block.super }}


$('#toggle_options').on('click', function(){

  if($("#options").hasClass("in")) {
    $("#options").removeClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-down\"> More");

  } else {
    $("#options").addClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-up\"> Less");
  }
});

let form_snapshot = new SliderForm("simulation_model_snapshot", "Model snapshot switch", 1, null);