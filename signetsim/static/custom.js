function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajax_call(ajax_method, csrf_token, ajax_url, ajax_data, ajax_done, ajax_fail)
{
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrf_token);
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


function toggle_slide(slide_id)
{
	if ($('#' + slide_id).prop('checked') == true) {
		$('#' + slide_id).prop('checked', false);
	} else {
		$('#' + slide_id).prop('checked', true);
	}
}

function add_error_modal(message_id, message) {
	if ($("#error_modal").children().length == 0) {
		$("#error_modal").append("\
			<div class=\"alert alert-danger fade in\" id=\"error_modal_list\">\
				<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>\
			</div>\
		");
	}
	if ($("#error_modal_list").find("#error_message_" + message_id).length == 0){
	$("#error_modal_list").append("<span id=\"error_message_" + message_id + "\"><strong>Error : </strong>" + message + "</span><br/>");}
}

function form_add_error_highlight(form_id)
{
    $("#" + form_id + "_label").addClass("text-danger");
    $("#" + form_id + "_group").addClass("has-error");

}
function form_remove_error_highlight(form_id)
{
    $("#" + form_id + "_label").removeClass("text-danger");
    $("#" + form_id + "_group").removeClass("has-error");

}

