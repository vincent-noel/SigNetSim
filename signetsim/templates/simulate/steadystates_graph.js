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
var config=
{
    type: 'line',

    data:
    {
        datasets: [
        {%  for id, t_y in sim_results.items %}
        {

            label: "{{id}}",
            data: [
                {% for tt_y in t_y %}
                {x: {{steady_states|my_lookup:forloop.counter0}}, y: {{tt_y}}},
                {% endfor %}
            ],

            fill: false,
            backgroundColor: "{{colors|get_color:forloop.counter0}}",
            borderColor: "{{colors|get_color:forloop.counter0}}",
            cubicInterpolationMode: "monotone",
        },
        {% endfor %}

        ],
    },

    title:
    {
      display: true,
      text: " Condition ",

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
                type: 'linear',
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

$(window).on('load', function() {

  var ctx = document.getElementById("canvas").getContext("2d");
  ctx.canvas.height = ctx.canvas.width*0.8;
  ctx.scale(10, 10);
  window.myLine = new Chart(ctx, config);

});
