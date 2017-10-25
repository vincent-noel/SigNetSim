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

{% include 'commons/js/forms.js' %}

let dropdown_unit = new Dropdown("compartment_unit");

// Value validator
let form_value = new FloatForm("compartment_size", "The size of the compartment", false);
let form_sbmlid = new SbmlIdForm("compartment_sbml_id", "The identifier of the compartment");

let form_sboterm = new SBOTermInput("compartment_sboterm");

$('#new_compartment_button').on('click', function(){

    new_compartment();
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

    form_value.clear();
    form_sbmlid.clear();

    $('#general').tab('show');
    $('#modal_compartment').modal('show');
    $("#modal_compartment").on('shown.bs.modal', function() { $("#compartment_name").focus(); });
}


function view_compartment(sbml_id)
{

    $("#modal_title").html("Edit compartment");

    ajax_call(
        "POST", "{% url 'get_compartment' %}",
        {'sbml_id': sbml_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "id") { $("#compartment_id").val(element.toString()); }
               else if (index == "sbml_id") { $("#compartment_sbml_id").val(element.toString()); form_sbmlid.setValue(element.toString()); }
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
                   $("#compartment_sboterm").val(element.toString());
                   $("#compartment_sboterm_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());
               }
               else if (index == "sboterm_name") { $("#compartment_sboterm_name").html(element.toString()); }
           });

           form_sbmlid.check();
           reset_errors();
        },
        function() { console.log("failed"); }
    )
    $("#general").tab('show');

    $('#modal_compartment').modal('show');
    $("#modal_compartment").on('shown.bs.modal', function() { $("#compartment_name").focus(); });

}
function reset_errors()
{
    form_sbmlid.unhighlight();
    form_value.unhighlight();
    $("#error_modal").empty();

}

function save_compartment()
{
    var nb_errors = 0;
    reset_errors();

    if (form_sbmlid.hasError()){
        add_error_modal_v3(form_sbmlid);
        form_sbmlid.highlight();
        nb_errors++;
    }
    if (form_value.hasError()){
        add_error_modal_v3(form_value);
        form_value.highlight();
        nb_errors++;
    }
    if (nb_errors == 0)
    {
        $("#modal_compartment").modal("hide");
    }
    return (nb_errors == 0);
}