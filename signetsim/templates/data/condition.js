function new_treatment()
{
    $("#modal_treatment-title").html("New treatment");

    $("#treatment_id").val("");
    $("#treatment_name").val("");
    $("#treatment_time").val("");
    $("#treatment_value").val("");
    $("#treatment_title").html("New treatment");

    $('#treatment_modal').modal('show');
}

function view_treatment(treatment_id)
{

    $("#modal_treatment-title").html("Edit treatment");

    ajax_call(
        "POST",
        "{% url 'get_treatment' %}", {'id': treatment_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "species") { $("#treatment_name").val(element.toString()); }
               else if (index == "time") { $("#treatment_time").val(element.toString()); }
               else if (index == "value") { $("#treatment_value").val(element.toString()); }
           });

           $("#treatment_id").val(treatment_id);


        },
        function(){}
    );

    $('#treatment_modal').modal('show');
}

function save_treatment()
{
    $("#treatment_form").submit()
}

function new_observation()
{
    $("#modal_observation-title").html("New observation");

    $("#observation_id").val("");
    $("#observation_name").val("");
    $("#observation_time").val("");
    $("#observation_value").val("");
    $("#observation_stddevs").val("");
    $("#observation_steady_state").prop("checked", false);
    $("#observation_min_steady_state").val("");
    $("#observation_max_steady_state").val("");

    $('#observation_modal').modal('show');
}

function view_observation(observation_id)
{

    $("#modal_observation-title").html("Edit observation");

    ajax_call(
        "POST",
        "{% url 'get_observation' %}", {'id': observation_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index == "species") { $("#observation_name").val(element.toString()); }
               else if (index == "time") { $("#observation_time").val(element.toString()); }
               else if (index == "value") { $("#observation_value").val(element.toString()); }
               else if (index == "stddev") { $("#observation_stddev").val(element.toString()); }
               else if (index == "steady_state") {
                   if (element == 1){

					   form_steadystates.switch_on();
                       $("#steady_state_on").addClass("in");

                   } else {
					   form_steadystates.switch_off();
                       $("#steady_state_on").removeClass("in");
                   }
               }
               else if (index == "min_steady_state") { $("#observation_min_steady_stateplace").val(element.toString()); }
               else if (index == "max_steady_state") { $("#observation_max_steady_stateplace").val(element.toString()); }
           });

           $("#observation_id").val(observation_id);


        },
        function(){}
    );

    $('#observation_modal').modal('show');
}

function save_observation()
{
    $("#observation_form").submit()
}

let form_steadystates = new SliderForm(
	"observation_steady_state", "Steady states switch", 0,
	() => {
		if ($("#steady_state_on").hasClass("in")) {
        	$("#steady_state_on").removeClass("in");
		} else {
			$("#steady_state_on").addClass("in");
		}
	}
);
