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

{% load bootstrap3 %}
{% load tags %}


$('#unit_list li').on('click', function(){
  $("#species_unit_label").html($(this).text());
  $('#species_unit').val($(this).index());
});


$('#species_compartment_dropdown li').on('click', function(){
  $("#species_compartment_label").html($(this).text());
  $('#species_compartment').val($(this).index());
});


$('#new_species_button').on('click', function(){

    $("#modal_title").html("New species");
    $("#species_id").attr("value", "");
    $("#species_name").attr("value", "");
    $("#species_sbml_id").attr("value", "");
    $("#species_value").attr("value", "");
    {% if list_of_compartments|my_len == 1 %}
    $("#species_compartment_label").html("{{list_of_compartments|my_lookup:0}}");
    $("#species_compartment").attr("value", "0");
    {% else %}
    $("#species_compartment_label").html("Choose a compartment");
    $("#species_compartment").attr("value", "");
    {% endif %}
    $("#species_unit_label").html("Choose a unit");
    $("#species_unit").attr("value", "");
    $("#species_constant").attr("value", 0);
    $("#species_boundary").attr("value", 0);
    $('#modal_species').modal('show');

});

function toggle_slide(slide_id) {
  if ($('#' + slide_id).prop('checked') == true) {
    $('#' + slide_id).prop("checked", false);
  } else {
    $('#' + slide_id).prop("checked", true);
  }
}


// SbmlId Validation

var old_sbml_id = "{% if form.isEditing == True and form.sbmlId != None %}{{form.sbmlId}}{% endif %}";

function setSbmlIdValid()
{
  $("#sbmlid_invalid").removeClass("in");
  $("#sbmlid_validating").removeClass("in");
  $("#sbmlid_valid").addClass("in");
}

function setSbmlIdInvalid()
{
  $("#sbmlid_validating").removeClass("in");
  $("#sbmlid_valid").removeClass("in");
  $("#sbmlid_invalid").addClass("in");
}

function setSbmlIdValidating()
{
  $("#sbmlid_invalid").removeClass("in");
  $("#sbmlid_valid").removeClass("in");
  $("#sbmlid_validating").addClass("in");
}


$("#species_sbml_id").on('change paste keyup', function()
{
  new_sbml_id = $.trim($("#species_sbml_id").val());
  if (old_sbml_id === "" || new_sbml_id !== old_sbml_id)
  {
    setSbmlIdValidating();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{csrf_token}}");
            }
        }
    });
    $.ajax(
    {
        type: "POST",
        url: '{% url 'sbml_id_validator' %}',
        data: {
            'sbml_id': new_sbml_id,
        },

    })
    .done(function(data)
    {
       $.each(data, function(index, element) {
         if (index === 'valid' && element === 'true') {
           setSbmlIdValid();
         } else {
           setSbmlIdInvalid();
         }
       });
    })
    .fail(function()
    {
      setSbmlIdInvalid();
    })
  }
  else if (new_sbml_id === old_sbml_id)
  {
    setSbmlIdValid();
  }
});



{% if form.hasErrors == True or form.isEditing == True %}
    $(window).on('load',function(){
        $('#modal_species').modal('show');
    });
{% endif %}
