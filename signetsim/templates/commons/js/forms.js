{% load static from staticfiles %}

class FloatForm extends Form
{
    constructor(field, description, required) {
        super(field, description);
        this.required = required;
    }

    check() {
        ajax_call(
            "POST", "{% url 'float_validator' %}",
            {'value' : $.trim($("#" + this.field).val()), 'required': this.required},
            (data) => {
                $.each(data, (index, element) => {
                    if (index == "error"){ this.setError(element.toString()); }
                    else { this.setError("couldn't be validated : unknown response"); }
                });
            },
            () => { this.setError("couldn't be validated : unable to connect"); }
        );
    }
}

class SbmlIdForm extends Form
{
    constructor(field, description) {
        super(field, description);
        this.value = "";
    }

    setValue(value){
        this.value = value;
    }
    check() {
        if (this.value != $.trim($("#" + this.field).val())){
        this.setIndicatorValidating();
        ajax_call(
            "POST", "{% url 'sbml_id_validator' %}",
            {'sbml_id': $.trim($("#" + this.field).val()) },
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
                        this.setError("Unkown error while checking the identifier");
                        this.setIndicatorInValid();
                    }
                });
            },
            () => {
                this.setError("Connection failed while checking the identifier");
                this.setIndicatorInvalid();
            }
        );} else { this.setIndicatorValid(); }
    }

}