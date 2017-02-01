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
{% for t,y in sim_results %}
var config_{{forloop.counter0}}=
{
    type: 'line',

    data:
    {
        labels:{{t}},
        datasets: [
        {% for id, t_y in y.items %}
        {
            label: "{{id}}",
            data: {{t_y}},
            fill: false,
            backgroundColor: "{{colors|get_color:forloop.counter0}}",
            borderColor: "{{colors|get_color:forloop.counter0}}",
            cubicInterpolationMode: "monotone",
        },
        {% endfor %}
        ]
    },

    options:
    {
        {% if experiment_conditions_names != None %}
        title:
        {
          display: true,
          text: " Condition #{{forloop.counter0}} : {{ experiment_conditions_names|my_lookup:forloop.counter0 }}",
        },
        {% endif %}


        legend:
        {
            display: true,
            position: "bottom",

            labels: {
              padding: 40,

            },
            fullWidth: true,

        },

        scales:
        {
            xAxes: [
            {
                display: true,

                {% if t_unit != None %}
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: "{{t_unit}}",
                },
                {% endif %}
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0,
                    suggestedMax: {{t_max}},
                    maxTicksLimit: 51,
                },
            }],

            yAxes: [
            {

                display: true,

                {% if y_unit != None %}
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: "{{y_unit}}",
                },
                {% endif %}
                ticks: {
                    beginAtZero: true,
                    suggestedMax: {{y_max}},
                }
            }]
        }
    }
};
{% endfor %}

window.onload = function() {


{% for t,y in sim_results %}
  var ctx_{{forloop.counter0}} = document.getElementById("canvas_{{forloop.counter0}}").getContext("2d");
  ctx_{{forloop.counter0}}.canvas.height = ctx_{{forloop.counter0}}.canvas.width*0.8;
  ctx_{{forloop.counter0}}.scale(10, 10);
  window.myLine_{{forloop.counter0}} = new Chart(ctx_{{forloop.counter0}}, config_{{forloop.counter0}});
{% endfor %}

};
