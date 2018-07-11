

class ListOfSubunits extends ListForm{

    constructor(field, description, parent_form_name, form_name, post_treatment=null) {
        super(field, description, parent_form_name, form_name, post_treatment, true, true);

        this.unit_ids = {
            {% for unit in unit_list %}
            {{ forloop.counter0 }}: "{{ unit }}",
            {% endfor %}
        };

    }

    add(unit_name="", unit_kind="", unit_kind_name="", unit_exponent="", unit_scale="", unit_multiplier=""){
        super.add(
            [
                $("<input>").attr({
                    'type': 'hidden',
                    'id': this.field + '_id_' + this.index.toString(),
                    'name': this.field + '_id_' + this.index.toString(),
                    'value': unit_kind,
                }),
                $("<input>").attr({
                    'type': 'hidden',
                    'id': this.field + '_id_' + this.index.toString() + '_name',
                    'name': this.field + '_id_' + this.index.toString() + '_name',
                    'value': unit_kind_name,
                }),
                $("<input>").attr({
                    'type': 'hidden',
                    'id': this.field + '_exponent_' + this.index.toString(),
                    'name': this.field + '_exponent_' + this.index.toString(),
                    'value': unit_exponent,
                }),
                $("<input>").attr({
                    'type': 'hidden',
                    'id': this.field + '_scale_' + this.index.toString(),
                    'name': this.field + '_scale_' + this.index.toString(),
                    'value': unit_scale,
                }),
                $("<input>").attr({
                    'type': 'hidden',
                    'id': this.field + '_multiplier_' + this.index.toString(),
                    'name': this.field + '_multiplier_' + this.index.toString(),
                    'value': unit_multiplier,
                }),
                $("<td>").attr({'class': 'col-xs-10', 'id': this.field + '_desc_' + this.index.toString()}).text(unit_name)
            ]
            , ""
        );
        this.update();
    }

    remove(element_id){
        super.remove(element_id);
        this.update();
    }

    new()
    {
        $("#unit_edit_id").val("");
        $("#unit_id").val("");
        $("#unit_name").html("Choose unit type");
        $("#unit_exponent").val(1);
        $("#unit_scale").val(1);
        $("#unit_multiplier").val(1);
        $("#unit_button").html("Add")

        $("#edit_unit").addClass("in");
    }


    edit(unit_id)
    {
        $("#unit_edit_id").val(unit_id);
        $("#unit_id").val($("#subunit_id_" + unit_id.toString()).val());
        $("#unit_kind_name").html($("#subunit_id_" + unit_id.toString() + "_name").val());
        $("#unit_exponent").val($("#subunit_exponent_" + unit_id.toString()).val());
        $("#unit_scale").val($("#subunit_scale_" + unit_id.toString()).val());
        $("#unit_multiplier").val($("#subunit_multiplier_" + unit_id.toString()).val());

        if (!$("#edit_unit").hasClass("in")) { $("#edit_unit").addClass("in"); }
    }

    save()
    {
        var desc = "";

        if (parseFloat($("#unit_multiplier").val()) !== 1){
            desc += "(" + $("#unit_multiplier").val() + "."
        }

        if (parseInt($("#unit_scale").val()) === -3){
            desc += "m";
        } else if (parseInt($("#unit_scale").val()) === -6){
            desc += "u";
        } else if (parseInt($("#unit_scale").val()) === -9){
            desc += "n";
        } else if (parseInt($("#unit_scale").val()) === 3){
            desc += "k";
        } else if (parseInt($("#unit_scale").val()) === 6){
            desc += "M";
        } else if (parseInt($("#unit_scale").val()) === 9) {
            desc += "G";
        }
        desc += this.unit_ids[$("#unit_id").val()];
        if (parseFloat($("#unit_exponent").val()) !== 1){
            desc += "^" + $("#unit_exponent").val();
        }

        if (parseFloat($("#unit_multiplier").val()) !== 1){
            desc += ")";
        }

        if ($("#unit_edit_id").val() === ""){
            console.log("This is a new subunit");
            this.add(desc,
                $("#unit_id").val(),
                $("#unit_kind_name").html(),
                $("#unit_exponent").val(),
                $("#unit_scale").val(),
                $("#unit_multiplier").val(),
            );

        } else {
            console.log("This is an existing subunit");
            $("#subunit_desc_" + $("#unit_edit_id").val().toString()).html(desc);
            $("#subunit_id_" + $("#unit_edit_id").val().toString()).val($("#unit_id").val());
            $("#subunit_id_" + $("#unit_edit_id").val().toString() + "_name").val($("#unit_kind_name").html());
            $("#subunit_scale_" + $("#unit_edit_id").val().toString()).val($("#unit_scale").val());
            $("#subunit_exponent_" + $("#unit_edit_id").val().toString()).val($("#unit_exponent").val());
            $("#subunit_multiplier_" + $("#unit_edit_id").val().toString()).val($("#unit_multiplier").val());
            $("#edit_unit").removeClass("in");
        }
        if ($("#edit_unit").hasClass("in")) { $("#edit_unit").removeClass("in"); }
        eval(this.parent_form_name + ".update_desc();");

    }

