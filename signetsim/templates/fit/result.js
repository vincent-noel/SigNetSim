{% load tags %}


class ModelNameForm extends HasIndicator(Form)
{
    constructor(field, description, default_value="")
    {
        super(field, description, default_value, () => { this.check(); });
        this.initial_value = "";
        this.check();
    }

    setInitialValue(value){
        this.initial_value = value;
    }


    check()
    {
        let name = this.getValue();

        if (name !== "")
        {
            // We actually only need to check
            if (this.initial_value !== name)
            {

                this.setIndicatorValidating();

                ajax_call(
                    "POST", getModelNameValidatorURL(),
                    {'name': name},
                    (data) => {
                        $.each(data, (index, element) => {
                            if (index === 'error')
                            {
                                this.setError(element.toString());
                                if (element == "") {
                                    this.setIndicatorValid();
                                } else {
                                    this.setIndicatorInvalid();
                                }
                            }
                            else
                            {
                                this.setError("couldn't be verified : unknown error");
                                this.setIndicatorInvalid();
                            }
                        });
                    },
                    () => {
                        this.setError("couldn't be verified : connection failed.");
                        this.setIndicatorInvalid();
                    }
                );
            }
            // Otherwise no need to check, it's valid
            else { this.setIndicatorValid(); super.clearError(); }
        }
        else
        {
            this.setError("is empty !");
            this.setIndicatorInvalid();
        }

    }

    clear()
    {
        super.clear();
        super.unhighlight();
        super.setIndicatorEmpty();
    }

}


class FormSaveModel extends  FormGroup {

    constructor(){
        super();

        this.master_model_form = new ModelNameForm("model_name", "The name of the model to save", "{{ model_name|append_string:' (Fitted)' }}");
        this.addForm(this.master_model_form, true);

        {% for name in submodel_names %}
        {% if modified_submodel_names|my_lookup:name %}
        {% with "submodel_"|append_int:forloop.counter0|append_string:"_name" as submodel_id %}
        this.submodel_model_form_{{ forloop.counter0 }} = new ModelNameForm("{{submodel_id}}", "The name of the model to save", "{{ name|append_string:' (Fitted)' }}");
        this.addForm(this.submodel_model_form_{{ forloop.counter0 }}, true);
        {% endwith %}
        {% endif %}
        {% endfor %}
    }

    save(){
        this.checkErrors();
        return (this.nb_errors === 0);
    }
}

let form_save_model = new FormSaveModel();