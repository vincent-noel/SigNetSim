{% for user in users %}

$( "#is_active_{{forloop.counter0}}" ).change(function()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'set_account_active' %}", {'username' : '{{user.username}}', 'status': $("#is_active_{{forloop.counter0}}").prop('checked')},
        function(data) {
           $.each(data, function(index, element) {
             if (index == "result") {console.log(element);}
           });
        },
        function(){}
    );
});

$( "#is_staff_{{forloop.counter0}}" ).change(function()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'set_account_staff' %}", {'username' : '{{user.username}}', 'status': $("#is_staff_{{forloop.counter0}}").prop('checked')},
        function(data) {
           $.each(data, function(index, element) {
             if (index == "result") {console.log(element);}
           });
        },
        function(){}
    );
});

{% endfor %}