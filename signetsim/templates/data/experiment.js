function new_condition()
{
    $("#modal_condition-title").html("New condition");

    $("#condition_id").val("");
    $("#condition_name").val("");
    $("#condition_notes").val("");

    $("#modal_condition").modal('show');
}

function view_condition(condition_id)
{

    $("#modal_condition-title").html("Edit condition");

    ajax_call(
        "POST",
        "{% url 'get_condition' %}", {'id': condition_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "name") { $("#condition_name").val(element.toString()); }
               else if (index == "notes") { $("#condition_notes").val(element.toString()); }
           });

           $("#condition_id").val(condition_id);


        },
        function(){}
    );

    $('#modal_condition').modal('show');
}

function save_condition()
{
    $("#condition_form").submit()
}