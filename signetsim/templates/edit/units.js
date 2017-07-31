$('#unit_kind_list li').on('click', function(){
  $("#unit_kind_name").html($(this).text());
  $('#unit_id').val($(this).index());
});

var nb_units = 0;
function add_unit(unit_name, unit_kind, unit_kind_name, unit_exponent, unit_scale, unit_multiplier)
{
    $("#list_units").append("\
        <tr class=\"row\" id=\"unit_tr_" + nb_units.toString() + "\">\
        <input type=\"hidden\" id=\"unit_id_" + nb_units.toString() + "\" name=\"unit_id_" + nb_units.toString() + "\" value=\"" + unit_kind.toString() + "\">\
        <input type=\"hidden\" id=\"unit_id_" + nb_units.toString() + "_name\" name=\"unit_id_" + nb_units.toString() + "_name\" value=\"" + unit_kind_name.toString() + "\">\
        <input type=\"hidden\" id=\"unit_exponent_" + nb_units.toString() + "\" name=\"unit_exponent_" + nb_units.toString() + "\" value=\"" + unit_exponent.toString() + "\">\
        <input type=\"hidden\" id=\"unit_scale_" + nb_units.toString() + "\" name=\"unit_scale_" + nb_units.toString() + "\" value=\"" + unit_scale.toString() + "\">\
        <input type=\"hidden\" id=\"unit_multiplier_" + nb_units.toString() + "\" name=\"unit_multiplier_" + nb_units.toString() + "\" value=\"" + unit_multiplier.toString() + "\">\
        <td class=\"col-xs-10\" id=\"unit_desc_" + nb_units.toString() + "\">" + unit_name.toString() + "</td><td class=\"col-xs-2 text-right\">\
            <button type=\"button\" class=\"btn btn-primary btn-xs\" onclick=\"view_unit(" + nb_units.toString() + ")\"><span class=\"glyphicon glyphicon-pencil\"></span></button>\
            <button type=\"button\" class=\"btn btn-danger btn-xs\" onclick=\"remove_unit(" + nb_units.toString() + ")\"><span class=\"glyphicon glyphicon-trash\"></span></button>\
        </td></tr>\
        ");
    nb_units++;
    update_units_form();
}
function remove_units()
{
  $("#list_units").children("tr").each(function() {
    $(this).remove();
  });
  nb_units = 0;
}

function remove_unit(unit_id)
{
    $("#unit_tr_" + unit_id.toString()).remove();
    update_units_form();
}

function update_units_form()
{
    var p_id = 0;
    var global_desc = "";
    $("#list_units").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^unit_id_[0-9]+$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'unit_id_' + p_id.toString());
            }

            var name = new RegExp('^unit_id_[0-9]+_name$');
            if (name.test($(this).attr('name')))
            {
              $(this).attr('name', 'unit_id_' + p_id.toString() + '_name');
            }

            var exponent = new RegExp('^unit_exponent_[0-9]+$');
            if (exponent.test($(this).attr('name')))
            {
              $(this).attr('name', 'unit_exponent_' + p_id.toString());
            }
            var scale = new RegExp('^unit_scale_[0-9]+$');
            if (scale.test($(this).attr('name')))
            {
              $(this).attr('name', 'unit_scale_' + p_id.toString());
            }
            var multiplier = new RegExp('^unit_multiplier_[0-9]+$');
            if (multiplier.test($(this).attr('name')))
            {
              $(this).attr('name', 'unit_multiplier_' + p_id.toString());
            }
        });
        if (p_id > 0){
            global_desc += ".";
        }
        $('td', $(this)).each(function()
        {
            var td = new RegExp('^unit_desc_[0-9]+$');
            if (td.test($(this).attr('id'))) {
                global_desc += $(this).html();
            }
        });
        p_id = p_id + 1;
    });
    $("#unit_definition_desc").val(global_desc);
}

function update_global_desc()
{
    var p_id = 0;
    var global_desc = "";

    $("#list_units").children("tr").each(function()
    {
        if (p_id > 0){
            global_desc += ".";
        }
        $('td', $(this)).each(function()
        {
            var td = new RegExp('^unit_desc_[0-9]+$');
            if (td.test($(this).attr('id'))) {
                global_desc += $(this).html();
            }
        });
        p_id = p_id + 1;
    });
    $("#unit_definition_desc").val(global_desc);
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

    if(!$("#edit_unit").hasClass("in")) {

            $("#unit_edit_id").val("");
            $("#unit_id").val("");
            $("#unit_name").html("Choose unit type");
            $("#unit_exponent").val(1);
            $("#unit_scale").val(1);
            $("#unit_multiplier").val(1);
            $("#unit_button").html("Add")

            $("#edit_unit").addClass("in");

    } else {
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
    $("#unit_edit_id").val(unit_id);
    $("#unit_id").val($("#unit_id_" + unit_id.toString()).val());
    $("#unit_kind_name").html($("#unit_id_" + unit_id.toString() + "_name").val());
    $("#unit_exponent").val($("#unit_exponent_" + unit_id.toString()).val());
    $("#unit_scale").val($("#unit_scale_" + unit_id.toString()).val());
    $("#unit_multiplier").val($("#unit_multiplier_" + unit_id.toString()).val());

    if (!$("#edit_unit").hasClass("in")) { $("#edit_unit").addClass("in"); }
}
var unit_ids = {
    {% for unit in unit_list %}
    {{ forloop.counter0 }}: "{{ unit }}",
    {% endfor %}
};

function save_unit()
{
    var desc = "";
    if (parseFloat($("#unit_multiplier").val()) !== 1){
        desc += "(" + $("#unit_multiplier").val() + "."
    }

    if (parseInt($("#unit_scale").val()) === -3){
        desc += "m";
    } else if (parseInt($("#unit_scale").val()) === -6){
        desc += "u";
    } else if (parseInt($("#unit_scale").val()) === -9){
        desc += "n";
    } else if (parseInt($("#unit_scale").val()) === 3){
        desc += "k";
    } else if (parseInt($("#unit_scale").val()) === 6){
        desc += "M";
    } else if (parseInt($("#unit_scale").val()) === 9) {
        desc += "G";
    }
    desc += unit_ids[$("#unit_id").val()];
    if (parseFloat($("#unit_exponent").val()) !== 1){
        desc += "^" + $("#unit_exponent").val();
    }

    if (parseFloat($("#unit_multiplier").val()) !== 1){
        desc += ")";
    }

    if ($("#unit_edit_id").val() === ""){
        add_unit(desc,
            $("#unit_id").val(),
            $("#unit_kind_name").html(),
            $("#unit_exponent").val(),
            $("#unit_scale").val(),
            $("#unit_multiplier").val(),
        );

    } else {
        $("#unit_desc_" + $("#unit_edit_id").val().toString()).html(desc);
        $("#unit_id_" + $("#unit_edit_id").val().toString()).val($("#unit_id").val());
        $("#unit_id_" + $("#unit_edit_id").val().toString() + "_name").val($("#unit_kind_name").val());
        $("#unit_scale_" + $("#unit_edit_id").val().toString()).val($("#unit_scale").val());
        $("#unit_exponent_" + $("#unit_edit_id").val().toString()).val($("#unit_exponent").val());
        $("#unit_multiplier_" + $("#unit_edit_id").val().toString()).val($("#unit_multiplier").val());
        update_global_desc();
        $("#edit_unit").removeClass("in");
    }
}







