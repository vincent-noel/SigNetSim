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
{% for curves, points in list_of_figures %}

var config_{{forloop.counter0}}=
{
    type: 'line',

    data:
    {
        datasets: [
		{
			label: "Poil",
			data: [
				{% for x, y in curves %}
				{x: {{ x }}, y: {{ y }} },
				{% endfor %}
			],
			fill: false,
			backgroundColor: "{{colors|get_color:forloop.counter0}}",
			borderColor: "{{colors|get_color:forloop.counter0}}",
			cubicInterpolationMode: "monotone",
			pointRadius: 0
		}
{#        {%  for id, t_y in y.items %}#}
{#        {#}
{##}
{#            label: "{{id}}",#}
{#            data: [#}
{#                {% for tt_y in t_y %}#}
{#                {x: {{t|my_lookup:forloop.counter0}}, y: {{tt_y}}},#}
{#                {% endfor %}#}
{#            ],#}
{##}
{#            fill: false,#}
{#            backgroundColor: "{{colors|get_color:forloop.counter0}}",#}
{#            borderColor: "{{colors|get_color:forloop.counter0}}",#}
{#            cubicInterpolationMode: "monotone",#}
{#        },#}
{#        {% endfor %}#}
{##}
{#        {% if form.showObservations == True %}#}
{#            {% with t_observation=experiment_observations|my_lookup:forloop.counter0 %}#}
{#            {% for name in t_observation.getSpecies %}#}
{#            {#}
{##}
{#                label: "{{name}} (Data)",#}
{#                data: [#}
{#                    {% for data in t_observation.getByVariable|my_lookup:name %}#}
{#                    {x: {{data.t}}, y: {{data.value}}},#}
{#                    {% endfor %}#}
{#                ],#}
{##}
{#                fill: false,#}
{##}
{#                {% with t_length=y.keys|length %}#}
{#                {% with t_ind_color=forloop.counter0|add:t_length %}#}
{#                backgroundColor: "{{colors|get_color:t_ind_color}}",#}
{#                borderColor: "{{colors|get_color:t_ind_color}}",#}
{#                showLine: false,#}
{#                {% endwith %}#}
{#                {% endwith %}#}
{#            },#}
{#            {% endfor %}#}
{#            {% endwith %}#}
{#        {% endif %}#}
        ],
    },

    options:
    {
        scales:
        {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }],
            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Concentration'
                },
            }],
        },
        title:
        {
            display: true,
            text: " Condition #{{forloop.counter0}}",
        },
        legend:
        {
            display: true,
            position: 'bottom',

            fullWidth: true,
        },
    }
};
{% endfor %}

{% for _ in list_of_figures %}
var chart_{{ forloop.counter0 }} = null;
{% endfor %}


{% for figure in list_of_figures %}
$("#modal_result_{{forloop.counter0}}").on('shown.bs.modal', function()
{
	ctx_{{forloop.counter0}} = document.getElementById("canvas_{{forloop.counter0}}").getContext("2d");
	$("#div_canvas_{{ forloop.counter0 }}").width($("#modal_result_{{forloop.counter0}}_body").width()*0.9);
	chart_{{forloop.counter0}} = new Chart(ctx_{{forloop.counter0}}, config_{{forloop.counter0}});
});
{% endfor %}
