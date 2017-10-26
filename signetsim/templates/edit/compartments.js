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

{% include 'commons/js/sbmlid_form.js' %}
{% include 'commons/js/float_form.js' %}
{% include 'commons/js/sboterm_input.js' %}


let form_group = new FormGroup();

let dropdown_unit = new Dropdown("compartment_unit", post_treatment=null, default_value="", default_label="Choose an unit");
form_group.addForm(dropdown_unit);

let form_value = new FloatForm("compartment_size", "The size of the compartment", false, default_value=1);
form_group.addForm(form_value, error_checking=true);

let form_sbmlid = new SbmlIdForm("compartment_sbml_id", "The identifier of the compartment", default_value="");
form_group.addForm(form_sbmlid, error_checking=true);

let form_sboterm = new SBOTermInput("compartment_sboterm");
form_group.addForm(form_sboterm);

function modal_show()
{
    $('#general').tab('show');
    $('#modal_compartment').modal('show');
    $("#modal_compartment").on('shown.bs.modal', () => { $("#compartment_name").focus(); });
}
function new_compartment()
{
    $("#modal_title").html("New compartment");
    $("#compartment_id").val("");
    $("#compartment_name").val("");
    $("#compartment_constant").val(1);

    form_group.clearForms();
    modal_show();
}

function view_compartment(sbml_id)
{

    $("#modal_title").html("Edit compartment");

    ajax_call(
        "POST", "{% url 'get_compartment' %}",
        {'sbml_id': sbml_id},
        (data) =>
        {
           $.each(data, (index, element) =>
           {
               if (index == "id") {
                   $("#compartment_id").val(element.toString());

               } else if (index == "sbml_id") {
                   form_sbmlid.setValue(element.toString());
                   form_sbmlid.setInitialValue(element.toString());

               } else if (index == "name") {
                   $("#compartment_name").val(element.toString());

               } else if (index == "value") {
                   if (element == null) { $("#compartment_size").val(""); }
                   else { $("#compartment_size").val(element.toString()); }

               } else if (index == "unit_name") {
                   dropdown_unit.setLabel(element.toString());

               } else if (index == "unit_id") {
                   dropdown_unit.setValue(element.toString());

               } else if (index == "constant") {
                   if (element == "1") { $("#compartment_constant").prop('checked', true); }
                   else { $("#compartment_constant").prop('checked', false); }

               } else if (index == "notes") {
                   $("#compartment_notes").val(element.toString());

               } else if (index == "sboterm") {
                   form_sboterm.setValue(element.toString());
                   form_sboterm.setLink(element.toString());

               } else if (index == "sboterm_name") {
                   form_sboterm.setName(element.toString());
               }
           });

           form_sbmlid.check();
           form_group.resetErrors();
        },
        () => { console.log("compartment data retrieving failed"); }
    )

    modal_show();

}

function save_compartment()
{
    form_group.checkErrors();

    if (form_group.nb_errors == 0)
    {
        $("#modal_compartment").modal("hide");
    }

    return (form_group.nb_errors == 0);
}