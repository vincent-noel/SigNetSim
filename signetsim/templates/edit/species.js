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
             if (index === 'valid' && element === 'true') {setSbmlIdValid();}
             else {setSbmlIdInvalid();}
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
    $("#error_modal").empty();
    form_remove_error_highlight("species_sbml_id");

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
               if (index == "id") { $("#species_id").attr("value", element); }
               else if (index == "sbml_id") { $("#species_sbml_id").attr("value", element); old_sbml_id=element; }
               else if (index == "name") { $("#species_name").attr("value", element); }
               else if (index == "value") { $("#species_value").attr("value", element); }

               else if (index == "compartment_name") { $("#species_compartment_label").html(element); }
               else if (index == "compartment_id") { $("#species_compartment").attr("value", element); }

               else if (index == "unit_name") { $("#species_unit_label").html(element); }
               else if (index == "unit_id") { $("#species_unit").attr("value", element); }

               else if (index == "constant") { $("#species_constant").attr("value", element); }
               else if (index == "boundaryCondition") { $("#species_boundary").attr("value", element); }

               else if (index == "isConcentration") {
                   $("#species_value_type").attr("value", element);
                   if (element == "1") {
                       $("#species_value_type_label").html("Concentration");
                   }
                   else {
                       $("#species_value_type_label").html("Amount");
                   }
               }
           });
           $("#error_modal").empty();
           setSbmlIdEmpty();
           form_remove_error_highlight("species_sbml_id");

        },
        function() { console.log("failed"); }
    )

    $('#modal_species').modal('show');

}
function form_add_error_highlight(form_id)
{
    $("#" + form_id + "_label").addClass("text-danger");
    $("#" + form_id + "_group").addClass("has-error");

}
function form_remove_error_highlight(form_id)
{
    $("#" + form_id + "_label").removeClass("text-danger");
    $("#" + form_id + "_group").removeClass("has-error");

}
function save_species()
{
    console.log("checking form...");
    if ($("#sbmlid_invalid").hasClass("in")){
        add_error_modal("invalid_sbml_id", "Invalid SBML Id");
        form_add_error_highlight("species_sbml_id");
        console.log("ERroR");
        return;
    }
    else {$("#species_form").submit();}
}