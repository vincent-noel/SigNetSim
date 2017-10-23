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
{% for t,y, name in sim_results %}
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

        {% if form.showObservations == True %}
            {% with t_observation=experiment_observations|my_lookup:forloop.counter0 %}
            {% for name in t_observation.getSpecies %}
            {

                label: "{{name}} (Data)",
                data: [
                    {% for data in t_observation.getByVariable|my_lookup:name %}
                    {x: {{data.t}}, y: {{data.value}}},
                    {% endfor %}
                ],

                fill: false,

                {% with t_length=y.keys|length %}
                {% with t_ind_color=forloop.counter0|add:t_length %}
                backgroundColor: "{{colors|get_color:t_ind_color}}",
                borderColor: "{{colors|get_color:t_ind_color}}",
                showLine: false,
                {% endwith %}
                {% endwith %}
            },
            {% endfor %}
            {% endwith %}
        {% endif %}
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
                ticks: {
{#                    beginAtZero: true,#}
{#                    suggestedMax: {{y_max}},#}
                }
            }],
        },
        title:
        {
            display: true,
            {% if sim_results|length > 1 %}
            text: " Condition #{{forloop.counter0}} : {{name}}",
            {% else  %}
            text: "{{ name }}",
            {% endif %}
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
{% for _ in sim_results %}
var chart_{{ forloop.counter0 }} = null;
{% endfor %}

$(window).on('load', function() {

console.log('load');
{% for _ in sim_results %}
    ctx_{{forloop.counter0}} = document.getElementById("canvas_{{forloop.counter0}}").getContext("2d");
    ctx_{{forloop.counter0}}.canvas.height = $("#plots_container").width()*0.5;
    var chart_{{forloop.counter0}} = new Chart(ctx_{{forloop.counter0}}, config_{{forloop.counter0}});
    update_charts_size()

{% endfor %}

});
$(window).on('resize', function () {
    console.log('resize');
    update_charts_size();
});

function update_charts_size()
{
{% for _ in sim_results %}
    if (chart_{{ forloop.counter0 }} != null){
        legend_height = chart_{{forloop.counter0}}.legend.height;
        $("#canvas_{{forloop.counter0}}").css("height", $("#plots_container").width()*0.5 + legend_height);
    }
{% endfor %}
}

$('#toggle_options').on('click', function(){

  if($("#options").hasClass("in")) {
    $("#options").removeClass("in");
    $("#options_2").removeClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-down\"> More");

  } else {
    $("#options").addClass("in");
    $("#options_2").addClass("in");
    $("#toggle_options").html("<span class=\"glyphicon glyphicon-chevron-up\"> Less");
  }
});

function toggle_slide(slide_id) {
  if ($('#' + slide_id).prop('checked') == true) {
    $('#' + slide_id).prop("checked", false);
  } else {
    $('#' + slide_id).prop("checked", true);
  }
}

function toggle_observations() {
  toggle_slide('show_observations');
}

$('#experiment_list li').on('click', function(){
  $("#experiment_name").html($(this).text());
  $('#experiment_id').val($(this).index());
  $("#experiment_selected").addClass("in");

});
