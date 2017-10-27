{% load static from staticfiles %}

class FloatForm extends Form
{
    constructor(field, description, required, default_value=1)
    {
        super(field, description, default_value);
        this.required = required;
        $("#" + this.field).on('paste keyup', () => { this.check(); });

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
    clear() {
        super.clearError();
    }
}
