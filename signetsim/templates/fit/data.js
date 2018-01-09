
class ListOfDatasets {
    constructor(field, description, parent_form_name, form_name, post_treatment=null, removable=true, editable=false) {
        this.field = field;
        this.description = description;
        this.parent_form_name = parent_form_name;
        this.form_name = form_name;
        this.index = 0;
        this.post_treatment = post_treatment;
        this.removable = removable;
        this.editable = editable;
        this.error_messages = [];
    }

    add(id, experiment_name, variables)
    {
        let buttons = $("<div>").attr({'class': 'form-inline pull-right'});

        buttons.append(
            [
                $("<button>").attr({
                    'type': 'button',
                    'onclick': 'toggle_list_' + this.index.toString() + "();",
                    'class': 'btn btn-info btn-xs'
                })
                .append(
                    $("<span>").attr({
                        'class': 'glyphicon glyphicon-link'
                    })
                ),
                "&nbsp;",
                $("<button>").attr({
                    'type': 'button',
                    'onclick': this.parent_form_name + "." + this.form_name + ".remove(" + this.index + ")",
                    'class': 'btn btn-danger btn-xs'
                })
                .append(
                    $("<span>").attr({
                        'class': 'glyphicon glyphicon-remove'
                    })
                ),
            ]
        );

        $("#body_" + this.field + "s").append(
            $("<tr>").attr({'class': 'row', 'id': this.field + "_" + this.index.toString() + "_tr"}).append(
                [
                    $("<td>").attr({'class': 'col-xs-10 col-md-11 active'}).append([
                        $("<span>").text(experiment_name),
                        $("<div>").attr({'class': 'collapse container-fluid', 'id': 'list_species_' + this.index.toString()}).append([
                            $("<br>"),
                            $("<table>").attr({'class': 'table table-bordered'}).append([
                                $("<thead>").append(
                                    $("<tr>").attr('class', 'row').append([
                                        $("<th>").attr('class', 'col-xs-12').text("Mapping"),
                                    ])
                                ),
                                $("<tbody>").attr({'id': 'list_variables_' + this.index.toString()}).append(),

                            ]),
                            $("<br>")
                        ])
                    ]),
                $("<td>").attr({'class': 'col-xs-2 col-md-1 text-right active'}).append(buttons),
                $("<script>").append("function toggle_list_" + this.index.toString() + "(){$('#list_species_" + this.index.toString() + "').collapse('toggle'); }"),
                $("<input>").attr({'type': 'hidden', 'id': 'dataset_' + this.index.toString(), 'name': 'dataset_' + this.index.toString(), 'value': id.toString()})
            ])
        );

        let i_var = 0;
        for (name in variables){
            $("#list_variables_" + this.index.toString()).append(
                  $("<tr>").attr('class', 'row').append([
                      $("<td>").attr('class', 'col-xs-6').text(name),
                      $("<div>").attr("class", "dropdown").append([
                          $("<button>").attr({
                              'id': this.field + "_" + this.index.toString() + "_species_" + i_var.toString() + "_dropdown",
                              'type': 'button',
                              'class': 'btn btn-primary dropdown-toggle',
                              'data-toggle': 'dropdown'
                          }).append([
                              $("<span>").attr(
                                  'id', this.field + "_" + this.index.toString() + "_species_" + i_var.toString() + "_label"
                              ).text((variables[name] == null?"Choose a species":variables[name]) + " "),
                              $("<span>").attr('class', 'caret')
                          ]),
                          $("<ul>").attr({
                              'id': this.field + "_" + this.index.toString() + "_species_" + i_var.toString() + "_list",
                              'class': 'dropdown-menu'
                          }).append([
                              {% for species in list_of_species %}
                              $("<li>").append($("<a>").text("{{ species.getNameOrSbmlId }}")),
                              {% endfor %}
                          ]),
                          $("<script>").text(
                              "var " + this.field + "_" + this.index.toString() + "_species_" + i_var.toString() + "_dropdown = new Dropdown('" + this.field + "_" + this.index.toString() + "_species_" + i_var.toString() + "', 'The " + this.index.toString() + "th parameter', null, default_value='', default_label='Choose a species');"
                          )
                      ])
                  ])
            );
            i_var++;
        }

        this.index++;
    }

    remove(element_id)
    {
        $("#" + this.field + "_" + element_id + "_tr").remove();
    }

    edit(element_id)
    {

    }

    update()
    {

        if (this.post_treatment !== null) {
            this.post_treatment();
        }
    }

    clear()
    {
        $("#body_" + this.field + "s").empty();
        this.index = 0;
    }

    getExperiments()
    {
        let result = [];
        $("#body_" + this.field + "s").children("tr").each((index, element) =>
        {
            result.push($($(element).children("td")[0]).children("span")[0].innerText);
        });
        return result;
    }
}



class FormFit extends FormGroup{

    constructor() {
        super();
        this.form_list_datasets = new ListOfDatasets("list_dataset", "List of datasets", "form_fit", "form_list_datasets", null);
        this.addForm(this.form_list_datasets);

        this.form_dataset = new Dropdown("available_datasets", "list of available datasets", () => { this.add_dataset(); }, "", "Choose an experimental dataset");
        this.addForm(this.form_dataset);
    }

    add_dataset()
    {
        ajax_call(
                "POST",
                "{% url 'add_dataset' %}", {'dataset_ind': this.form_dataset.getValue()},
                (data) =>
                {
                    console.log(data);
                    if (this.form_list_datasets.getExperiments().indexOf(data['dataset_name']) < 0 && Object.keys(data['model_variables']).length > 0){
                        this.form_list_datasets.add(data['dataset_id'], data['dataset_name'], data['model_variables']);
                    }
                },
                () => { console.log("failed"); }
            );
    }

}

let form_fit = new FormFit();


{% for parameter in selected_parameters %}

  $("#select_parameter_{{forloop.counter0}}").on('click', function(){

		if ($(this).prop('checked')){
			$("#parameter_{{forloop.counter0}}_min_input").prop('disabled', false);
			$("#parameter_{{forloop.counter0}}_value_input").prop('disabled', false);
			$("#parameter_{{forloop.counter0}}_max_input").prop('disabled', false);
			$("#parameter_{{forloop.counter0}}_active").val(1);

		} else {
			$("#parameter_{{forloop.counter0}}_min_input").prop('disabled', true);
			$("#parameter_{{forloop.counter0}}_value_input").prop('disabled', true);
			$("#parameter_{{forloop.counter0}}_max_input").prop('disabled', true);
			$("#parameter_{{forloop.counter0}}_active").val(0);
		}

  });


  $("#parameter_{{forloop.counter0}}_value_input").change(function() {
		$("#parameter_{{forloop.counter0}}_value").val($(this).val());
  });

  $("#parameter_{{forloop.counter0}}_min_input").change(function() {
		$("#parameter_{{forloop.counter0}}_min").val($(this).val());
  });

  $("#parameter_{{forloop.counter0}}_max_input").change(function() {
		$("#parameter_{{forloop.counter0}}_max").val($(this).val());
  });

{% endfor %}
