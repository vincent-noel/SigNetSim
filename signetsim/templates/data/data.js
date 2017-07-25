function new_experiment()
{
    $("#modal_experiment-title").html("New experiment");

    $("#experiment_id").val("");
    $("#experiment_name").val("");
    $("#experiment_notes").val("");

    $("#modal_experiment").modal('show');
}

function view_experiment(experiment_id)
{

    $("#modal_experiment-title").html("Edit experiment");

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_experiment' %}", {'id': experiment_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "name") { $("#experiment_name").val(element.toString()); }
               else if (index == "notes") { $("#experiment_notes").val(element.toString()); }
           });

           $("#experiment_id").val(experiment_id);


        },
        function(){}
    );

    $('#modal_experiment').modal('show');
}

function save_experiment()
{
    $("#experiment_form").submit()
}