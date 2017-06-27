{% if create_folder_show != None %}

  $(window).on('load',function(){
    $('#new_folder').modal('show');

  });

{% endif %}

{% if send_folder_show != None %}

  $(window).on('load',function(){
    $('#send_folder').modal('show');

  });

{% endif %}

{% for project in projects %}

$('#send_{{project.id}}').on('click', function(){
    $('#send_id').val("{{project.id}}");
    $('#send_folder').modal('show');


});

{% endfor %}

function new_project()
{
    $("#modal_project_title").html("New project");
    $("#modal_project_id").val("");
    $("#modal_project_name").val("");
    $("#modal_project_access").prop('checked', false);

    $('#modal_project').modal('show');

}

function view_project(project_id)
{

    $("#modal_project_title").html("Edit project");

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_project' %}", {'id': project_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "name") { $("#modal_project_name").val(element.toString()); }
               else if (index == "public")
               {
                   if (element == "1") {
                       $("#modal_project_access").prop('checked', true);
                   }
                   else {
                       $("#modal_project_access").prop('checked', false);
                   }
               }
           });

           $("#modal_project_id").val(project_id);


        },
        function(){}
    );

    $('#modal_project').modal('show');
}


function save_project()
{
    $("#form_project").submit();
}