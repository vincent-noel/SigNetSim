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
               else if (index == "sbml_id") { $("#species_sbml_id").attr("value", element); }
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
                   if (element == "1") { $("#species_value_type_label").html("Concentration");}
                   else { $("#species_value_type_label").html("Amount");}
               }
           });
        },
        function() { console.log("failed"); }
    )

    $('#modal_species').modal('show');

}



// SbmlId Validation

var old_sbml_id = "{% if form.isEditing == True and form.sbmlId != None %}{{form.sbmlId}}{% endif %}";

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


$("#species_sbml_id").on('change paste keyup', function()
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



{% if form.hasErrors == True or form.isEditing == True %}
    $(window).on('load',function(){
        $('#modal_species').modal('show');

    });
{% endif %}



