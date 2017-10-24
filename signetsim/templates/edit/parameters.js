{% include 'commons/js/forms.js' %}

$('#parameter_scope_dropdown li').on('click', function(){
  $("#parameter_scope_label").html($(this).text());
  $('#parameter_scope').val($(this).index());
  check_sbml_id_validity();
});

$('#unit_list li').on('click', function(){
  $("#parameter_unit_label").html($(this).text());
  $('#parameter_unit').val($(this).index());
});



// Value validator
let form_value = new FloatForm("parameter_value", "The value of the parameter", false);
$("#parameter_value").on('paste keyup', () => { form_value.check(); });

// SbmlId Validation
let form_sbmlid = new SbmlIdForm("parameter_sbml_id", "The identifier of the parameter");
$("#parameter_sbml_id").on('paste keyup', () => { form_sbmlid.check(); });

$('#new_parameter_button').on('click', function()
{
    new_parameter();
    $('#modal_parameter').modal('show');
});

function new_parameter()
{
    $("#modal_title").html("New parameter");
    $("#parameter_name").val("");
    $("#parameter_sbml_id").val("");
    $("#parameter_value").val("");
    $("#parameter_unit_label").html("Choose a unit");
    $("#parameter_unit").val("");
    $("#parameter_constant").prop('checked', true);
    $("#parameter_id").val("");
    $("#parameter_reaction_id").val("");
    $("#parameter_scope").val(0);
    $("#parameter_scope_label").html("Global");

    form_value.clearError();
    form_sbmlid.clearError();
    form_sbmlid.setValue("");
    form_sbmlid.setIndicatorEmpty();

    reset_errors();
    $("#general").tab('show');
    $("#modal_parameter").on('shown.bs.modal', function() { $("#parameter_name").focus(); });

}


function view_parameter(sbml_id, reaction)
{

    $("#modal_title").html("Edit parameter");

    ajax_call(
        "POST",
        "{% url 'get_parameter' %}", {'sbml_id': sbml_id, 'reaction': reaction},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "id") { $("#parameter_id").val(element.toString()); }
               else if (index == "reaction_id") {
                   if (element.toString() == ""){
                       $("#parameter_scope").val(0);
                       $("#parameter_scope_label").html("Global");
                   } else {
                       $("#parameter_scope").val(parseInt(element)+1);

                       switch(element) {
                           {% for reaction in list_of_reactions %}
                           case {{forloop.counter0}}:
                                $("#parameter_scope_label").html("{{reaction.getName}}");
                                break;
                           {% endfor %}
                       }

                   }
               }
               else if (index == "sbml_id") { $("#parameter_sbml_id").val(element.toString()); form_sbmlid.setValue(element.toString()); }
               else if (index == "name") { $("#parameter_name").val(element.toString()); }

               else if (index == "value") {
                   if (element == null) { $("#parameter_value").val(""); }
                   else { $("#parameter_value").val(element.toString()); }
               }

               else if (index == "unit_name") { $("#parameter_unit_label").html(element.toString()); }
               else if (index == "unit_id") { $("#parameter_unit").val(element.toString()); }

               else if (index == "constant") {
                   if (element == "1") { $("#parameter_constant").prop('checked', true); }
                   else { $("#parameter_constant").prop('checked', false); }
               }
               else if (index == "notes") {
                   $("#parameter_notes").val(element.toString());

               }
                else if (index == "sboterm") {
                   $("#sboterm").val(element.toString());
                   $("#sboterm_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());
                }
                else if (index == "sboterm_name") { $("#sboterm_name").html(element.toString()); }
           });

           form_sbmlid.check();
           reset_errors();
        },
        function() { console.log("failed"); }
    )
    $("#general").tab('show');
    $('#modal_parameter').modal('show');
    $("#modal_parameter").on('shown.bs.modal', function() { $("#parameter_name").focus(); });

}
function reset_errors()
{
    form_value.unhighlight();
    form_sbmlid.unhighlight();
    $("#error_modal").empty();

}

function save_parameter()
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
        $("#modal_parameter").modal("hide");
    }
    return (nb_errors == 0);
}