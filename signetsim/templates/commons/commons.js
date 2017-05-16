
$('#edit_SBO_term').on('click', function(){
    $("#edit_SBO_term_on").addClass("in");
    $("#edit_SBO_term_off").removeClass("in");
    $("#edit_SBO_term_off_actions").addClass("in");
    $("#edit_SBO_term_on_actions").removeClass("in");
});

$('#edit_SBO_term_cancel').on('click', function(){
  $("#edit_SBO_term_off").addClass("in");
  $("#edit_SBO_term_on").removeClass("in");
  $("#edit_SBO_term_on_actions").addClass("in");
  $("#edit_SBO_term_off_actions").removeClass("in");
});

function resolve_sbo()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_sbo_name' %}", {'sboterm': $("#sboterm").val()},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "name") {
               		$("#sboterm_name").html(element.toString());
               		$("#sboterm_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());

               }

           });
              $("#edit_SBO_term_off").addClass("in");
              $("#edit_SBO_term_on").removeClass("in");
              $("#edit_SBO_term_on_actions").addClass("in");
              $("#edit_SBO_term_off_actions").removeClass("in");
        },
        function() { console.log("resolve sbo failed"); }

    );
}