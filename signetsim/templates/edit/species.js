{% load bootstrap3 %}
{% load tags %}

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

var old_sbml_id = "";

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

var form_sbml_id_error = "";

$("#species_sbml_id").on('paste keyup', function()
{
  new_sbml_id = $.trim($("#species_sbml_id").val());
  if (old_sbml_id === "" || new_sbml_id !== old_sbml_id)
  {
    setSbmlIdValidating();

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'sbml_id_validator' %}", {'sbml_id' : new_sbml_id},
        function(data) {
           $.each(data, function(index, element) {
             if (index == 'error' && element == '') {setSbmlIdValid(); form_sbml_id_error = element.toString();}
             else {setSbmlIdInvalid(); form_sbml_id_error = element.toString();}
           });
        },
        function()
        {
          setSbmlIdInvalid();
        }
    )
  }
  else if (new_sbml_id === old_sbml_id)
  {
    setSbmlIdValid();
  }
});

// Value validator

var form_value_error = "";

$("#species_value").on('paste keyup', function()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'float_validator' %}",
        {'value' : $("#species_value").val(), 'required' : 'false'},
        function(data) {
           $.each(data, function(index, element) {
             if (index == "error") {form_value_error=element.toString();}
             else {form_value_error = "";}
           });
        },
        function(){}
    );
});






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
    setSbmlIdEmpty();
    reset_errors();
    old_sbml_id = "";
    $("#general").tab('show');
    $("#modal_species").on('shown.bs.modal', function() { $("#species_name").focus(); });

}

function view_species(sbml_id)
{

    $("#modal_title").html("Edit species");

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_species' %}", {'sbml_id': sbml_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "id") { $("#species_id").val(element.toString()); }
               else if (index == "sbml_id") { $("#species_sbml_id").val(element.toString()); old_sbml_id=element; }
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

           setSbmlIdEmpty();
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

    if ($("#sbmlid_invalid").hasClass("in")){
        add_error_modal("invalid_sbml_id", "Species " + form_sbml_id_error);
        form_add_error_highlight("species_sbml_id");
        nb_errors++;
    }

    if (form_value_error != ""){
        add_error_modal("invalid_value", "Species initial value " + form_value_error);
        form_add_error_highlight("species_value");
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
   form_remove_error_highlight("species_sbml_id");
   form_remove_error_highlight("species_value");
   $("#error_modal").empty();

}

