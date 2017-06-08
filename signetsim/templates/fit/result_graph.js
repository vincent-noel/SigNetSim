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

{% for experiment in experiments %}
{% for condition in experiment %}
var config_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}} =
{
  type: 'line',

  data: {


      datasets: [
      {% for var in condition %}
      {

          label: "Model",
          data: [
          {% for obs in var.0 %}
              {x: {{obs.0}}, y: {{obs.1}}},
          {% endfor %}
          ],
          fill: false,
          backgroundColor: "{{colors|my_model_color:forloop.counter0}}",
          borderColor: "{{colors|my_model_color:forloop.counter0}}",
          cubicInterpolationMode: "monotone",

      },
      {
          label: "Data",
          data: [
          {% for sim in var.1 %}
              {x: {{sim.0}}, y: {{sim.1}}},
          {% endfor %}
          ],
          fill: false,
          backgroundColor: "{{colors|my_data_color:forloop.counter0}}",
          borderColor: "{{colors|my_data_color:forloop.counter0}}",
          cubicInterpolationMode: "monotone",

      },
      {% endfor %}
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
      position: "bottom",

      labels: {
        padding: 40,

      },
      fullWidth: true,
  },



  options: {
          scales: {
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
                  }
              }],

          }
      }

};
{% endfor %}
{% endfor %}

var config_score =
{
    type: 'line',

    data:
    {
        labels:{{score_time}},
        datasets: [

            {
                label: "Score",
                data: {{score_values}},
                fill: false,
                backgroundColor: "{{colors|get_color:0}}",
                borderColor: "{{colors|get_color:0}}",
            },
            {
                label: "Raw score",
                data: {{score_rawvalues}},
                fill: false,
                backgroundColor: "{{colors|get_color:1}}",
                borderColor: "{{colors|get_color:1}}",
            },
            {
                label: "Max ev",
                data: {{score_maxev}},
                fill: false,
                backgroundColor: "{{colors|get_color:2}}",
                borderColor: "{{colors|get_color:2}}",
            },



        ]
    },

    options:
    {

        title:
        {
          display: true,

        },

        legend:
        {
            display: true,
            position: "bottom",

            labels: {
              padding: 40,

            },
        },

        scales:
        {

            xAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                },
                ticks: {
                    maxTicksLimit: 11,
                }
            }],

            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                },
                ticks: {
                    beginAtZero: true,
                }
            }]
        }
    }
};



window.onload = function() {


  var ctx_score = document.getElementById("optim_score").getContext("2d");
  ctx_score.canvas.height = ctx_score.canvas.width*0.5;
  ctx_score.scale(10, 10);
  window.myLine_score = new Chart(ctx_score, config_score);


  {% for experiment in experiments %}
  {% for condition in experiment %}

  var ctx_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}} = document.getElementById("optim_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}}").getContext("2d");
  ctx_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}}.canvas.height = ctx_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}}.canvas.width*0.3;
  ctx_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}}.scale(10, 10);

  window.myLine_{{forloop.parentloop.counter0}}_{{forloop.counter0}} = new Chart(ctx_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}},config_result_{{forloop.parentloop.counter0}}_{{forloop.counter0}});

  {% endfor %}
  {% endfor %}


};
