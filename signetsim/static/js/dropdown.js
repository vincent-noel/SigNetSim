class Dropdown {
    constructor(field, post_treatment=null, default_value="", default_label="Choose an item") {
        this.field = field;
        this.default_value = default_value;
        this.default_label = default_label;

        $("#" + this.field + "_list li").on('click', (element) =>
        {
            this.setLabel($(element.currentTarget).text());
            this.setValue($(element.currentTarget).index());

            if (post_treatment !== null) {
                post_treatment();
            }
        });
    }
    setLabel(label){
        $("#" + this.field + "_label").html(label);
    }

    setValue(value){
        $("#" + this.field + "_value").val(value);
    }

    getLabel(){
        return $("#" + this.field + "_label").html();
    }

    getValue(){
        return parseInt($("#" + this.field + "_value").val());
    }

    clear(){
        this.setLabel(this.default_label);
        this.setValue(this.default_value);
    }
}