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


var config_graph=
{
    type: 'line',

    data:
    {
        datasets: [],
    },

    options:
    {
        scales:
        {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
				scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: ""
                },
            }],
            yAxes: [
            {
                display: true,
                scaleLabel:
                {
                    display: true,
                    fontStyle: "bold",
                    labelString: ""
                },
            }],
        },

		title:
        {
            display: true,
            text: "Equilibrium curve",
        },

        legend:
        {
            display: true,
            position: 'bottom',
            fullWidth: true,
			labels: {},
        },
    }
};

let chart_result = null;
let colors = [ {% for color in colors %}"{{ color }}", {% endfor %}];