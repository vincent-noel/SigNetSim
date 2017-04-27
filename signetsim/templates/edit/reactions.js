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

var nb_reactants = {{form.listOfReactants|length}} - 1;
var nb_modifiers = {{form.listOfModifiers|length}} - 1;
var nb_products = {{form.listOfProducts|length}} - 1;

function updateReactantsForm()
{
    var r_id = 0;

    $("#body_reactants").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^reaction_reactant_[0-9]+_id$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'reaction_reactant_' + r_id.toString() + '_id');
            }

            var exp = new RegExp('^reaction_reactant_[0-9]+_expression$');
            if (exp.test($(this).attr('name')))
            {
                $(this).attr('name', 'reaction_reactant_' + r_id.toString() + '_expression');
            }
        });
        r_id = r_id + 1;
    });
    buildReactionDescription();
}

function add_reactant(){
    nb_reactants = nb_reactants + 1;
    $("#body_reactants").append("\
    <tr class=\"row\" id=\"reaction_reactant_" + nb_reactants.toString() + "_tr\">\
      <td class=\"col-xs-3\">\
        <input type=\"text\" class=\"form-control input-sm text-center\" placeholder=\"Input stoichiometry\" \
          name=\"reaction_reactant_" + nb_reactants.toString() + "_stoichiometry\" value=\"1\">\
      </td>\
      <td class=\"col-xs-7\">\
        <input type=\"hidden\" id=\"reaction_reactant_" + nb_reactants.toString() + "\"\
          name=\"reaction_reactant_" + nb_reactants.toString() + "\" value=\"\">\
        <div class=\"dropdown\">\
          <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
            <span id=\"reaction_reactant_" + nb_reactants.toString() + "_label\">Choose a specie</span>\
            <span class=\"caret\"></span>\
          </button>\
          <ul id=\"reaction_reactant_" + nb_reactants.toString() + "_dropdown\" class=\"dropdown-menu\">\
            {% for species in list_of_species %}<li><a href=\"#\">{{ species }}</a></li>{% endfor %}\
          </ul>\
        </div>\
      </td>\
      <td class=\"col-xs-2 text-right\">\
        <button type=\"button\" onclick=\"remove_reactant(" + nb_reactants.toString() + ");\"\
          class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-remove\"></span></button>\
      </td>\
    </tr>\
    ");

    $('<script>')
      .attr('type', 'text/javascript')
      .text("\
        $('#reaction_reactant_" + nb_reactants.toString() + "_dropdown li').on('click', function(){\
          $('#reaction_reactant_" + nb_reactants.toString() + "_label').html($(this).text());\
          $('#reaction_reactant_" + nb_reactants.toString() + "').val($(this).index());\
          buildReactionDescription();});\
          ")
      .appendTo('#reaction_reactant_' + nb_reactants.toString());

    updateReactantsForm();

}

function remove_reactant(reactant_id)
{
    $("#reaction_reactant_" + reactant_id + "_tr").remove();
    updateReactantsForm();
}


function updateModifiersForm()
{
    var m_id = 0;

    $("#body_modifiers").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^reaction_modifier_[0-9]+_id$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'reaction_modifier_' + m_id.toString() + '_id');
            }

            var exp = new RegExp('^reaction_modifier_[0-9]+_expression$');
            if (exp.test($(this).attr('name')))
            {
                $(this).attr('name', 'reaction_modifier_' + m_id.toString() + '_expression');
            }
        });
        m_id = m_id + 1;
    });
    buildReactionDescription();
}

