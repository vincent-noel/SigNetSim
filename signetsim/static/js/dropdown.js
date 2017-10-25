class Dropdown {
    constructor(field) {
        this.field = field;

        $("#" + this.field + "_list li").on('click', (element) =>
        {
            $("#" + this.field + "_label").html($(element.currentTarget).text());
            $("#" + this.field + "_value").val($(element.currentTarget).index());
        });
    }
}