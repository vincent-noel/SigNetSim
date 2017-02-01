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

{% if form.hasErrors == True or form.isEditing == True %}
    $(window).on('load', function(){
        $('#modal_new_curve').modal('show');
    });
{% endif %}

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

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{csrf_token}}");
            }
        }
    });

    $.ajax(
    {
        type: "POST",
        url: '{% url 'get_continuation_status' %}',
        data: {
            'continuation_id': {{forloop.counter0}},
        },

    })
    .done(function(data)
    {
        $.each(data, function(index, element) {

          if (index === "status" && element === "EN"){

            $("#result_{{forloop.counter0}}_waiting").removeClass("in");
            $("#result_{{forloop.counter0}}_failed").removeClass("in");
            $("#result_{{forloop.counter0}}_finished").addClass("in");

          } else {
            setTimeout(update_status_{{forloop.counter0}}, 5000);

          }


        });


    })
    .fail(function()
    {
      $("#result_{{forloop.counter0}}_waiting").removeClass("in");
      $("#result_{{forloop.counter0}}_finished").removeClass("in");
      $("#result_{{forloop.counter0}}_failed").addClass("in");
    })

}
{% endif %}
{% endfor %}
