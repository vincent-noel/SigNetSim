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


$('#unit_list li').on('click', function(){
  $("#compartment_unit_label").html($(this).text());
  $('#compartment_unit').val($(this).index());
});

$('#constant_list li').on('click', function(){
  $("#compartment_constant_label").html($(this).text());
  $('#compartment_constant').val($(this).index());
});

// Value validator

var form_value_error = "";

$("#compartment_size").on('paste keyup', function()
{
    if ($("#compartment_size").val() != "")
    {
        ajax_call(
            "POST", "{{csrf_token}}",
            "{% url 'float_validator' %}", {'value' : $("#compartment_size").val()},
            function(data) {
               $.each(data, function(index, element) {
                 if (index == "error") {form_value_error=element.toString();}
               });
            },
            function(){}
        );
    }
    else { form_value_error = "";}

});


// SbmlId Validation

var old_sbml_id = "";
var form_sbml_id_error = "";

function setSbmlIdEmpty()
{
  $("#sbmlid_invalid").removeClass("in");
  $("#sbmlid_validating").removeClass("in");
  $("#sbmlid_valid").removeClass("in");
}

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


$("#compartment_sbml_id").on('change paste keyup', function()
{
  new_sbml_id = $.trim($("#compartment_sbml_id").val());
  if (old_sbml_id === "" || new_sbml_id !== old_sbml_id)
  {
    setSbmlIdValidating();
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'sbml_id_validator' %}", {'sbml_id': new_sbml_id },
        function(data)
        {
            $.each(data, function(index, element) {
                if (index === 'error') {
                    setSbmlIdValid(); form_sbml_id_error = element.toString();
                }
            });
        },
        function()
        {
          setSbmlIdInvalid();
        }
    );
  }
});


$('#new_compartment_button').on('click', function(){

    new_compartment();
    $('#modal_compartment').modal('show');
});

function new_compartment()
{
    $("#modal_title").html("New compartment");
    $("#compartment_id").val("");
    $("#compartment_name").val("");
    $("#compartment_sbml_id").val("");
    $("#compartment_size").val(1);
    $("#compartment_unit_label").html("Choose a unit");
    $("#compartment_unit").val("");
    $("#compartment_constant_label").html("True");
    $("#compartment_constant").val(1);
    old_sbml_id = "";
    form_sbml_id_error = "";
    form_value_error = "";
    $('#general').tab('show');

}


function view_compartment(sbml_id)
{

    $("#modal_title").html("Edit compartment");

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_compartment' %}", {'sbml_id': sbml_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "id") { $("#compartment_id").val(element.toString()); }
               else if (index == "sbml_id") { $("#compartment_sbml_id").val(element.toString()); old_sbml_id=element; }
               else if (index == "name") { $("#compartment_name").val(element.toString()); }

               else if (index == "value") {
                   if (element == null) { $("#compartment_size").val(""); }
                   else { $("#compartment_size").val(element.toString()); }
               }

               else if (index == "unit_name") { $("#compartment_unit_label").html(element.toString()); }
               else if (index == "unit_id") { $("#compartment_unit").val(element.toString()); }

               else if (index == "constant") {
                   if (element == "1") { $("#compartment_constant").prop('checked', true); }
                   else { $("#compartment_constant").prop('checked', false); }
               }
               else if (index == "notes") {
                   $("#compartment_notes").val(element.toString());

               }
               else if (index == "sboterm") {
                   $("#sboterm").val(element.toString());
                   $("#sboterm_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());
               }
               else if (index == "sboterm_name") { $("#sboterm_name").html(element.toString()); }
           });

           setSbmlIdEmpty();
           reset_errors();
        },
        function() { console.log("failed"); }
    )
    $("#general").tab('show');
    $('#modal_compartment').modal('show');

}
function reset_errors()
{
   form_remove_error_highlight("compartment_sbml_id");
   form_remove_error_highlight("compartment_value");
   $("#error_modal").empty();

}

function save_compartment()
{
    var nb_errors = 0;
    reset_errors();

    if ($("#sbmlid_invalid").hasClass("in")){
        add_error_modal("invalid_sbml_id", "Compartment " + form_sbml_id_error);
        form_add_error_highlight("species_sbml_id");
        nb_errors++;
    }

    if (form_value_error != ""){
        add_error_modal("invalid_value", "Compartment value " + form_value_error);
        form_add_error_highlight("compartment_value");
        nb_errors++;
    }
    if (nb_errors == 0)
    {
        $("#compartment_form").submit();
    }
}