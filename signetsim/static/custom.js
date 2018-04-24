
function toggle_slide(slide_id)
{
	if ($('#' + slide_id).prop('checked') == true) {
		$('#' + slide_id).prop('checked', false);
	} else {
		$('#' + slide_id).prop('checked', true);
	}
}

function nth(n){return n+(["st","nd","rd"][(((n<0?-n:n)+90)%100-10)%10-1]||"th")}