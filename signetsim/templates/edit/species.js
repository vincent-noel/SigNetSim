{% load bootstrap3 %}
{% load tags %}
{% include 'commons/js/sbmlid_form.js' %}
{% include 'commons/js/float_form.js' %}
{% include 'commons/js/sboterm_input.js' %}
{% include 'commons/js/slider_form.js' %}

let form_group = new FormGroup();

let form_value_type = new Dropdown("species_value_type", post_treatment=null, default_value="1", default_label="Concentration");
form_group.addForm(form_value_type);

let form_units = new Dropdown("species_unit", post_treatment=null, default_value="", default_label="Choose an unit");
form_group.addForm(form_units);

let form_compartment = new Dropdown("species_compartment", post_treatment=null, default_value="0", default_value="{{ list_of_compartments|my_lookup:0 }}");
form_group.addForm(form_compartment);

let form_sbmlid = new SbmlIdForm("species_sbml_id", "The identifier of the species", default_value="");
form_group.addForm(form_sbmlid, error_checking=true);

let form_value = new FloatForm("species_value", "The initial value of the species", false, default_value="0");
form_group.addForm(form_value, error_checking=true);

let form_sboterm = new SBOTermInput("species_sboterm");
form_group.addForm(form_sboterm);

let form_constant = new SliderForm("species_constant", "The constant setting of the species", default_value=0);
form_group.addForm(form_constant);

let form_boundary = new SliderForm("species_boundary", "The boundary value setting of the species", default_value=0);
form_group.addForm(form_boundary);

let form_notes = new Form("species_notes", "The notes of the species", default_value="");
form_group.addForm(form_notes);

let form_id = new Form("species_id", "The id of the species", default_value="");
form_group.addForm(form_id);

let form_name = new Form("species_name", "The name of the species", default_value="");
form_group.addForm(form_name);

function modal_show()
{
    $("#general").tab('show');
    $("#modal_species").on('shown.bs.modal', () => { $("#species_name").focus(); });
    $('#modal_species').modal('show');
}

function new_species()
{
    $("#modal_title").html("New species");
    form_group.clearForms();
    modal_show();
}

function view_species(sbml_id)
{

    $("#modal_title").html("Edit species");

    ajax_call(
        "POST",
        "{% url 'get_species' %}", {'sbml_id': sbml_id},
        (data) =>
        {
           $.each(data, (index, element) =>
           {
               if (index == "id") {
                   form_species.setValue(element.toString());

               } else if (index == "sbml_id") {
                   form_sbmlid.setValue(element.toString());
                   form_sbmlid.setInitialValue(element.toString());

               } else if (index == "name") {
                   form_name.setValue(element.toString());

               } else if (index == "value") {
                   if (element == null) { form_value.setValue(""); }
                   else { form_value.setValue(element.toString()); }

               } else if (index == "compartment_name") {
                   form_compartment.setLabel(element.toString());

               } else if (index == "compartment_id") {
                   form_compartment.setValue(element.toString());

               } else if (index == "unit_name") {
                   form_units.setLabel(element.toString());

               } else if (index == "unit_id") {
                   form_units.setValue(element.toString());

               } else if (index == "constant") {
                   if (element == "1") {
                       form_constant.switch_on();
                   } else {
                       form_constant.switch_off();
                   }

               } else if (index == "boundaryCondition") {
                   if (element == "1") { form_boundary.switch_on(); }
                   else { form_boundary.switch_off(); }

               } else if (index == "isConcentration") {

                   form_value_type.setValue(element.toString());
                   if (element == "1") {
                       form_value_type.setLabel("Concentration");
                   }
                   else {
                       form_value_type.setLabel("Amount");
                   }

               }  else if (index == "notes") {
                   form_notes.setValue(element.toString());

               } else if (index == "sboterm") {
                   form_sboterm.setValue(element.toString());
                   form_sboterm.setLink(element.toString());

               } else if (index == "sboterm_name") {
                   form_sboterm.setLabel(element.toString());
               }
           });

           form_sbmlid.check();
           form_group.resetErrors();
        },
        () => { console.log("failed"); }
    )

    modal_show();
}

function save_species()
{

    form_group.checkErrors();
    if (form_group.nb_errors == 0)
    {
        $("#modal_species").modal("hide");
    }

    return (form_group.nb_errors == 0);
}
