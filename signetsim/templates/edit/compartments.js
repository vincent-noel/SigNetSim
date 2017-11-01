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

class CompartmentForm extends FormGroup{

    constructor(field){
        super();
        this.field = field;

        this.dropdown_unit = new Dropdown("compartment_unit", null, "", "Choose an unit");
        this.addForm(this.dropdown_unit);

        this.form_value = new FloatForm("compartment_size", "The size of the compartment", false, 1);
        this.addForm(this.form_value, true);

        this.form_sbmlid = new SbmlIdForm("compartment_sbml_id", "The identifier of the compartment", "");
        this.addForm(this.form_sbmlid, true);

        this.form_sboterm = new SBOTermInput("compartment_sboterm");
        this.addForm(this.form_sboterm);

        this.form_constant = new SliderForm("compartment_constant", "The constant parameter of the compartment", 1);
        this.addForm(this.form_constant);

        this.form_name = new Form("compartment_name", "The name of the compartment", "");
        this.addForm(this.form_name);

        this.form_id = new Form("compartment_id", "The id of the compartment", "");
        this.addForm(this.form_id);

        this.form_notes = new Form("compartment_notes", "The notes of the compartment", "");
        this.addForm(this.form_notes);

    }

    show(){
        $('#general').tab('show');
        $('#' + this.field).modal('show');
        $("#" + this.field).on('shown.bs.modal', () => { $("#compartment_name").focus(); });
    }

    new(){
        $("#modal_title").html("New compartment");
        this.clearForms();
        this.show();
    }

    load(sbml_id){
        $("#modal_title").html("Edit compartment");

        ajax_call(
            "POST", "{% url 'get_compartment' %}",
            {'sbml_id': sbml_id},
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

                   } else if (index == "unit_name") {
                       this.dropdown_unit.setLabel(element.toString());

                   } else if (index == "unit_id") {
                       this.dropdown_unit.setValue(element.toString());

                   } else if (index == "constant") {
                       if (element == "1") { this.form_constant.switch_on(); }
                       else { this.form_constant.switch_off(); }

                   } else if (index == "notes") {
                       this.form_notes.setValue(element.toString());

                   } else if (index == "sboterm") {
                       this.form_sboterm.setValue(element.toString());
                       this.form_sboterm.setLink(element.toString());

                   } else if (index == "sboterm_name") {
                       this.form_sboterm.setName(element.toString());
                   }
               });

               this.form_sbmlid.check();
               this.resetErrors();
            },
            () => { console.log("compartment data retrieving failed"); }
        )

        this.show();
    }

    save(){
        this.checkErrors();

        if (this.nb_errors == 0)
        {
            $("#" + this.field).modal("hide");
        }

        return (this.nb_errors == 0);
    }
}

let form_compartment = new CompartmentForm("modal_compartment");
