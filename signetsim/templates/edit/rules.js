function clear_form()
{
  $("#dropdown_variable_name").html("Choose a variable");
  $('#dropdown_variable_id').val("");

  $("#rule_expression").val("");
  $("#rule_expression_alg").val("");

  reset_errors();
}


$('#rule_type_dropdown li').on('click', function(){
  $("#rule_type_name").html($(this).text());
  $('#rule_type').val($(this).index());
  clear_form();

  if ($(this).index() == 0){

    $("#rule_species").removeClass("in");
    $("#rule_exp_others").removeClass("in");
    $("#rule_exp_alg").addClass("in");

  } else {

    $("#rule_species").addClass("in");
    $("#rule_exp_others").addClass("in");
    $("#rule_exp_alg").removeClass("in");
  }

});


$('#dropdown_variables_list li').on('click', function(){
  $("#dropdown_variable_name").html($(this).text());
  $('#dropdown_variable_id').val($(this).index());
});


$('#new_rule_button').on('click', function()
{
  $("#modal_rule-title").html("New rule");

  $("#rule_id").val("");
  $("#rule_type_name").html("Choose a type");
  $("#rule_type").val("");
  clear_form();


  setExpressionEmpty();
  setExpressionAlgEmpty();
  reset_errors();
  $("#rule_species").removeClass("in");
  $("#rule_exp_others").removeClass("in");
  $("#rule_exp_alg").removeClass("in");
  $('#modal_rule').modal('show');
});
var form_exp_error = "";
var form_expalg_error = "";

function setExpressionEmpty()
{
$("#exp_invalid").removeClass("in");
  $("#exp_valid").removeClass("in");
  $("#exp_validating").removeClass("in");

}
function setExpressionValidating()
{
$("#exp_invalid").removeClass("in");
  $("#exp_valid").removeClass("in");
  $("#exp_validating").addClass("in");

}
function setExpressionValid()
{
    $("#exp_invalid").removeClass("in");
    $("#exp_validating").removeClass("in");
    $("#exp_valid").addClass("in");
}
function setExpressionInvalid()
{
    $("#exp_validating").removeClass("in");
    $("#exp_valid").removeClass("in");
    $("#exp_invalid").addClass("in");
}
$("#rule_expression").on('change paste keyup', function()
{
  setExpressionValidating();
  ajax_call(
      "POST", "{{csrf_token}}",
      "{% url 'math_validator' %}",
      {
          'math': $("#rule_expression").val(),
      },
      function(data)
      {
        $.each(data, function(index, element) {
            if (index === 'valid' && element === 'true') {
                setExpressionValid();
                form_exp_error = "";

            } else {
                setExpressionInvalid();
                form_exp_error = "is invalid";

            }
        });
      },
      function()
      {
        setExpressionInvalid();
      });

});


function setExpressionAlgEmpty()
{
$("#expalg_invalid").removeClass("in");
  $("#expalg_valid").removeClass("in");
  $("#expalg_validating").removeClass("in");

}
function setExpressionAlgValidating()
{
$("#expalg_invalid").removeClass("in");
  $("#expalg_valid").removeClass("in");
  $("#expalg_validating").addClass("in");

}
function setExpressionAlgValid()
{
    $("#expalg_invalid").removeClass("in");
    $("#expalg_validating").removeClass("in");
    $("#expalg_valid").addClass("in");
}
function setExpressionAlgInvalid()
{
    $("#expalg_validating").removeClass("in");
    $("#expalg_valid").removeClass("in");
    $("#expalg_invalid").addClass("in");
}

$("#rule_expression_alg").on('change paste keyup', function()
{
  setExpressionAlgValidating();
  ajax_call(
      "POST", "{{csrf_token}}",
      "{% url 'math_validator' %}",
      {
          'math': $("#rule_expression_alg").val(),
      },
      function(data)
      {
        $.each(data, function(index, element) {
            if (index === 'valid' && element === 'true') {
               form_expalg_error = "";
               setExpressionAlgValid();
            } else {
                form_expalg_error = "is invalid";
                setExpressionAlgInvalid();
            }
        });
      },
      function()
      {
        setExpressionAlgInvalid();
      });

});


function view_rule(rule_ind)
{
    $("#modal_rule-title").html("Edit rule");
    setExpressionAlgEmpty();
    setExpressionEmpty();
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_rule' %}", {'rule_ind': rule_ind},
        function(data)
        {
            $.each(data, function(index, element) {
                if (index == "rule_id") { $("#rule_id").val(element); }
                else if (index === "rule_type") {

                  $("#rule_type").val(element.toString());
                  rule_type = element;

                  if (element == 0) {
                    $("#rule_species").removeClass("in");
                    $("#rule_exp_alg").addClass("in");
                    $("#rule_exp_others").removeClass("in");
                  } else {
                    $("#rule_species").addClass("in");
                    $("#rule_exp_others").addClass("in");
                    $("#rule_exp_alg").removeClass("in");
                  }
                }
                else if (index === "rule_type_label") { $("#rule_type_name").html(element.toString()); }
                else if (index === "variable_label") { $("#dropdown_variable_name").html(element.toString()); }
                else if (index === "variable") { $("#dropdown_variable_id").val(element.toString()); }
                else if (index === "expression"){

                  if (rule_type == 0) {
                    $("#rule_expression_alg").val(element);
                  } else {
                    $("#rule_expression").val(element);
                  }
                }
            });

        },
        function() { console.log("failed"); }
    );

    $('#modal_rule').modal('show');

}
function reset_errors()
{
   $("#error_modal").empty();
   // form_exp_error = "";
   // form_expalg_error = "";
}

function save_rule()
{
    var nb_errors = 0;
    reset_errors();

    if ($("#rule_type").val() == ""){
        add_error_modal("no_type", "Please select a rule type");
        nb_errors++;

    } else {

        if ($("#rule_type").val() != 0){

            if ($("#dropdown_variable_id").val() == "") {
                add_error_modal("no_var", "Please select a variable");
                nb_errors++;
            }

            if ($("#rule_expression").val() == "") {
                add_error_modal("empty_exp", "Expression is empty");
                nb_errors++;
            }

        } else {
            if ($("#rule_expression_alg").val() == "") {
                add_error_modal("empty_exp_alg", "Expression is empty");
                nb_errors++;
            }
        }



    }

    if (form_exp_error != ""){
        add_error_modal("invalid_exp", "Expression " + form_exp_error);
        nb_errors++;
    }
    if (form_expalg_error != ""){
        add_error_modal("invalid_expalg", "Expression " + form_expalg_error);
        nb_errors++;
    }

    if (nb_errors == 0)
    {
        $("#rule_form").submit();
    }
}
