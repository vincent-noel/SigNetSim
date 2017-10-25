{% load static from staticfiles %}

class FloatForm extends Form
{
    constructor(field, description, required)
    {
        super(field, description);
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

class SbmlIdForm extends HasIndicator(Form)
{
    constructor(field, description, has_scope=false, scope_field="")
    {
        super(field, description);
        this.value = "";

        // For local parameters, we need to have an extra information : the scope (global, or local to a reaction)
        this.hasScope = has_scope;
        this.scope_field = scope_field
        this.scope = 0;
        $("#" + this.field).on('paste keyup', () => { this.check(); });

    }

    setValue(value){
        this.value = value;
    }

    setScope(scope) {
        this.scope = scope;
    }

    check()
    {
        let sbml_id = $.trim($("#" + this.field).val());
        let scope;
        if (this.hasScope)
             scope = parseInt($("#" + this.scope_field).val());

        // We actually only need to check
        if (
            // If there is no scope, but the value has been changed
            (!this.hasScope && this.value !== sbml_id)

            // Or if there is a scope, and either the value or the scope has been changed
            || (this.hasScope && (this.value !== sbml_id || this.scope !== scope))
        ){

            this.setIndicatorValidating();
            let post_data;
            if (!this.hasScope){
                post_data = {'sbml_id': sbml_id };}
            else{
                post_data = {'sbml_id': sbml_id, 'reaction_id': scope};}

            ajax_call(
                "POST", "{% url 'sbml_id_validator' %}",
                post_data,
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
            );
        }
        // Otherwise no need to check, it's valid
        else { this.setIndicatorValid(); super.clearError(); }
    }

    clear()
    {
        super.clearError();
        super.unhighlight();
        super.setIndicatorEmpty();
        this.scope = 0;
    }
}

class EditableInput extends Form
{
    constructor(field) {
        super(field);
        this.field = field;

        $("#" + this.field + "_edit").on('click', () => { this.edit_on(); });
        $("#" + this.field + "_edit_cancel").on('click', () => { this.edit_off(); });
    }

    edit_on() {
        $("#" + this.field + "_edit_on").addClass("in");
        $("#" + this.field + "_edit_off").removeClass("in");
        $("#" + this.field + "_edit_off_actions").addClass("in");
        $("#" + this.field + "_edit_on_actions").removeClass("in");
    }

    edit_off() {
        $("#" + this.field + "_edit_off").addClass("in");
        $("#" + this.field + "_edit_on").removeClass("in");
        $("#" + this.field + "_edit_on_actions").addClass("in");
        $("#" + this.field + "_edit_off_actions").removeClass("in");
    }

    validate() {
        ;
    }


}

class SBOTermInput extends EditableInput
{
    constructor(field)
    {
        super(field);
    }

    resolve()
    {
        ajax_call(
            "POST", "{% url 'get_sbo_name' %}",
            {'sboterm': $("#" + this.field).val()},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                   if (index == "name") {
                        $("#" + this.field + "_name").html(element.toString());
                        $("#" + this.field + "_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());
                   }

               });
                super.edit_off();
            },
            () => { console.log("resolve sbo failed"); }

        );
    }

}