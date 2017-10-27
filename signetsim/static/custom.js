function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
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
	if ($("#error_modal").children().length === 0) {
		$("#error_modal").append("\
			<div class=\"alert alert-danger fade in\" id=\"error_modal_list\">\
				<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>\
			</div>\
		");
	}
	if ($("#error_modal_list").find("#error_message_" + message_id).length === 0){
	$("#error_modal_list").append("<span id=\"error_message_" + message_id + "\"><strong>Error : </strong>" + message + "</span><br/>");}
}


function add_error_modal_v2(form, message_prefix) {
    error_modal = $("#error_modal");
	if (error_modal.children().length === 0) {
		error_modal.append(
			"<div class=\"alert alert-danger fade in\" id=\"error_modal_list\">\
				<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>\
			</div>"
		);
	}
	if ($("#error_modal_list").find("#error_message_" + form.id).length === 0){
        $("#error_modal_list").append(
            "<span id=\"error_message_" + form.id
            + "\"><strong>Error : </strong>" + message_prefix
            + " " + form.error_message + "</span><br/>"
        );
	}
}


function add_error_modal_v3(form) {

 	if ($("#error_modal").children().length === 0) {
		$("#error_modal").append(
			"<div class=\"alert alert-danger fade in\" id=\"error_modal_list\">\
				<a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>\
			</div>"
		);
	}
	if ($("#error_modal_list").find("#error_message_" + form.field).length === 0){
        $("#error_modal_list").append(
            "<span id=\"error_message_" + form.field + "\">\
                <strong>Error : </strong>" + form.description + " " + form.error_message + "\
            </span><br/>"
        );
	}
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