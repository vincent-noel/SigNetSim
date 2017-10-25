{% load bootstrap3 %}
{% load tags %}
{% include 'commons/js/forms.js' %}

$('#species_value_type_dropdown li').on('click', function()
{
  $("#species_value_type_label").html($(this).text());
  $('#species_value_type').val($(this).index());
});

$('#unit_list li').on('click', function()
{
  $("#species_unit_label").html($(this).text());
  $('#species_unit').val($(this).index());
});

$('#species_compartment_dropdown li').on('click', function()
{
  $("#species_compartment_label").html($(this).text());
  $('#species_compartment').val($(this).index());
});

$('#new_species_button').on('click', function()
{
    new_species();
    $('#modal_species').modal('show');

});

// SbmlId Validation
let form_sbmlid = new SbmlIdForm("species_sbml_id", "The identifier of the species");
let form_value = new FloatForm("species_value", "The initial value of the species", false);

function new_species()
{
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
    form_value.clearError();
    form_sbmlid.clearError();
    form_sbmlid.setValue("");
    form_sbmlid.setIndicatorEmpty();
    reset_errors();
    $("#general").tab('show');
    $("#modal_species").on('shown.bs.modal', function() { $("#species_name").focus(); });

}

function view_species(sbml_id)
{

    $("#modal_title").html("Edit species");

    ajax_call(
        "POST",
        "{% url 'get_species' %}", {'sbml_id': sbml_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "id") { $("#species_id").val(element.toString()); }
               else if (index == "sbml_id") { $("#species_sbml_id").val(element.toString()); form_sbmlid.setValue(element.toString()); }
               else if (index == "name") { $("#species_name").val(element.toString()); }

               else if (index == "value") {
                   if (element == null) { $("#species_value").val(""); }
                   else { $("#species_value").val(element.toString()); }
               }

               else if (index == "compartment_name") { $("#species_compartment_label").html(element.toString()); }
               else if (index == "compartment_id") { $("#species_compartment").val(element.toString()); }

               else if (index == "unit_name") { $("#species_unit_label").html(element.toString()); }
               else if (index == "unit_id") { $("#species_unit").val(element.toString()); }

               else if (index == "constant") {
                   if (element == "1") { $("#species_constant").prop('checked', true); }
                   else { $("#species_constant").prop('checked', false); }
               }
               else if (index == "boundaryCondition") {
                   if (element == "1") { $("#species_boundary").prop('checked', true); }
                   else { $("#species_boundary").prop('checked', false); }
               }

               else if (index == "isConcentration") {
                   $("#species_value_type").val(element.toString());
                   if (element == "1") {
                       $("#species_value_type_label").html("Concentration");
                   }
                   else {
                       $("#species_value_type_label").html("Amount");
                   }
               }
               else if (index == "notes") { $("#specie_notes").val(element.toString()); }

               else if (index == "sboterm") {
                   $("#sboterm").val(element.toString());
                   $("#sboterm_link").attr(
                       "href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString()
                   );
               }
               else if (index == "sboterm_name") { $("#sboterm_name").html(element.toString()); }
           });

           form_sbmlid.check();
           reset_errors();
        },
        function() { console.log("failed"); }
    )

    $("#general").tab('show');
    $('#modal_species').modal('show');

    $("#modal_species").on('shown.bs.modal', function() { $("#species_name").focus(); });


}

function save_species()
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
        $("#modal_species").modal("hide");
    }

    return (nb_errors == 0);
}

function reset_errors()
{
   form_sbmlid.unhighlight();
   form_value.unhighlight();
   $("#error_modal").empty();

}

