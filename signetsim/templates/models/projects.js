
class SendProjectForm extends FormGroup {

	constructor(field, description) {

		super("error_" + field);

		this.field = field;
		this.description = description;

		this.id = new ValueForm("modal_send_project_id", "The identifier of the project", "", null);
		this.addForm(this.id);

		this.name = new UsernameForm("modal_send_project_username", "The user to send the project to", true, "");
		this.addForm(this.name, true);

	}

	show(project_id) {
		this.id.setValue(project_id)
		$("#" + this.field).modal('show');
	}


	send() {
		this.checkErrors();

        if (this.nb_errors === 0)
        {
            $("#" + this.field).modal("hide");
        }
        return (this.nb_errors === 0);
	}

}

class ProjectForm extends ModalForm {

	constructor(field, description){

		super(field, description);

		this.id = new ValueForm("modal_project_id", "The identifier of the project", "", null);
		this.addForm(this.id);

		this.name = new ValueForm("modal_project_name", "The name of the project", "", null, true);
		this.addForm(this.name, true);

		this.access = new SliderForm("modal_project_access", "The accessibility of the project", 0, null);
		this.addForm(this.access);
	}

	load(project_id)
	{
		super.load(
			ajax_call(
				"POST",
				"{% url 'get_project' %}", {'id': project_id},
				(data) =>
				{
					$.each(data, (index, element) =>
					{
						if (index === "name") {
							this.name.setValue(element); }

						else if (index === "public")
						{
							if (element === "1") {
								this.access.switch_on();
							}
							else {
								this.access.switch_off();
							}
						}
					});

					this.id.setValue(project_id);
				},
				() => {}
			)
		);
	}
}

let form_project = new ProjectForm('modal_project', 'project');
let form_send_project = new SendProjectForm('modal_send_project', 'Send project');