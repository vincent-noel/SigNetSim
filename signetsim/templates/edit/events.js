{% load static from staticfiles %}

class ListOfAssignments extends ListForm{

    constructor(field, description, parent_form_name, form_name, post_treatment=null) {
        super(field, description, parent_form_name, form_name, post_treatment, true);
    }

    add(variable_id="", variable_name="Choose a variable", value=""){
        console.log("adding a field");
        super.add(
            [
                $("<td>").attr('class', 'col-xs-4').append(
                    $("<input>").attr({
                        'type': 'hidden',
                        'id': this.field + '_' + this.index + '_id_value',
                        'name': this.field + '_' + this.index + '_id',
                        'value': variable_id
                    }),
                    $("<div>").attr('class', 'dropdown').append(
                        $("<button>").attr({
                            'type': 'button', 'class': 'btn btn-primary btn-sm dropdown-toggle',
                            'data-toggle': 'dropdown'
                        }).append(
                            $("<span>").attr({
                                'id': this.field + '_' + this.index + '_id_label'
                            }).text(variable_name),
                            $("<span>").attr('class', 'caret')
                        ),
                        $("<ul>").attr({
                            'class': 'dropdown-menu',
                            'id': this.field + '_' + this.index + '_id_list'
                        }).append(
                            {% for var in list_of_variables %}
                            $("<li>").append($("<a>").attr("href", "#").text("{{ var }}")),
                            {% endfor %}
                        )
                    )
                ),
                $("<td>").attr('class', 'col-xs-5').append(
                  $("<input>").attr({
                      'type': 'text',
                      'class': 'form-control input-sm',
                      'placeholder': 'Input assignment expression',
                      'name': this.field + '_' + this.index + '_expression',
                      'id': this.field + '_' + this.index + '_expression',
                      'value': value
                  })
                ),
                $("<td>").attr({'class': 'col-xs-1', 'style': 'vertical-align:middle'}).append(
                    [
                        $("<div>").attr({
                            'id': this.field + '_' + this.index + '_expression_validating',
                            'class' : 'pull-right collapse'
                        }).append($("<img>").attr({'src': '{% static 'images/wait_blue.svg' %}', 'class': 'loading_anim'})),
                        $("<div>").attr({
                            'id': this.field + '_' + this.index + '_expression_valid',
                            'class' : 'pull-right collapse'
                        }).append($("<span>").attr({'class': 'glyphicon glyphicon-ok', 'style': 'color: #5cb85c; font-size: 1.5em'})),
                         $("<div>").attr({
                            'id': this.field + '_' + this.index + '_expression_invalid',
                            'class' : 'pull-right collapse'
                        }).append($("<span>").attr({'class': 'glyphicon glyphicon-remove', 'style': 'color: #d9534f; font-size: 1.5em'})),
                    ]
                )
            ],

        "var " + this.field + "_" + this.index + "_dropdown = new Dropdown('" + this.field + "_" + this.index + "_id', 'The variable of the " + this.index + "th variable', null, '', 'Choose a variable', true);"
            + "form_event.addForm(" + this.field + "_" + this.index + "_dropdown, true);"
            + "var " + this.field + "_" + this.index + "_expression = new MathForm('" + this.field + "_" + this.index + "_expression', 'The expression of the " + this.index + "th assignment', '', true);"
            + "form_event.addForm(" + this.field + "_" + this.index + "_expression, true);"

        );
        this.update();
    }

    remove(element_id){
        eval("form_event.removeForm(" + this.field + '_' + element_id.toString() + '_dropdown' + ");")
        eval("form_event.removeForm(" + this.field + '_' + element_id.toString() + '_expression' + ");")
        super.remove(element_id);
        this.update();
    }

    update(){

        $("#body_" + this.field + "s").children("tr").each((tr_id, tr)=>
        {
            $('input', $(tr)).each((input_id, input) =>
            {
                console.log(input_id);
                let id = new RegExp('^' + this.field + '_[0-9]_expression+$');
                if (id.test($(input).attr('name')))
                {
                    console.log('found expression');
                    $(input).attr('name', this.field + '_' + tr_id.toString() + '_expression');
                }

                let exp = new RegExp('^' + this.field + '_[0-9]+_id');
                if (exp.test($(input).attr('name')))
                {
                    console.log('found variable');
                    $(input).attr('name', this.field + '_' + tr_id.toString() + '_id');
                }
            });
        })
        super.update();
    }


}

class FormEvent extends FormGroup {
    constructor(field){
        super();
        this.field = field;

        this.event_id = new Form("event_id", "The id of the event", "");
        this.addForm(this.event_id);

        this.name = new Form("event_name", "The name of the event", "");
        this.addForm(this.name);

        this.sbmlId = new SbmlIdForm("event_sbmlid", "The identifier of the event", "");
        this.addForm(this.sbmlId, true);

        this.trigger = new MathForm("event_trigger", "The formula of the trigger", "", true)
        this.addForm(this.trigger, true);

        this.delay = new MathForm("event_delay", "The delay of the event", "");
        this.addForm(this.delay, true);

        this.priority = new MathForm("event_priority", "The priority of the event", "");
        this.addForm(this.priority, true);

        this.persistent = new SliderForm(
            "event_persistent", "The persistence of the event", true, null);
        this.addForm(this.persistent);

        this.initial_value = new SliderForm(
            "event_initialvalue", "The initial value of the event", true, null);
        this.addForm(this.initial_value);

        this.usetriggertime = new SliderForm(
            "event_usetriggertime", "The choice of time of the assignements", true, null);
        this.addForm(this.usetriggertime);

        this.assignments = new ListOfAssignments("event_assignment", "The assignments of the event", "form_event", "assignments", null);
        this.addForm(this.assignments, false);
    }

    show(){
       $("#general").tab('show');
       $("#" + this.field).on('shown.bs.modal', () => { $("#event_name").focus(); });
       $('#' + this.field).modal('show');

    }

    new(){
        this.resetErrors();
        this.clearForms();
        this.show();
    }

    load(event_ind)
    {
        $("#modal_event-title").html("Edit events");

        ajax_call(
            "POST",
            "{% url 'get_event' %}", {'event_ind': event_ind},
            (data) =>
            {
                $.each(data, (index, element) => {
                    if (index === "event_ind") {
                        this.event_id.setValue(element);

                    } else if (index === "event_name") {
                        this.name.setValue(element);

                    } else if (index === "event_sbmlid") {
                        this.sbmlId.setValue(element);

                    } else if (index === "event_trigger") {
                        this.trigger.setValue(element);

                    } else if (index === "event_delay") {
                        this.delay.setValue(element);

                    } else if (index === "event_priority") {
                        this.priority.setValue(element);

                    } else if (index == "event_persistent") {
                        this.persistent.setValue(element);

                    } else if (index == "event_initialvalue") {
                       this.initial_value.setValue(element);

                    } else if (index == "event_valuefromtrigger") {
                       this.usetriggertime.setValue(element);

                    } else if (index === "list_of_assignments") {
                        this.assignments.clear();
                        $.each(element, (sub_index, subelement) =>{


                            this.assignments.add(
                                subelement[0], subelement[1], subelement[2]
                            );

                        });
                    }


                });

            },
            () => { console.log("failed"); }
        );

        this.show();
    }

    save()
    {
        this.checkErrors();

        if (this.nb_errors == 0)
        {
            $("#" + this.field).hide();
        }

        return (this.nb_errors === 0);
    }
}

let form_event = new FormEvent("modal_event");
