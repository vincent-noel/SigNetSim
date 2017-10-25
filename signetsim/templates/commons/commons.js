{% load static from staticfiles %}

function ajax_call(ajax_method, ajax_url, ajax_data, ajax_done, ajax_fail)
{
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
			}
		}
	});
	$.ajax(
	{
		type: ajax_method,
		url: ajax_url,
		data: ajax_data

	})
	.done(ajax_done)
	.fail(ajax_fail)
}


function resolve_sbo()
{
    ajax_call(
        "POST", "{% url 'get_sbo_name' %}",
        {'sboterm': $("#sboterm").val()},
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
