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

var config_observations_graph =

{
  type: 'line',

  data: {


      datasets: [
      {% for var in observations %}

      {
          label: "{{var.0}}",
          data: [
          {% for sim in var.1 %}
              {x: {{sim.0}}, y: {{sim.1}}},
          {% endfor %}
          ],
          fill: false,
          backgroundColor: "{{colors|get_color:forloop.counter}}",
          borderColor: "{{colors|get_color:forloop.counter}}",
          cubicInterpolationMode: "monotone",
      },


      {% endfor %}

      ],
  },





  options:
  {
      scales: {
          xAxes: [{
              type: 'linear',
              scaleLabel:
              {
                  display: true,
                  fontStyle: "bold",
                  labelString: 'Time (minutes)'
              },
              position: 'bottom'
          }],
          yAxes: [
          {
              display: true,
              scaleLabel:
              {
                  display: true,
                  fontStyle: "bold",
                  labelString: 'Concentration (nM)'
              },
              ticks: {
                  beginAtZero: true,
              }
          }],

      },
       title:
      {
        display: true,
        text: "{{ experiment_name }}, {{ condition_name }}",

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
      maintainAspectRatio: false,

  }

};

$(window).on('load', function() {

  ctx_observations_graph = document.getElementById("observations_graph").getContext("2d");
  ctx_observations_graph.canvas.height = ctx_observations_graph.canvas.width*0.5;
  observations_chart = new Chart(ctx_observations_graph, config_observations_graph);

  update_charts_size();

});

$(window).on('resize', function() {
    update_charts_size();
});

function update_charts_size() {
    legend_height = observations_chart.legend.height;
    $("#observations_graph").css("height", $("#observations_graph").width() * 0.5 + legend_height);
}

