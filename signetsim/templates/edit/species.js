{% comment %}

 Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

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

{% load bootstrap3 %}
{% load tags %}

class SpeciesForm extends FormGroup{

    constructor(field){
        super();
        this.field = field;

        this.form_value_type = new Dropdown("species_value_type", null, "1", "Concentration");
        this.addForm(this.form_value_type);

        this.form_units = new Dropdown("species_unit", null, "", "Choose an unit");
        this.addForm(this.form_units);

        this.form_compartment = new Dropdown("species_compartment", null, "0", "{{ list_of_compartments|my_lookup:0 }}");
        this.addForm(this.form_compartment);

        this.form_sbmlid = new SbmlIdForm("species_sbml_id", "The identifier of the species", "");
        this.addForm(this.form_sbmlid, true);

        this.form_value = new FloatForm("species_value", "The initial value of the species", false, "0");
        this.addForm(this.form_value, true);

        this.form_sboterm = new SBOTermInput("species_sboterm");
        this.addForm(this.form_sboterm);

        this.form_constant = new SliderForm("species_constant", "The constant setting of the species", 0);
        this.addForm(this.form_constant);

        this.form_boundary = new SliderForm("species_boundary", "The boundary value setting of the species", 0);
        this.addForm(this.form_boundary);

        this.form_notes = new Form("species_notes", "The notes of the species", "");
        this.addForm(this.form_notes);

        this.form_id = new Form("species_id", "The id of the species", "");
        this.addForm(this.form_id);

        this.form_name = new Form("species_name", "The name of the species", "");
        this.addForm(this.form_name);
    }

    show(){
        $("#general").tab('show');
        $("#" + this.field).on('shown.bs.modal', () => { $("#species_name").focus(); });
        $('#' + this.field).modal('show');
    }

    new(){
        $("#modal_title").html("New species");
        this.clearForms();
        this.show();
    }

    load(sbml_id){
        $("#modal_title").html("Edit species");

        ajax_call(
            "POST",
            "{% url 'get_species' %}", {'sbml_id': sbml_id},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                   if (index == "id") {
                       this.form_id.setValue(element.toString());

                   } else if (index == "sbml_id") {
                       this.form_sbmlid.setValue(element.toString());
                       this.form_sbmlid.setInitialValue(element.toString());

                   } else if (index == "name") {
                       this.form_name.setValue(element.toString());

                   } else if (index == "value") {
                       if (element == null) { this.form_value.setValue(""); }
                       else { this.form_value.setValue(element.toString()); }

                   } else if (index == "compartment_name") {
                       this.form_compartment.setLabel(element.toString());

                   } else if (index == "compartment_id") {
                       this.form_compartment.setValue(element.toString());

                   } else if (index == "unit_name") {
                       this.form_units.setLabel(element.toString());

                   } else if (index == "unit_id") {
                       this.form_units.setValue(element.toString());

                   } else if (index == "constant") {
                       if (element == "1") {
                           this.form_constant.switch_on();
                       } else {
                           this.form_constant.switch_off();
                       }

                   } else if (index == "boundaryCondition") {
                       if (element == "1") { this.form_boundary.switch_on(); }
                       else { this.form_boundary.switch_off(); }

                   } else if (index == "isConcentration") {

                       this.form_value_type.setValue(element.toString());
                       if (element == "1") {
                           this.form_value_type.setLabel("Concentration");
                       }
                       else {
                           this.form_value_type.setLabel("Amount");
                       }

                   }  else if (index == "notes") {
                       this.form_notes.setValue(element.toString());

                   } else if (index == "sboterm") {
                       this.form_sboterm.setValue(element.toString());
                       this.form_sboterm.setLink(element.toString());

                   } else if (index == "sboterm_name") {
                       this.form_sboterm.setLabel(element.toString());
                   }
               });

               this.checkErrors();
            },
            () => { console.log("failed"); }
        )

        this.show();
    }

    save()
    {
        this.checkErrors();
        if (this.nb_errors == 0)
        {
            $("#modal_species").modal("hide");
        }

        return (this.nb_errors == 0);
    }
}

