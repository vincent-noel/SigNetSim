
function toggle_slide(slide_id)
{
	if ($('#' + slide_id).prop('checked') == true) {
		$('#' + slide_id).prop('checked', false);
	} else {
		$('#' + slide_id).prop('checked', true);
	}
}
