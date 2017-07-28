$('#unit_list li').on('click', function(){
  $("#unit_name").html($(this).text());
  $('#unit_id').val($(this).index());
});

var nb_units = 0;
function add_unit(unit_name, unit_kind, unit_kind_name, unit_exponent, unit_scale, unit_multiplier)
{
    $("#list_units").append("\
        <tr class=\"row\"><td class=\"col-xs-10\">" + unit_name.toString() + "\
            <input type=\"hidden\" id=\"unit_id_" + nb_units.toString() + "\" name=\"unit_id_" + nb_units.toString() + "\" value=\"" + unit_kind.toString() + "\">\
            <input type=\"hidden\" id=\"unit_id_" + nb_units.toString() + "_name\" name=\"unit_id_" + nb_units.toString() + "_name\" value=\"" + unit_kind_name.toString() + "\">\
            <input type=\"hidden\" id=\"unit_exponent_" + nb_units.toString() + "\" name=\"unit_exponent_" + nb_units.toString() + "\" value=\"" + unit_exponent.toString() + "\">\
            <input type=\"hidden\" id=\"unit_scale_" + nb_units.toString() + "\" name=\"unit_scale_" + nb_units.toString() + "\" value=\"" + unit_scale.toString() + "\">\
            <input type=\"hidden\" id=\"unit_multiplier_" + nb_units.toString() + "\" name=\"unit_multiplier_" + nb_units.toString() + "\" value=\"" + unit_multiplier.toString() + "\">\
        </td><td class=\"col-xs-2 text-right\">\
            <button type=\"button\" class=\"btn btn-primary btn-xs\" onclick=\"view_unit(" + nb_units.toString() + ")\"><span class=\"glyphicon glyphicon-pencil\"></span></button>\
            <button type=\"button\" class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-trash\"></span></button>\
        </td></tr>\
        ");
    nb_units++;
}
function remove_units()
{
  $("#list_units").children("tr").each(function() {
    $(this).remove();
  });
  nb_units = 0;
}

function new_unit_definition()
{
    $("#modal_title").html("New unit");
    $("#unit_definition_identifier").val("");
    $("#unit_definition_name").val("");
    $("#unit_definition_desc").val("");

    remove_units();
    $('#new_unit').modal('show');

}

function view_unit_definition(unit_id)
{

    $("#modal_title").html("Edit unit");
    remove_units();
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_unit_definition' %}", {'id': unit_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index === "unit_id") { $("#unit_definition_identifier").val(element.toString()); }
               else if (index === "name") { $("#unit_definition_name").val(element.toString()); }
               else if (index === "desc") { $("#unit_definition_desc").val(element.toString()); }
               else if (index === "list_of_units") {
                   console.log(element);
                   $.each(element, function(index, subelement) {
                       add_unit(subelement[0], subelement[1], subelement[2], subelement[3], subelement[4], subelement[5]);
                   });
               }
               $("#unit_definition_id").val(unit_id);
           });

        },
        function() { console.log("failed"); }
    )
    $('#new_unit').modal('show');

}

function save_unit_definition()
{
    var nb_errors = 0;
//    reset_errors();

    if (nb_errors == 0)
    {
         $("#unit_form").submit();
    }
}


$('#add_new_unit').on('click', function(){

    if($("#edit_unit").hasClass("out")) {

            $("#unit_id").val("");
            $("#unit_name").html("Choose unit type");
            $("#unit_exponent").val(1);
            $("#unit_scale").val(1);
            $("#unit_multiplier").val(1);
            $("#unit_button").html("Add")

            $("#edit_unit").addClass("in");
            $("#edit_unit").removeClass("out");

    } else {
            $("#edit_unit").addClass("out");
            $("#edit_unit").removeClass("in");
    }
});


function new_unit()
{
    if($("#edit_unit").hasClass("in")) {
        $("#edit_unit").removeClass("in");
    } else {
            $("#unit_id").val("");
            $("#unit_name").html("Choose unit type");
            $("#unit_exponent").val(1);
            $("#unit_scale").val(1);
            $("#unit_multiplier").val(1);
            $("#unit_button").html("Add")

            $("#edit_unit").addClass("in");

    }


    $("#modal_substitution_id").val("");
    $("#substitution_type").val(0);
    $("#substitution_type_label").html("Replace a variable from a submodel with a variable from the main model (Replacement)");
    $("#substitution_model_object").val("");
    $("#substitution_model_object_label").html("Select an object in the main model");
    $("#substitution_submodel").val("");
    $("#substitution_submodel_label").html("Select a submodel");
    $("#substitution_submodel_object").val("");
    $("#substitution_submodel_object_label").html("Select an object in the submodel");
    reset_errors();

    $('#modal_substitution').modal('show');
}



function view_unit(unit_id)
{
    $("#unit_kind").val($("#unit_id_" + unit_id.toString()).val());
    $("#unit_kind_name").html($("#unit_id_" + unit_id.toString() + "_name").val());
    $("#unit_exponent").val($("#unit_exponent_" + unit_id.toString()).val());
    $("#unit_scale").val($("#unit_scale_" + unit_id.toString()).val());
    $("#unit_multiplier").val($("#unit_multiplier_" + unit_id.toString()).val());

    if (!$("#edit_unit").hasClass("in")) { $("#edit_unit").addClass("in"); }
}

function save_unit()
{

}







