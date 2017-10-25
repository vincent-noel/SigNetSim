class Form
{
    constructor(field, description){

        this.field = field;
        this.description = description;
        this.error_message = "";
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
