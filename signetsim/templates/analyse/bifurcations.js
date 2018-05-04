{#   _layout/base.html : This is the top template 							  #}

{#   Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br) 		  #}

{#   This program is free software: you can redistribute it and/or modify     #}
{#   it under the terms of the GNU Affero General Public License as published #}
{#   by the Free Software Foundation, either version 3 of the License, or     #}
{#   (at your option) any later version. 									  #}

{#   This program is distributed in the hope that it will be useful, 		  #}
{#   but WITHOUT ANY WARRANTY; without even the implied warranty of 		  #}
{#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 			  #}
{#   GNU Affero General Public License for more details.					  #}

{#   You should have received a copy of the GNU Affero General Public License #}
{#   along with this program. If not, see <http://www.gnu.org/licenses/>. 	  #}

{% load tags %}


class EquilibriumCurveForm extends FormGroup{

    constructor(field){
        super();
        this.field = field;

        this.parameter = new Dropdown("parameter", "The parameter to vary", null, "", "Choose an parameter", true);
        this.addForm(this.parameter, true);

        this.from_value = new FloatForm("from_value", "The initial value of the parameter", true, 0);
        this.addForm(this.from_value, true);

        this.to_value = new FloatForm("to_value", "The final value of the parameter", true, 100);
        this.addForm(this.to_value, true);

    }

    show(){
        $('#' + this.field).modal('show');
    }

    new(){
        $('#' + this.field + "-title").html("New equilibrium curve");
        this.clearForms();
        this.show();
    }

    submit(){
        this.checkErrors();

        if (this.nb_errors == 0)
        {
            $("#" + this.field).modal("hide");
        }

        return (this.nb_errors == 0);
    }
}

let form_equilibrium = new EquilibriumCurveForm("modal_new_curve");


$('#new_curve_button').on('click', function(){
    $('#modal_new_curve').modal('show');
});

$(window).on('load', function(){
  {% for continuation in list_of_computations %}
  {% if continuation.status == "BU" %}
      update_status_{{forloop.counter0}}();
  {% endif %}
  {% endfor %}


});

{% for continuation in list_of_computations %}
{% if continuation.status == "BU" %}
function update_status_{{forloop.counter0}}()
{
  $("#result_{{forloop.counter0}}_failed").removeClass("in");
  $("#result_{{forloop.counter0}}_finished").removeClass("in");
  $("#result_{{forloop.counter0}}_waiting").addClass("in");

  ajax_call(
	"POST", '{% url 'get_continuation_status' %}',
	{ 'continuation_id': {{forloop.counter0}},},
	(data) =>
	{
		$.each(data, function(index, element)
		{
			if (index === "status" && element === "EN") {
				$("#result_{{forloop.counter0}}_waiting").removeClass("in");
				$("#result_{{forloop.counter0}}_failed").removeClass("in");
				$("#result_{{forloop.counter0}}_finished").addClass("in");

			} else {
				setTimeout(update_status_{{forloop.counter0}}, 5000);
			}
		});
	},
	() =>
	{
		$("#result_{{forloop.counter0}}_waiting").removeClass("in");
		$("#result_{{forloop.counter0}}_finished").removeClass("in");
		$("#result_{{forloop.counter0}}_failed").addClass("in");
	},
  );

}
{% endif %}
{% endfor %}



function view_curve(curve_id)
{
	ajax_call(
		"POST", "{% url 'get_equilibrium_curve' %}",
		{'id': curve_id},
		(data) =>
		{
			var slices_groups = [];
			var group = [];
			config_graph['data']['datasets'] = [];

			x = data['curve_x'];
			$("#modal_modification_title").html(data['parameter']);
			$.each(Object.keys(data['curve_ys']), (i_variable, variable) => {

				// Equilibrium curves
				$.each(data['curve_ys'][variable], (i_slice, slice) => {
					let dataset = {};
					dataset['label'] = variable + " equilibrium";
					dataset['data'] = [];
					$.each(slice, (i, y_i) => {
						dataset['data'].push({'x': x[i_slice][i], 'y': y_i})
					});
					dataset['fill'] = false;
					dataset['pointRadius'] = 0;
					if (data['stability'][i_slice] === 'S') {
						dataset['borderColor'] = colors[i_variable];

					} else if (data['stability'][i_slice] === 'N' || data['stability'][i_slice] === 'U') {
						dataset['borderColor'] = colors[i_variable];
						dataset['borderDash'] = [5, 5]

					} else {
						dataset['borderColor'] = "#ff0000";
					}

					group.push(config_graph['data']['datasets'].length);

					config_graph['data']['datasets'].push(dataset);

				});


				// Limit cycle curves
				if (Object.keys(data).indexOf('curve_lc_x') >= 0 && data['curve_lc_x'].length > 0) {
					let dataset = {};
					dataset['label'] = variable + " limit cycle minimum";
					dataset['data'] = [];
					$.each(data['curve_lc_ys'][variable]['min'], (i, y_i) => {
						dataset['data'].push({'x': data['curve_lc_x'][i], 'y': y_i})
					});
					dataset['fill'] = false;
					dataset['pointRadius'] = 0;
					dataset['borderColor'] = colors[i_variable];

					group.push(config_graph['data']['datasets'].length);
					config_graph['data']['datasets'].push(dataset);

					dataset = {};
					dataset['label'] = variable + " limit cycle maximum";
					dataset['data'] = [];
					$.each(data['curve_lc_ys'][variable]['max'], (i, y_i) => {
						dataset['data'].push({'x': data['curve_lc_x'][i], 'y': y_i})
					});
					dataset['fill'] = false;
					dataset['pointRadius'] = 0;
					dataset['borderColor'] = colors[i_variable];

					group.push(config_graph['data']['datasets'].length);
					config_graph['data']['datasets'].push(dataset);

				}

				// Bifurcation points
				let points_dataset = {};
				points_dataset['label'] = variable + " bifurcation points";
				points_dataset['data'] = [];
				$.each(data['points'][variable], (index, element) => {
					points_dataset['data'].push({'x': element[1],'y': element[2]});
				});
				points_dataset['fill'] = false;
				points_dataset['showLine'] = false;
				points_dataset['backgroundColor'] = colors[i_variable];
				points_dataset['borderColor'] = colors[i_variable];

				group.push(config_graph['data']['datasets'].length);
				config_graph['data']['datasets'].push(points_dataset);

				slices_groups.push(group);
				group = [];

				// Units
				config_graph['options']['scales']['xAxes'][0]['scaleLabel']['labelString'] = data['parameter_unit'];

			});

			config_graph['data']['slices_groups'] = slices_groups;

			// Modifying legend elements to show groups instead of individual datasets
			config_graph['options']['legend']['labels']['filter'] = (legendItem, chartData) => {

				var i = 0;
				while(i < chartData['slices_groups'].length && chartData['slices_groups'][i].indexOf(legendItem.datasetIndex) < 0) { i++; }

				if (i < chartData['slices_groups'].length && legendItem.datasetIndex == chartData['slices_groups'][i][0]) {
					return true;

				} else {return false;}
			}

			// Modifying legend click to use groups
			var original = Chart.defaults.global.legend.onClick;
			Chart.defaults.global.legend.onClick = function(e, legendItem) {

				var index = legendItem.datasetIndex;
				var ci = this.chart;

				var i = 0;
				while(i < ci.data['slices_groups'].length && ci.data['slices_groups'][i].indexOf(index) < 0) { i++; }


				if (i < ci.data['slices_groups'].length && index == ci.data['slices_groups'][i][0]) {

					for (j = 0; j < ci.data['slices_groups'][i].length; j++) {
						var slice_index = ci.data['slices_groups'][i][j];

						if (ci.getDatasetMeta(slice_index).hidden === null){
							ci.getDatasetMeta(slice_index).hidden = !ci.data.datasets[slice_index].hidden;
						} else {
							ci.getDatasetMeta(slice_index).hidden = null;
						}
					}

				} else {

					if (ci.getDatasetMeta(index).hidden === null){
						ci.getDatasetMeta(index).hidden = !ci.data.datasets[index].hidden;
					} else {
						ci.getDatasetMeta(index).hidden = null;
					}
				}

				ci.update();
			};


			$("#modal_result").on('shown.bs.modal', function()
			{
				ctx_graph = document.getElementById("canvas_graph").getContext("2d");
				$("#div_canvas_graph").width($("#modal_result_body").width()*0.9);
				chart_result = new Chart(ctx_graph, config_graph);
			});
			$('#modal_result').modal('show');
		},
		() => { console.log("equilibrium curve retrieving failed"); }
	);
}