function add_modifier(){
    nb_modifiers = nb_modifiers + 1;
    $("#body_modifiers").append("\
    <tr class=\"row\" id=\"reaction_modifier_" + nb_modifiers.toString() + "_tr\">\
      <td class=\"col-xs-3\">\
        <input type=\"text\" class=\"form-control input-sm text-center\" placeholder=\"Input stoichiometry\" \
          name=\"reaction_modifier_" + nb_modifiers.toString() + "_stoichiometry\" value=\"1\">\
      </td>\
      <td class=\"col-xs-7\">\
        <input type=\"hidden\" id=\"reaction_modifier_" + nb_modifiers.toString() + "\"\
          name=\"reaction_modifier_" + nb_modifiers.toString() + "\" value=\"\">\
        <div class=\"dropdown\">\
          <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
            <span id=\"reaction_modifier_" + nb_modifiers.toString() + "_label\">Choose a specie</span>\
            <span class=\"caret\"></span>\
          </button>\
          <ul id=\"reaction_modifier_" + nb_modifiers.toString() + "_dropdown\" class=\"dropdown-menu\">\
            {% for species in list_of_species %}<li><a href=\"#\">{{ species }}</a></li>{% endfor %}\
          </ul>\
        </div>\
      </td>\
      <td class=\"col-xs-2 text-right\">\
        <button type=\"button\" onclick=\"remove_modifier(" + nb_modifiers.toString() + ");\"\
          class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-remove\"></span></button>\
      </td>\
    </tr>\
    ");

    $('<script>')
      .attr('type', 'text/javascript')
      .text("\
        $('#reaction_modifier_" + nb_modifiers.toString() + "_dropdown li').on('click', function(){\
          $('#reaction_modifier_" + nb_modifiers.toString() + "_label').html($(this).text());\
          $('#reaction_modifier_" + nb_modifiers.toString() + "').val($(this).index());\
          buildReactionDescription();});\
          ")
      .appendTo('#reaction_modifier_' + nb_modifiers.toString());
      updateModifiersForm();

}

function remove_modifier(modifier_id)
{
    $("#reaction_modifier_" + modifier_id + "_tr").remove();
    updateModifiersForm();
}

function updateProductsForm()
{
    var p_id = 0;

    $("#body_products").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^reaction_product_[0-9]+_id$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'reaction_product_' + p_id.toString() + '_id');
            }

            var exp = new RegExp('^reaction_product_[0-9]+_expression$');
            if (exp.test($(this).attr('name')))
            {
                $(this).attr('name', 'reaction_product_' + p_id.toString() + '_expression');
            }
        });
        p_id = p_id + 1;
    });
    buildReactionDescription();
}

