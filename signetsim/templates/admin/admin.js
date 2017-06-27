{% for user in users %}

$( "#is_active_{{forloop.counter0}}" ).change(function()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'set_account_active' %}", {'username' : '{{user.username}}', 'status': $("#is_active_{{forloop.counter0}}").prop('checked')},
        function(data) {
           $.each(data, function(index, element) {
                if (index == "result" && element != "ok") {
                    if ($("#is_active_{{forloop.counter0}}").prop('checked') == true) {
                        $("#is_active_{{forloop.counter0}}").prop('checked', false);
                    } else {
                        $("#is_active_{{forloop.counter0}}").prop('checked', true);
                    }
                }
           });
        },
        function() {
            if ($("#is_active_{{forloop.counter0}}").prop('checked') == true) {
                $("#is_active_{{forloop.counter0}}").prop('checked', false);
            } else {
                $("#is_active_{{forloop.counter0}}").prop('checked', true);
            }
        }
    );
});

$( "#is_staff_{{forloop.counter0}}" ).change(function()
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'set_account_staff' %}", {'username' : '{{user.username}}', 'status': $("#is_staff_{{forloop.counter0}}").prop('checked')},
        function(data) {
           $.each(data, function(index, element) {
             if (index == "result" && element != "ok")
             {
                 if ($("#is_staff_{{forloop.counter0}}").prop('checked') == true) {
                    $("#is_staff_{{forloop.counter0}}").prop('checked', false);
                 } else {
                    $("#is_staff_{{forloop.counter0}}").prop('checked', true);
                 }
             }
           });
        },
        function() {
            if ($("#is_staff_{{forloop.counter0}}").prop('checked') == true) {
                $("#is_staff_{{forloop.counter0}}").prop('checked', false);
            } else {
                $("#is_staff_{{forloop.counter0}}").prop('checked', true);
            }
        }
    );
});

{% endfor %}