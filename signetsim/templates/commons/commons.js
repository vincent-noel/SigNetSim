{% load static from staticfiles %}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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
