{% for user in users %}
{% if user.is_superuser != True %}

let form_isactive_{{ forloop.counter0 }} = new SliderForm(
	'is_active_{{ forloop.counter0 }}',
	"The activity of the " + nth({{ forloop.counter }}) + " account",
	{% if user.is_active %}1{% else %}0{% endif %},
	() => {
		ajax_call(
			"POST",
			"{% url 'set_account_active' %}",
			{
				'username': '{{user.username}}',
				'status': form_isactive_{{ forloop.counter0 }}.getValue()
			},
			(data) => {
			   $.each(data, (index, element) => {
					if (index == "result" && element != "ok") {
						if (form_isactive_{{ forloop.counter0 }}.getValue() === true) {
							$("#is_active_{{forloop.counter0}}").prop('checked', false);
						} else {
							$("#is_active_{{forloop.counter0}}").prop('checked', true);
						}
					}
			   });
			},
			() => {
				if ($("#is_active_{{forloop.counter0}}").prop('checked') == true) {
					$("#is_active_{{forloop.counter0}}").prop('checked', false);
				} else {
					$("#is_active_{{forloop.counter0}}").prop('checked', true);
				}
			}
		);
	}

);

let form_isstaff_{{ forloop.counter0 }} = new SliderForm(
	'is_staff_{{ forloop.counter0 }}',
	"The staff membership of the " + nth({{ forloop.counter }}) + " account",
	{% if user.is_staff %}1{% else %}0{% endif %},
	() => {

		ajax_call(
			"POST",
			"{% url 'set_account_staff' %}",
			{'username' : '{{user.username}}', 'status': $("#is_staff_{{forloop.counter0}}").prop('checked')},
			(data) => {
			   $.each(data, (index, element) => {
				 if (index == "result" && element != "ok")
				 {
					 if ($("#is_staff_{{forloop.counter0}}").prop('checked') == true) {
						$("#is_staff_{{forloop.counter0}}").prop('checked', false);
					 } else {
						$("#is_staff_{{forloop.counter0}}").prop('checked', true);
					 }
				 }
			   });
			},
			() => {
				if ($("#is_staff_{{forloop.counter0}}").prop('checked') == true) {
					$("#is_staff_{{forloop.counter0}}").prop('checked', false);
				} else {
					$("#is_staff_{{forloop.counter0}}").prop('checked', true);
				}
			}
		);
	}
);

{% endif %}
{% endfor %}