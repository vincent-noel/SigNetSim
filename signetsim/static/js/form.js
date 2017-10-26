class Form
{
    constructor(field, description, default_value){

        this.field = field;
        this.description = description;
        this.default_value = default_value;
        this.error_message = "";
    }

    clearValue() {
        $("#" + this.field).val(this.default_value);
    }

    getValue() {
        return $.trim($("#" + this.field).val());
    }

    setValue(value) {
        $("#" + this.field).val(value);
    }

    setError(error_message){
        this.error_message = error_message;
    }

    clearError(){
        this.error_message = "";
    }

    hasError(){
        return this.error_message !== "";
    }

    highlight(){
        $("#" + this.field + "_label").addClass("text-danger");
        $("#" + this.field + "_group").addClass("has-error");
    }
    unhighlight(){
        $("#" + this.field + "_label").removeClass("text-danger");
        $("#" + this.field + "_group").removeClass("has-error");
    }

    clear(){
        this.clearValue();
        this.clearError();
    }

}

let HasIndicator = (superclass) => class extends superclass {
    setIndicatorValid(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_valid").addClass("in");
    }
    setIndicatorInvalid(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_valid").removeClass("in");
        $("#" + this.field + "_invalid").addClass("in");
    }
    setIndicatorValidating(){
        $("#" + this.field + "_valid").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_validating").addClass("in");
    }
    setIndicatorEmpty(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_valid").removeClass("in");
    }
}
