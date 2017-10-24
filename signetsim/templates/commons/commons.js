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


function check_float(form)
{
    ajax_call(
        "POST", "{% url 'float_validator' %}",
        {'value' : $.trim($("#" + form.field).val()), 'required': form.required},
        function(data) {
           $.each(data, function(index, element) {
             if (index == "error")
                 form.error_message = element.toString();
             else
                 form.error_message = "";
           });
        },
        function(){}
    );
}

function check_sbmlid(form, on_success, on_error)
{
     ajax_call(
        "POST", "{% url 'sbml_id_validator' %}",
         {'sbml_id': $.trim($("#" + form.field).val()) },
        function(data)
        {
            $.each(data, function(index, element) {
                if (index === 'error')
                {
                    form.error_message = element.toString();
                    if (element == "") {
                        on_success();
                    } else {
                        on_error();
                    }
                }
                else{
                    form.error_message = "Unkown error while checking the identifier";
                    on_error();
                }
            });
        },
        function()
        {
            form.error_message = "Connection failed while checking the identifier";
            on_error();
        }
    );
}