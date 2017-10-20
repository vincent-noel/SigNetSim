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
{% for plot_2d in plots_2d %}
var config_{{forloop.counter0}}=
{
    type: 'line',

    data:
    {
        datasets: [
        {% for curve in plot_2d.listOfCurves %}
        {
            label: "{{curve.getYAxisTitle}}",
            data: [
                {% for x_i, y_i in curve.getData %}
                {x: {{x_i}}, y: {{y_i}}},
                {% endfor %}
            ],
            fill: false,
            backgroundColor: "{{colors|get_color:forloop.counter0}}",
            borderColor: "{{colors|get_color:forloop.counter0}}",
//            cubicInterpolationMode: "monotone",

        },
        {% endfor %}
        ],
    },




    options:
    {
        scales:
        {
            xAxes: [{
                type: 'linear',
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: '{{plot_2d.listOfCurves.getXAxisTitle}}'
                },
                position: 'bottom'
            }],
            yAxes: [
            {
                type: 'linear',
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: 'Concentration'
                },
                ticks: {
                    min: 0,
                },
            }]
        },
        title:
        {
          display: true,
          text: "{{plot_2d.getName}}",

        },
        legend:
        {
            display: true,
            position: 'bottom',

            fullWidth: true,
        },
        maintainAspectRatio: false,
    }
};
{% endfor %}

$(window).on('load', function()
{

    {% for plot_2d in plots_2d %}

    ctx_{{forloop.counter0}} = document.getElementById("canvas_{{forloop.counter0}}").getContext("2d");
    ctx_{{forloop.counter0}}.canvas.height = $("#plots_container").width()*0.5;

    chart_{{forloop.counter0}} = new Chart(ctx_{{forloop.counter0}}, config_{{forloop.counter0}});

    {% endfor %}

    update_charts_size();

});

$(window).on('resize', function () {
    update_charts_size();
});

function update_charts_size()
{
    {% for plot_2d in plots_2d %}

    legend_height = chart_{{forloop.counter0}}.legend.height;
    $("#canvas_{{forloop.counter0}}").css("height", $("#plots_container").width()*0.5 + legend_height);

    {% endfor %}
}

