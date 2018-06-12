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


class UserQuotasForm extends FormGroup {

	constructor(field, description){

		super();

		this.field = field;
		this.description = description;

		this.user_cores = new ValueForm("user_cores", "The maximum number of cores", "", null, true);
		this.addForm(this.user_cores, true);

		this.user_cpu_time = new ValueForm("user_cpu_time", "The maximum number of CPU hours", "", null, true);
		this.addForm(this.user_cpu_time, true);

	}

	load(username)
	{

		ajax_call(
			"POST",
			"{% url 'get_user_quotas' %}", {'username': username},
			(data) =>
			{
				$("#user_username").val(username);
				this.user_cores.setValue(data['max_cpu']);
				this.user_cpu_time.setValue(data['max_time']);
				$("#user_used_cpu_time").val(data['used_time']);
			},
			() => {}
		);
		$('#' + this.field).modal('show');

	}

	reset()
	{
		$("#user_used_cpu_time").val(0);
	}

	save() {

		this.checkErrors();

        if (this.nb_errors == 0)
        {
            $("#" + this.field).modal("hide");
        }
        return (this.nb_errors == 0);
	}
}

let form_quotas = new UserQuotasForm('user_quotas', "The user quotas");
{% endif %}
{% endfor %}