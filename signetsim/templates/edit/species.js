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

        this.form_value_type = new Dropdown("species_value_type", "The type of the value of the species", null, "1", "Concentration");
        this.addForm(this.form_value_type);

        this.form_units = new Dropdown("species_unit", "The unit of the species", null, "", "Choose an unit");
        this.addForm(this.form_units);

        this.form_compartment = new Dropdown("species_compartment", "The compartment of the species", null, "0", "{{ list_of_compartments|my_lookup:0 }}");
        this.addForm(this.form_compartment);

        this.form_sbmlid = new SbmlIdForm("species_sbml_id", "The identifier of the species", "");
        this.addForm(this.form_sbmlid, true);

        this.form_value = new FloatForm("species_value", "The initial value of the species", false, "0");
        this.addForm(this.form_value, true);

        this.form_sboterm = new SBOTermInput("species_sboterm");
        this.addForm(this.form_sboterm);

        this.form_constant = new SliderForm("species_constant", "The constant setting of the species", false);
        this.addForm(this.form_constant);

        this.form_boundary = new SliderForm("species_boundary", "The boundary value setting of the species", false);
        this.addForm(this.form_boundary);

        this.form_notes = new ValueForm("species_notes", "The notes of the species", "");
        this.addForm(this.form_notes);

        this.form_id = new ValueForm("species_id", "The id of the species", "");
        this.addForm(this.form_id);

        this.form_name = new ValueForm("species_name", "The name of the species", "");
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
                       this.form_sbmlid.setInitialValue(element.toString());
                       this.form_sbmlid.setValue(element.toString());

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

               // this.checkErrors();
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

let form_species = new SpeciesForm("modal_species");