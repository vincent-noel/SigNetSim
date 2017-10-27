{% include 'commons/js/float_form.js' %}
{% include 'commons/js/sbmlid_form.js' %}
{% include 'commons/js/sboterm_input.js' %}
{% include 'commons/js/slider_form.js' %}

let form_group = new FormGroup();

let form_value = new FloatForm("parameter_value", "The value of the parameter", false, default_value="1");
form_group.addForm(form_value, error_checking=true);

let form_sbmlid = new SbmlIdForm("parameter_sbml_id", "The identifier of the parameter", has_scope=true, scope_field="parameter_scope_value", default_value="");
form_group.addForm(form_sbmlid, error_checking=true);

let dropdown_unit = new Dropdown("parameter_unit", post_treatment=null, default_value="", default_label="Choose an unit");
form_group.addForm(dropdown_unit);

let dropdown_scope = new Dropdown("parameter_scope", post_treatment=() => {form_sbmlid.check();},default_value="0",default_label="Global");
form_group.addForm(dropdown_scope);

let form_sboterm = new SBOTermInput("parameter_sboterm");
form_group.addForm(form_sboterm);

let form_constant = new SliderForm("parameter_constant", "The constant setting of the parameter", default_value=1);
form_group.addForm(form_constant);

let form_name = new Form("parameter_name", "The name of the parameter", default_value="");
form_group.addForm(form_name);

let form_id = new Form("parameter_id", "The id of the parameter", default_value="");
form_group.addForm(form_id);

let form_reaction_id = new Form("parameter_reaction_id", "The scope id of the parameter", default_value="");
form_group.addForm(form_reaction_id);

let form_notes = new Form("parameter_notes", "The notes of the parameter", default_value="");
form_group.addForm(form_notes);

function modal_show()
{
    $("#general").tab('show');
    $("#modal_parameter").on('shown.bs.modal', () => { $("#parameter_name").focus(); });
    $('#modal_parameter').modal('show');
}

function new_parameter()
{
    $("#modal_title").html("New parameter");
    form_group.clearForms();
    modal_show();
}


function view_parameter(sbml_id, reaction)
{

    $("#modal_title").html("Edit parameter");

    ajax_call(
        "POST",
        "{% url 'get_parameter' %}", {'sbml_id': sbml_id, 'reaction': reaction},
        (data) =>
        {
           $.each(data, (index, element) =>
           {
                if (index == "id") {
                    form_id.setValue(element.toString());

                } else if (index == "reaction_id") {

                    form_reaction_id.setValue(element.toString());

                    if (element.toString() == ""){
                        dropdown_scope.setValue(0);
                        dropdown_scope.setLabel("Global");
                        form_sbmlid.setInitialScope(0);

                    } else {
                        dropdown_scope.setValue(parseInt(element)+1);
                        form_sbmlid.setInitialScope(parseInt(element)+1);

                        switch(element) {
                            {% for reaction in list_of_reactions %}
                            case {{forloop.counter0}}:
                                dropdown_scope.setLabel("{{reaction.getName}}");
                                break;
                            {% endfor %}
                        }
                    }

                } else if (index == "sbml_id") {
                   form_sbmlid.setValue(element.toString());
                   form_sbmlid.setInitialValue(element.toString());

                } else if (index == "name") {
                   form_name.setValue(element.toString());

                } else if (index == "value") {
                   if (element == null) {
                       form_value.setValue("");
                   } else {
                       form_value.setValue(element.toString());
                   }

                } else if (index == "unit_name") {
                   dropdown_unit.setLabel(element.toString());

                } else if (index == "unit_id") {
                   dropdown_unit.setValue(element.toString());

                } else if (index == "constant") {

                   if (element == "1") {
                       form_constant.switch_on();
                   } else {
                       form_constant.switch_off();
                   }

                } else if (index == "notes") {
                   form_notes.setValue(element.toString());

                } else if (index == "sboterm") {
                   form_sboterm.setValue(element.toString());
                   form_sboterm.setLink(element.toString());

                } else if (index == "sboterm_name") {
                   form_sboterm.setLabel(element.toString());

                }
           });

           form_group.resetErrors();
           form_sbmlid.check();
        },
        () => { console.log("failed"); }
    );

    modal_show();
}

function save_parameter()
{
    form_group.checkErrors();

    if (form_group.nb_errors == 0)
    {
        $("#modal_parameter").modal("hide");
    }
    return (form_group.nb_errors == 0);
}