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
        datasets: [
        {%  for id, t_y in y.items %}
        {

            label: "{{id}}",
            data: [
                {% for tt_y in t_y %}
                {x: {{t|my_lookup:forloop.counter0}}, y: {{tt_y}}},
                {% endfor %}
            ],

            fill: false,
            backgroundColor: "{{colors|get_color:forloop.counter0}}",
            borderColor: "{{colors|get_color:forloop.counter0}}",
            cubicInterpolationMode: "monotone",
        },
        {% endfor %}

        {% with t_observation=experiment_observations|my_lookup:forloop.counter0 %}
        {%  for id, t_values in t_observation.items %}
        {

            label: "{{id}} (Data)",
            data: [
                {% for tt_t, tt_y in t_values %}
                {x: {{tt_t}}, y: {{tt_y}}},
                {% endfor %}
            ],

            fill: false,

            {% with t_length=y.keys|length %}
            {% with t_ind_color=forloop.counter0|add:t_length %}
            backgroundColor: "{{colors|get_color:t_ind_color}}",
            borderColor: "{{colors|get_color:t_ind_color}}",
            {% endwith %}
            {% endwith %}
            cubicInterpolationMode: "monotone",
        },
        {% endfor %}
        {% endwith %}

        ],
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

        // labels: {
        //   padding: 40,
        //
        // },
        fullWidth: true,
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
                ticks: {
                    beginAtZero: true,
                    suggestedMax: {{y_max}},
                }
            }],
        }
    }
};
{% endfor %}

$(window).on('load', function() {


{% for t,y in sim_results %}
  var ctx_{{forloop.counter0}} = document.getElementById("canvas_{{forloop.counter0}}").getContext("2d");
  ctx_{{forloop.counter0}}.canvas.height = ctx_{{forloop.counter0}}.canvas.width*0.8;
  ctx_{{forloop.counter0}}.scale(10, 10);
  window.myLine_{{forloop.counter0}} = new Chart(ctx_{{forloop.counter0}}, config_{{forloop.counter0}});
{% endfor %}

});
