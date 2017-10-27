
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
