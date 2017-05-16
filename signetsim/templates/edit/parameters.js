$('#parameter_scope_dropdown li').on('click', function(){
  $("#parameter_scope_label").html($(this).text());
  $('#parameter_scope').val($(this).index());
  check_sbml_id_validity();
});

$('#unit_list li').on('click', function(){
  $("#parameter_unit_label").html($(this).text());
  $('#parameter_unit').val($(this).index());
});



function toggle_slide(slide_id) {
  if ($('#' + slide_id).prop('checked') == true) {
    $('#' + slide_id).prop("checked", false);
  } else {
    $('#' + slide_id).prop("checked", true);
  }
}


// Value validator

var form_value_error = "";

$("#parameter_value").on('paste keyup', function()
{
    if ($("#parameter_value").val() != "")
    {
        ajax_call(
            "POST", "{{csrf_token}}",
            "{% url 'float_validator' %}", {'value' : $("#parameter_value").val()},
            function(data) {
               $.each(data, function(index, element) {
                 if (index == "error") {form_value_error=element.toString();}
               });
            },
            function(){}
        );
    }

});



// SbmlId Validation

var form_sbml_id_error= "";
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

$("#parameter_sbml_id").on('paste keyup', function()
{
    check_sbml_id_validity();
});


function check_sbml_id_validity()
{
    new_sbml_id = $.trim($("#parameter_sbml_id").val());

    reaction_id = "";
    if (parseInt($("#parameter_scope").val()) > 0) {
        reaction_id = parseInt($("#parameter_scope").val()) - 1;
    }

    if (old_sbml_id === "" || new_sbml_id !== old_sbml_id) {
        setSbmlIdValidating();
        ajax_call(
            "POST", "{{csrf_token}}",
            "{% url 'sbml_id_validator' %}", {'sbml_id': new_sbml_id, 'reaction_id': reaction_id},
            function (data) {
                $.each(data, function (index, element) {
                    if (index == 'error' && element == '') {
                        setSbmlIdValid()
                        form_sbml_id_error = "";
                    } else {
                        setSbmlIdInvalid();
                        form_sbml_id_error = element.toString();
                    }
                });
            },
            function () {
                setSbmlIdInvalid();
            }
        );
    }
    else if (new_sbml_id === old_sbml_id) {
        setSbmlIdValid();
    }
}


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
    old_sbml_id = "";
    setSbmlIdEmpty();
    reset_errors();
    $("#general").tab('show');
}


function view_parameter(sbml_id, reaction)
{

    $("#modal_title").html("Edit parameter");

    ajax_call(
        "POST", "{{csrf_token}}",
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
               else if (index == "sbml_id") { $("#parameter_sbml_id").val(element.toString()); old_sbml_id=element; }
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

           setSbmlIdEmpty();
           reset_errors();
        },
        function() { console.log("failed"); }
    )
    $("#general").tab('show');
    $('#modal_parameter').modal('show');

}
function reset_errors()
{
   form_remove_error_highlight("parameter_sbml_id");
   form_remove_error_highlight("parameter_value");
   $("#error_modal").empty();

}

function save_parameter()
{
    var nb_errors = 0;
    reset_errors();

    if ($("#sbmlid_invalid").hasClass("in")){
        add_error_modal("invalid_sbml_id", "Parameter " + form_sbml_id_error);
        form_add_error_highlight("species_sbml_id");
        nb_errors++;
    }

    if (form_value_error != ""){
        add_error_modal("invalid_value", "Parameter value " + form_value_error);
        form_add_error_highlight("parameter_value");
        nb_errors++;
    }
    if (nb_errors == 0)
    {
        $("#parameter_form").submit();
    }
}