function add_product(){
    nb_products = nb_products + 1;
    $("#body_products").append("\
    <tr class=\"row\" id=\"reaction_product_" + nb_products.toString() + "_tr\">\
      <td class=\"col-xs-3\">\
        <input type=\"text\" class=\"form-control input-sm text-center\" placeholder=\"Input stoichiometry\" \
          name=\"reaction_product_" + nb_products.toString() + "_stoichiometry\" value=\"1\">\
      </td>\
      <td class=\"col-xs-7\">\
        <input type=\"hidden\" id=\"reaction_product_" + nb_products.toString() + "\"\
          name=\"reaction_product_" + nb_products.toString() + "\" value=\"\">\
        <div class=\"dropdown\">\
          <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
            <span id=\"reaction_product_" + nb_products.toString() + "_label\">Choose a specie</span>\
            <span class=\"caret\"></span>\
          </button>\
          <ul id=\"reaction_product_" + nb_products.toString() + "_dropdown\" class=\"dropdown-menu\">\
            {% for species in list_of_species %}<li><a href=\"#\">{{ species }}</a></li>{% endfor %}\
          </ul>\
        </div>\
      </td>\
      <td class=\"col-xs-2 text-right\">\
        <button type=\"button\" onclick=\"remove_product(" + nb_products.toString() + ");\"\
          class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-remove\"></span></button>\
      </td>\
    </tr>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
        $('#reaction_product_" + nb_products.toString() + "_dropdown li').on('click', function(){\
          $('#reaction_product_" + nb_products.toString() + "_label').html($(this).text());\
          $('#reaction_product_" + nb_products.toString() + "').val($(this).index());\
          buildReactionDescription();});")
      .appendTo('#reaction_product_' + nb_products.toString() + '_tr');
    updateProductsForm();

}

function remove_product(product_id)
{
    $("#reaction_product_" + product_id + "_tr").remove();
    updateProductsForm();
}

function removeReactants()
{
  $("#body_reactants").children("tr").each(function() {
    $(this).remove();
  });
}

function removeModifiers()
{
  $("#body_modifiers").children("tr").each(function() {
    $(this).remove();
  });
}

function removeProducts()
{
  $("#body_products").children("tr").each(function() {
    $(this).remove();
  });
}


function toggle_reversible() {

    if ($('#reaction_reversible').prop('disabled') == false) {

        if ($('#reaction_reversible').prop('checked') == true)
        {
            $('#reaction_reversible').prop("checked", false);
        } else {
            $('#reaction_reversible').prop("checked", true);
        }
        updateParameters($('#new_reaction_type_dropdown li').index(),$('#reaction_reversible').prop('checked'));
        buildReactionDescription();
    }
}


function updateReversibleToggle(reaction_type){

  switch(reaction_type) {
  {% for t_type in reaction_types %}
    case {{forloop.counter0}}:
    {% if allow_reversible|my_lookup:forloop.counter0 == True %}
        $('#reaction_reversible').prop('disabled', false);
    {% else %}
        $('#reaction_reversible').prop('checked', false);
        $('#reaction_reversible').prop('disabled', true);
    {% endif %}
        break;
  {% endfor %}
  }
}
function updateParameters(reaction_type, reversible){

  removeParameters();

  switch(reaction_type) {
    {% for t_type in reaction_types %}
        case {{forloop.counter0}}:
          {% if allow_reversible|my_lookup:forloop.counter0 == True %}
          if (reversible == true){
              {% for parameter in parameters_list|my_lookup:forloop.counter0|my_lookup:True %}
              addParameter({{forloop.counter0}}, "{{parameter}}");
              {% endfor %}
          } else {
              {% for parameter in parameters_list|my_lookup:forloop.counter0|my_lookup:False %}
              addParameter({{forloop.counter0}}, "{{parameter}}");
              {% endfor %}
          }
          {% else %}
          {% for parameter in parameters_list|my_lookup:forloop.counter0|my_lookup:False %}
          addParameter({{forloop.counter0}}, "{{parameter}}");
          {% endfor %}
          {% endif %}
          break;

    {% endfor %}
  }

}
function addParameter(id, name) {

  $("#body_parameters").append("\
  <tr id=\"reaction_parameter_" + id.toString() + "_tr\">\
    <td class=\"col-xs-6\"><span id=\"reaction_parameter_" + id.toString() + "_name\">" + name + "</span></td>\
    <td class=\"col-xs-6\">\
      <input type=\"hidden\" id=\"reaction_parameter_" + id.toString() + "\" name=\"reaction_parameter_" + id.toString() + "\" value=\"\">\
      <div class=\"dropdown\">\
        <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
          <span id=\"reaction_parameter_" + id.toString() + "_label\">Choose a parameter</span>\
          <span class=\"caret\"></span>\
        </button>\
        <ul id=\"reaction_parameter_" + id.toString() + "_dropdown\" class=\"dropdown-menu\">\
            {% for t_parameter in list_of_parameters %}<li><a href=\"#\">{{ t_parameter }}</a></li>{% endfor %}\
        </ul>\
      </div>\
    </td>\
  </tr>\
  ");
  $("<script>").attr("type", "text/javascript").text("\
      $('#reaction_parameter_" + id.toString() + "_dropdown li').on('click', function(){\
        $('#reaction_parameter_" + id.toString() + "_label').html($(this).text());\
        $('#reaction_parameter_" + id.toString() + "').val($(this).index());});")
    .appendTo('#reaction_parameter_' + id.toString() + '_tr');
}
function removeParameters () {

  $("#body_parameters").children("tr").each(function() {
    $(this).remove();
  });

}
function removeParameter(id) {

  $("#reaction_parameter_" + id.toString()).remove();

}

function buildReactionDescription() {

  result_reactants = "";
  $("#body_reactants").children("tr").each(function(index)
  {


    if (!$("#reaction_reactant_" + index.toString() + "").val()) {

    } else {
      if (result_reactants != "") {
        result_reactants += " + "
      }
      result_reactants += $("#reaction_reactant_" + index.toString() + "_label").html()
    }

  });

  result_modifiers = "";
  $("#body_modifiers").children("tr").each(function(index)
  {


    if (!$("#reaction_modifier_" + index.toString() + "").val()) {
    } else {

      if (result_modifiers != "") {
        result_modifiers += " + "
      }
      result_modifiers += $("#reaction_modifier_" + index.toString() + "_label").html()
    }

  });

  result_products = ""
  $("#body_products").children("tr").each(function(index)
  {

    if (!$("#reaction_product_" + index.toString() + "").val()) {
    } else {

      if (result_products != "") {
        result_products += " + "
      }

      result_products += $("#reaction_product_" + index.toString() + "_label").html()
    }

  });

  result = result_reactants;
  if (result_modifiers != ""){
    if (result_reactants === ""){
      result += result_modifiers;
    } else {
      result += " + " + result_modifiers;
    }
  }

  if ($("#reaction_reversible").prop("checked") == true) {
    result += " <-> ";

  } else {
    result += " -> ";
  }

  if (result_modifiers != ""){
    if (result_products === ""){
      result += result_modifiers;
    } else {
      result += result_modifiers + " + ";
    }
  }
  result += result_products;

  $("#reaction_summary").html(result);

}

function clearForm()
{
  $("#edit_reaction_name").val("")
  $("#edit_reaction_id").val("")

  removeReactants();
  removeModifiers();
  removeProducts();
  buildReactionDescription();

  $("#new_reaction_type_label").html("{{reaction_types|my_lookup:0}}");
  $('#new_reaction_type').val(0);
  updateReversibleToggle(0);
  updateParameters(0, true);
  $("#input_parameters").addClass('in');
  $("#reaction_reversible").prop('checked', true);

  $("#reaction_notes").val("");
}

function newReaction() {
  clearForm();
  $('#modal_reaction').modal('show');

}

buildReactionDescription();

// {% if form.hasErrors == True or form.isEditing == True %}
//     $(window).on('load',function(){
//         $('#modal_reaction').modal('show');
//     });
// {% endif %}

$(window).on('load',function()
{
    {% for reaction in list_of_reactions %}
        load_reaction_kinetic_law({{forloop.counter0}});
    {% endfor %}
});


function load_reaction_kinetic_law(reaction_id)
{
    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_reaction_kinetic_law' %}", {'reaction_id': reaction_id.toString()},
        function(data) {
            $.each(data, function(index, element) {
             if (index === 'kinetic_law') { $("#kinetic_law_" + reaction_id.toString()).html(element.toString());  }
            });
        },
        function() {}
    );
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$("#kineticlaw_input").on('change paste keyup', function()
{
  $("#kineticlaw_invalid").removeClass("in");
  $("#kineticlaw_valid").removeClass("in");
  $("#kineticlaw_validating").addClass("in");
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
      url: '{% url 'math_validator' %}',
      data: {
          'math': $("#kineticlaw_input").val(),
      },

  })
  .done(function(data)
  {
     $.each(data, function(index, element) {
       if (index === 'valid' && element === 'true') {
         $("#kineticlaw_invalid").removeClass("in");
         $("#kineticlaw_validating").removeClass("in");
         $("#kineticlaw_valid").addClass("in");
       } else {
         $("#kineticlaw_validating").removeClass("in");
         $("#kineticlaw_valid").removeClass("in");
         $("#kineticlaw_invalid").addClass("in");
       }
     });
  })
  .fail(function()
  {
    $("#kineticlaw_validating").removeClass("in");
    $("#kineticlaw_valid").removeClass("in");
    $("#kineticlaw_invalid").addClass("in");
  })
});

var old_sbml_id = "{% if form.isEditing == True and form.sbmlId != None %}{{form.sbmlId}}{% endif %}";

$("#edit_reaction_id").on('change paste keyup', function()
{

  if (old_sbml_id === "" || $("#edit_reaction_id").val() !== old_sbml_id)
  {
    $("#sbmlid_invalid").removeClass("in");
    $("#sbmlid_valid").removeClass("in");
    $("#sbmlid_validating").addClass("in");
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
        url: '{% url 'sbml_id_validator' %}',
        data: {
            'sbml_id': $("#edit_reaction_id").val(),
        },

    })
    .done(function(data)
    {
       $.each(data, function(index, element) {
         if (index === 'valid' && element === 'true') {
           $("#sbmlid_invalid").removeClass("in");
           $("#sbmlid_validating").removeClass("in");
           $("#sbmlid_valid").addClass("in");
         } else {
           $("#sbmlid_validating").removeClass("in");
           $("#sbmlid_valid").removeClass("in");
           $("#sbmlid_invalid").addClass("in");
         }
       });
    })
    .fail(function()
    {
      $("#sbmlid_validating").removeClass("in");
      $("#sbmlid_valid").removeClass("in");
      $("#sbmlid_invalid").addClass("in");
    })
  }
});