    update()
    {
        $("#list_units").children("tr").each((tr_id, tr) =>
        {
            $('input', $(tr)).each((input_id, input) =>
            {
                var id = new RegExp('^unit_id_[0-9]+$');
                if (id.test($(td).attr('name')))
                {
                  $(td).attr('name', 'unit_id_' + tr_id.toString());
                }

                var name = new RegExp('^unit_id_[0-9]+_name$');
                if (name.test($(td).attr('name')))
                {
                  $(td).attr('name', 'unit_id_' + tr_id.toString() + '_name');
                }

                var exponent = new RegExp('^unit_exponent_[0-9]+$');
                if (exponent.test($(td).attr('name')))
                {
                  $(td).attr('name', 'unit_exponent_' + tr_id.toString());
                }
                var scale = new RegExp('^unit_scale_[0-9]+$');
                if (scale.test($(td).attr('name')))
                {
                  $(td).attr('name', 'unit_scale_' + tr_id.toString());
                }
                var multiplier = new RegExp('^unit_multiplier_[0-9]+$');
                if (multiplier.test($(td).attr('name')))
                {
                  $(td).attr('name', 'unit_multiplier_' + tr_id.toString());
                }
            });
        });
        super.update();
        eval(this.parent_form_name + ".update_desc();");
    }


}

class FormUnit extends FormGroup
{
    constructor(field){
        super();
        this.field = field;

        this.unit_id = new ValueForm("unit_definition_id", "The id of the unit", "");
        this.addForm(this.unit_id);

        this.name = new ValueForm("unit_definition_name", "The name of the unit", "");
        this.addForm(this.name);

        this.sbmlId = new SbmlIdForm("unit_definition_identifier", "The identifier of the unit", "");
        this.addForm(this.sbmlId, true);

        this.subunits = new ListOfSubunits("subunit", "The list of subunits", "form_unit", "subunits", null);
        this.addForm(this.subunits);
    }

    update_desc()
    {
        let global_desc = "";

        $("#body_subunits").children("tr").each((tr_id, tr) =>
        {

            console.log(global_desc);
            if (tr_id > 0){
                global_desc += ".";
            }
            $('td', $(tr)).each((td_id, td) =>
            {
                var td_re = new RegExp('^subunit_desc_[0-9]+$');
                if (td_re.test($(td).attr('id'))) {
                    global_desc += $(td).html();
                }
            });
        });
        $("#unit_definition_description").html(global_desc);
    }


    show(){
       $("#general").tab('show');
       $("#" + this.field).on('shown.bs.modal', () => { $("#unit_name").focus(); });
       $('#' + this.field).modal('show');
    }

    new(){
        $("#modal_title").html("New unit");
        this.clearForms();
        this.update_desc();
        this.show();
    }

    load(unit_id)
    {
        this.clearForms();
        $("#modal_title").html("Edit unit");

        ajax_call(
            "POST",
            "{% url 'get_unit_definition' %}", {'id': unit_id},
            (data) =>
            {
                this.unit_id.setValue(unit_id)
                $.each(data, (index, element) =>
                {

                   if (index === "unit_id") {
                       this.sbmlId.setValue(element);

                   } else if (index === "name") {
                       this.name.setValue(element);

                   } else if (index === "desc") {
                       $("#unit_definition_description").val(element.toString());

                   } else if (index === "list_of_units") {

                       $.each(element, (subindex, subelement) => {
                            this.subunits.add(
                                subelement[0], subelement[1], subelement[2],
                                subelement[3], subelement[4], subelement[5]
                            );
                       });
                   }
               });
                this.update_desc();

            },
            () => { console.log("failed"); }
        )
        this.show();
    }

    save()
    {
        if (this.nb_errors == 0)
        {
             $("#" + this.field).hide();
        }

        return (this.nb_errors == 0);
    }
}

let form_unit = new FormUnit("new_unit");


$('#unit_kind_list li').on('click', function(){
  $("#unit_kind_name").html($(this).text());
  $('#unit_id').val($(this).index());
});
