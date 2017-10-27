{% load static from staticfiles %}
{% include 'commons/js/editable_input.js' %}

class SBOTermInput extends EditableInput
{
    constructor(field)
    {
        super(field);
    }

    setValue(value) {
        $("#" + this.field).val(value);
    }

    setName(name){
        $("#" + this.field + "_name").html(name);
    }

    setLink(link){
        if (link !== ""){
           $("#" + this.field + "_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + link);
        } else {
            $("#" + this.field + "_link").removeAttr("href");
        }
    }

    resolve()
    {
        ajax_call(
            "POST", "{% url 'get_sbo_name' %}",
            {'sboterm': this.getValue()},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                    if (index === "name")
                    {
                        this.setName(element.toString());
                        this.setLink(this.getValue());
                    }

                });
                super.edit_off();
            },
            () => { console.log("resolve sbo failed"); }

        );
    }



}