{##}
{#let form_group = new FormGroup();#}
{##}
{#let form_value_type = new Dropdown("species_value_type", post_treatment=null, default_value="1", default_label="Concentration");#}
{#form_group.addForm(form_value_type);#}
{##}
{#let form_units = new Dropdown("species_unit", post_treatment=null, default_value="", default_label="Choose an unit");#}
{#form_group.addForm(form_units);#}
{##}
{#let form_compartment = new Dropdown("species_compartment", post_treatment=null, default_value="0", default_value="{{ list_of_compartments|my_lookup:0 }}");#}
{#form_group.addForm(form_compartment);#}
{##}
{#let form_sbmlid = new SbmlIdForm("species_sbml_id", "The identifier of the species", default_value="");#}
{#form_group.addForm(form_sbmlid, error_checking=true);#}
{##}
{#let form_value = new FloatForm("species_value", "The initial value of the species", false, default_value="0");#}
{#form_group.addForm(form_value, error_checking=true);#}
{##}
{#let form_sboterm = new SBOTermInput("species_sboterm");#}
{#form_group.addForm(form_sboterm);#}
{##}
{#let form_constant = new SliderForm("species_constant", "The constant setting of the species", default_value=0);#}
{#form_group.addForm(form_constant);#}
{##}
{#let form_boundary = new SliderForm("species_boundary", "The boundary value setting of the species", default_value=0);#}
{#form_group.addForm(form_boundary);#}
{##}
{#let form_notes = new Form("species_notes", "The notes of the species", default_value="");#}
{#form_group.addForm(form_notes);#}
{##}
{#let form_id = new Form("species_id", "The id of the species", default_value="");#}
{#form_group.addForm(form_id);#}
{##}
{#let form_name = new Form("species_name", "The name of the species", default_value="");#}
{#form_group.addForm(form_name);#}
{##}
{#function modal_show()#}
{#{#}
{#    $("#general").tab('show');#}
{#    $("#modal_species").on('shown.bs.modal', () => { $("#species_name").focus(); });#}
{#    $('#modal_species').modal('show');#}
{#}#}
{##}
{#function new_species()#}
{#{#}
{#    $("#modal_title").html("New species");#}
{#    form_group.clearForms();#}
{#    modal_show();#}
{#}#}
{##}
{#function view_species(sbml_id)#}
{#{#}
{##}
{#    $("#modal_title").html("Edit species");#}
{##}
{#    ajax_call(#}
{#        "POST",#}
{#        "{% url 'get_species' %}", {'sbml_id': sbml_id},#}
{#        (data) =>#}
{#        {#}
{#           $.each(data, (index, element) =>#}
{#           {#}
{#               if (index == "id") {#}
{#                   form_id.setValue(element.toString());#}
{##}
{#               } else if (index == "sbml_id") {#}
{#                   form_sbmlid.setValue(element.toString());#}
{#                   form_sbmlid.setInitialValue(element.toString());#}
{##}
{#               } else if (index == "name") {#}
{#                   form_name.setValue(element.toString());#}
{##}
{#               } else if (index == "value") {#}
{#                   if (element == null) { form_value.setValue(""); }#}
{#                   else { form_value.setValue(element.toString()); }#}
{##}
{#               } else if (index == "compartment_name") {#}
{#                   form_compartment.setLabel(element.toString());#}
{##}
{#               } else if (index == "compartment_id") {#}
{#                   form_compartment.setValue(element.toString());#}
{##}
{#               } else if (index == "unit_name") {#}
{#                   form_units.setLabel(element.toString());#}
{##}
{#               } else if (index == "unit_id") {#}
{#                   form_units.setValue(element.toString());#}
{##}
{#               } else if (index == "constant") {#}
{#                   if (element == "1") {#}
{#                       form_constant.switch_on();#}
{#                   } else {#}
{#                       form_constant.switch_off();#}
{#                   }#}
{##}
{#               } else if (index == "boundaryCondition") {#}
{#                   if (element == "1") { form_boundary.switch_on(); }#}
{#                   else { form_boundary.switch_off(); }#}
{##}
{#               } else if (index == "isConcentration") {#}
{##}
{#                   form_value_type.setValue(element.toString());#}
{#                   if (element == "1") {#}
{#                       form_value_type.setLabel("Concentration");#}
{#                   }#}
{#                   else {#}
{#                       form_value_type.setLabel("Amount");#}
{#                   }#}
{##}
{#               }  else if (index == "notes") {#}
{#                   form_notes.setValue(element.toString());#}
{##}
{#               } else if (index == "sboterm") {#}
{#                   form_sboterm.setValue(element.toString());#}
{#                   form_sboterm.setLink(element.toString());#}
{##}
{#               } else if (index == "sboterm_name") {#}
{#                   form_sboterm.setLabel(element.toString());#}
{#               }#}
{#           });#}
{##}
{#           form_sbmlid.check();#}
{#           form_group.resetErrors();#}
{#        },#}
{#        () => { console.log("failed"); }#}
{#    )#}
{##}
{#    modal_show();#}
{#}#}
{##}
{#function save_species()#}
{#{#}
{##}
{#    form_group.checkErrors();#}
{#    if (form_group.nb_errors == 0)#}
{#    {#}
{#        $("#modal_species").modal("hide");#}
{#    }#}
{##}
{#    return (form_group.nb_errors == 0);#}
{#}#}

let form_species = new SpeciesForm("modal_species");