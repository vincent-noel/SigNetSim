
var nb_assignments = {{form.assignments|length}} - 1;

function add_assignment(){
    nb_assignments = nb_assignments + 1;
    $("#body_assignments").append("\
    <tr id='event_assignment_" + nb_assignments.toString() + "_tr'>\
      <td class=\"col-xs-5 text-center\">\
        <input type=\"hidden\" id=\"event_assignment_" + nb_assignments.toString() + "\" name=\"event_assignment_" + nb_assignments.toString() + "_id\" value=\"\">\
        <div class=\"dropdown\">\
          <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
            <span id=\"event_assignment_" + nb_assignments.toString() + "_label\">Choose a variable</span>\
            <span class=\"caret\"></span>\
          </button>\
          <ul id=\"event_assignment_" + nb_assignments.toString() + "_dropdown\" class=\"dropdown-menu\">\
            {% for var in list_of_variables %}<li><a href=\"#\">{{ var }}</a></li>{% endfor %}\
          </ul>\
        </div>\
      </td>\
      <td class=\"col-xs-5\">\
        <input type=\"text\" class=\"form-control input-sm\" placeholder=\"Input assignment exression\" name=\"event_assignment_" + nb_assignments.toString() + "_expression\" value=\"\">\
      </td>\
      <td class=\"col-xs-2 text-right vert-align\">\
        <button type=\"button\" onclick=\"remove_assignment(" + nb_assignments.toString() + ");\" class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-remove\"></span></button>\
      </td>\
    </tr>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
         $(\"#event_assignment_" + nb_assignments.toString() + "_dropdown li\").on(\"click\", function(){\
           $(\"#event_assignment_" + nb_assignments.toString() + "_label\").html($(this).text());\
           $(\"#event_assignment_" + nb_assignments.toString() + "\").val($(this).index());});")
       .appendTo('#event_assignment_' + nb_assignments.toString() + '_tr');

    updateFormNames();
}

function remove_assignment(assignment_id)
{
    $("#event_assignment_" + assignment_id + "_tr").remove();
    updateFormNames();

}

function updateFormNames()
{
    var ass_id = 0;

    $("#body_assignments").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^event_assignment_[0-9]+_id$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'event_assignment_' + ass_id.toString() + '_id');
            }

            var exp = new RegExp('^event_assignment_[0-9]+_expression$');
            if (exp.test($(this).attr('name')))
            {
                $(this).attr('name', 'event_assignment_' + ass_id.toString() + '_expression');
            }
        });
        ass_id = ass_id + 1;
    });
}


$('#toggle_trigger_options').on('click', function(){

  if($("#trigger_options").hasClass("in")) {
          $("#trigger_options").removeClass("in");

  } else {
          $("#trigger_options").addClass("in");
  }
});

$('#new_event_button').on('click', function(){
    $("#body_assignments").children("tr").remove();
    add_assignment();
    $("#event_trigger").attr("value", "");
    $("#event_priority").attr("value", "");
    $("#event_delay").attr("value", "");
    $("#event_persistent").attr("checked", true);
    $("#event_initialvalue").attr("checked", false);
    $("#error_messages").remove();
    if($("#trigger_options").hasClass("in")) {
            $("#trigger_options").addClass("out");
            $("#trigger_options").removeClass("in");
    }
    $('#modal_event').modal('show');

});


function toggle_slide(slide_id) {
  if ($('#' + slide_id).prop('checked') == true) {
    $('#' + slide_id).prop("checked", false);
  } else {
    $('#' + slide_id).prop("checked", true);
  }
}

