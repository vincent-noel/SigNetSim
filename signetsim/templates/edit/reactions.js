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
{% include 'commons/js/sbmlid_form.js' %}
{% include 'commons/js/math_form.js' %}
{% include 'commons/js/list_form.js' %}

let form_group = new FormGroup();


let form_sbmlid = new SbmlIdForm("reaction_sbml_id", "The identifier of the reaction", default_value="");
form_group.addForm(form_sbmlid, error_checking=true);

let form_kinetic_law = new MathForm("reaction_kinetic_law", "The kinetic law of the reaction", default_value="");
form_group.addForm(form_kinetic_law, error_checking=true);


class ListOfSpeciesReference extends ListForm{

    add(species_stoichiometry="1", species_id="", species_name="Choose a species"){
        super.add(
            [
                $("<td>").attr('class', 'col-xs-3').append(
                    $("<input>").attr({
                        'type': 'text', 'class': 'form-control input-sm text-center',
                        'placeholder': 'Input stoichiometry',
                        'name': this.field + '_' + this.index + "_stoichiometry",
                        'value': species_stoichiometry
                    })
                ),
                $("<td>").attr('class', 'col-xs-7').append(
                    $("<input>").attr({
                        'type': 'hidden',
                        'id': this.field + '_' + this.index + '_value',
                        'name': this.field + '_' + this.index,
                        'value': species_id
                    }),
                    $("<div>").attr('class', 'dropdown').append(
                        $("<button>").attr({
                            'type': 'button', 'class': 'btn btn-primary btn-sm dropdown-toggle',
                            'data-toggle': 'dropdown'
                        }).append(
                            $("<span>").attr({
                                'id': this.field + '_' + this.index + '_label'
                            }).text(species_name),
                            $("<span>").attr('class', 'caret')
                        ),
                        $("<ul>").attr({
                            'class': 'dropdown-menu',
                            'id': this.field + '_' + this.index + '_list'
                        }).append(
                            {% for species in list_of_species %}
                            $("<li>").append($("<a>").attr("href", "#").text("{{ species }}")),
                            {% endfor %}
                        )
                    )
                )
            ],

        "var " + this.field + "_" + this.index + "_dropdown = new Dropdown('" + this.field + "_" + this.index + "', " + this.post_treatment + ", default_value='');"
        );
        this.update();
    }

    remove(element_id){
        super.remove(element_id);
        this.update();
    }

    update(){
        let m_id = 0;

        $("#body_" + this.field + "s").children("tr").each((tr_id, tr)=>
        {
            $('input', $(tr)).each((input_id, input) =>
            {
                let id = new RegExp('^' + this.field + '_[0-9]+$');
                if (id.test($(input).attr('name')))
                {
                    $(input).attr('name', this.field + '_' + m_id.toString());
                }

                let exp = new RegExp('^' + this.field + '_[0-9]+_stoichiometry');
                if (exp.test($(input).attr('name')))
                {
                    $(input).attr('name', this.field + '_' + m_id.toString() + '_stoichiometry');
                }
            });
            m_id = m_id + 1;
        })
        super.update();
    }

    getSpecies(){
        let result = "";
        $("#body_" + this.field + "s").children("tr").each((index) =>
        {
            if ($("#" + this.field + "_" + index.toString()).val() != "") {
                if (result != "") {
                    result += " + "
                }
            result += $("#" + this.field + "_" + index.toString() + "_label").html();
            }
        });
        return result;
    }
}


let form_list_reactants = new ListOfSpeciesReference("reaction_reactant", "The list of reactants", "form_list_reactants", post_treatment=()=>{buildReactionDescription();});
form_group(form_list_reactants);

let form_list_modifiers = new ListOfSpeciesReference("reaction_modifier", "The list of modifiers", "form_list_modifiers", post_treatment=()=>{buildReactionDescription();});
form_group(form_list_modifiers);

let form_list_products = new ListOfSpeciesReference("reaction_product", "The list of products", "form_list_products", post_treatment=()=>{buildReactionDescription();});
form_group(form_list_products);

var nb_local_parameters = -1;
var nb_parameters = {{ list_of_parameters|length }};
var local_parameters = [];
var selected_parameters = [];




function get_species_name(species_id)
{
    switch(species_id)
    {
        {% for species in list_of_species %}
        case {{forloop.counter0}}:
            return "{{species}}";
        {% endfor %}
    }
}

function get_parameter_name(parameter_id)
{
    switch(parameter_id)
    {
        {% for t_parameter in list_of_parameters %}
        case {{forloop.counter0}}:
            return "{{ t_parameter }}";
        {% endfor %}
    }
}


function buildReactionDescription() {

    result_reactants = form_list_reactants.getSpecies();
    result_modifiers = form_list_modifiers.getSpecies();
    result_products = form_list_products.getSpecies();

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

function select_reaction_type (type_id)
{
    updateReversibleToggle(type_id);
    updateParameters(type_id, ($('#reaction_reversible').prop('checked') == true));
    if (type_id == 2) {
        $("#input_parameters").removeClass("in");
        $("#input_kinetic_law").addClass("in");
    } else {
        $("#input_kinetic_law").removeClass("in");
        $("#input_parameters").addClass("in");
    }

}
function toggle_reversible()
{
    if ($('#reaction_reversible').prop('disabled') == false)
    {
        if ($('#reaction_reversible').prop('checked') == true) {
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
  updateParametersLists();

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
        </ul>\
      </div>\
    </td>\
  </tr>\
  ");
}

function addParametersScript(id) {
     $("<script>").attr("type", "text/javascript").attr("id", "reaction_parameter_" + id.toString() + "_script").text("\
      $('#reaction_parameter_" + id.toString() + "_dropdown li').on('click', function(){\
        selected_parameters[" + id.toString() + "] = $(this).index();\
        $('#reaction_parameter_" + id.toString() + "_label').html($(this).text());\
        $('#reaction_parameter_" + id.toString() + "').val($(this).index());\
      });")
    .appendTo('#reaction_parameter_' + id.toString() + '_tr');
}
function removeParameters () {

  $("#body_parameters").children("tr").each(function() {
    $(this).remove();
  });

}

function updateParametersLists()
{
  var p_id = 0;

  $("#body_parameters").children("tr").each(function()
  {
    $("#reaction_parameter_" + p_id.toString() + "_dropdown").empty();
    if (local_parameters.length > 0) {
        $.each(local_parameters, function (index, element) {
            $("#reaction_parameter_" + p_id.toString() + "_dropdown").append("<li><a>" + element[0] + "</a></li>")
        });
        $("#reaction_parameter_" + p_id.toString() + "_dropdown").append("<li role='separator' class='divider'></li>");

    }
    for (var counter = 0; counter < nb_parameters; counter++) { $("#reaction_parameter_" + p_id.toString() + "_dropdown").append("<li><a>" + get_parameter_name(counter) + "</a></li>")}
    addParametersScript(p_id);
    p_id = p_id + 1;
  });
}

function removeParameter(id) {

  $("#reaction_parameter_" + id.toString()).remove();

}

function changed_local_parameter_name(parameter_id)
{
  local_parameters[parameter_id][0] = $("#local_parameter_" + parameter_id.toString() + "_name").val();
  updateParametersLists();
}

function changed_local_parameter_value(parameter_id)
{
  local_parameters[parameter_id][1] = $("#local_parameter_" + parameter_id.toString() + "_value").val();
  updateParametersLists();
}

function add_local_parameter(name, value){
    nb_local_parameters = nb_local_parameters + 1;
    $("#table_local_parameters").append("\
    <tr class=\"row\" id=\"local_parameter_" + nb_local_parameters.toString() + "_tr\">\
        <td class=\"col-xs-6\">\
          <input type=\"text\" class=\"form-control input-sm\" placeholder=\"<Input parameter's name>\"\
                 id=\"local_parameter_" + nb_local_parameters.toString() + "_name\" name=\"local_parameter_" + nb_local_parameters.toString() + "_name\" value=\"" + name + "\"\
          ></td>\
        <td class=\"col-xs-4\">\
          <input type=\"text\" class=\"form-control input-sm\" placeholder=\"<Input parameter's value>\"\
                 id=\"local_parameter_" + nb_local_parameters.toString() + "_value\" name=\"local_parameter_" + nb_local_parameters.toString() + "_value\" value=\"" + value + "\"\
          ></td>\
        <td class=\"col-xs-2 text-right\">\
          <button type=\"button\" onclick=\"remove_local_parameter(" + nb_local_parameters.toString() + ");\" class=\"btn btn-danger btn-xs\">\
            <span class=\"glyphicon glyphicon-remove\"></span>\
          </button>\
        </td>\
      </tr>\
    ");
    $("<script>").attr("type", "text/javascript").text("\
       $('#local_parameter_" + nb_local_parameters.toString() + "_name').on('paste keyup', function() { changed_local_parameter_name(" + nb_local_parameters.toString() + ");});\
       $('#local_parameter_" + nb_local_parameters.toString() + "_value').on('paste keyup', function() { changed_local_parameter_value(" + nb_local_parameters.toString() + ");});\
    ")
    .appendTo('#local_parameter_' + nb_local_parameters.toString() + '_tr');
    local_parameters.push([name, value]);
    updateLocalParametersForm();
    updateParametersLists();
}

function remove_local_parameter(parameter_id)
{
    $("#local_parameter_" + parameter_id + "_tr").remove();
    updateLocalParametersForm();
    updateParametersLists();
}

function removeLocalParameters(parameter_id)
{
    $("#table_local_parameters").empty();
    nb_local_parameters = -1;
}
function updateLocalParametersForm()
{
    var m_id = 0;

    $("#table_local_parameters").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^local_parameter_[0-9]+_name$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'local_parameter_' + m_id.toString() + '_name');
            }

            var exp = new RegExp('^local_parameter_[0-9]+_expression$');
            if (exp.test($(this).attr('name')))
            {
                $(this).attr('name', 'local_parameter_' + m_id.toString() + '_value');
            }
        });
        m_id = m_id + 1;
    });
}


function view_reaction(sbml_id)
{
    $("#modal_reaction-title").html("Edit reaction");
    $("#loading_wait").addClass("in");
    $("#loading_done").removeClass("in");
    form_list_reactants.clear();
    form_list_modifiers.clear();
    form_list_products.clear();
    removeLocalParameters();
    ajax_call(
        "POST",
        "{% url 'get_reaction' %}", {'sbml_id': sbml_id},
        function(data)
        {
            $.each(data, function(index, element)
            {
                if (index === "id") {
                    $("#reaction_id").val(element.toString());

                } else if (index === "sbml_id") {
                    form_sbmlid.setValue(element.toString());
                    form_sbmlid.setInitialValue(element.toString());

                } else if (index === "name") {
                    $("#reaction_name").val(element.toString());

                } else if (index === "list_of_reactants") {
                    $.each(element, function(index, subelement) {
                        form_list_reactants.add(subelement[1], subelement[0], get_species_name(subelement[0]));
                    });

                }
                else if (index === "list_of_modifiers") {
                    $.each(element, function (index, subelement) {
                        form_list_modifiers.add(subelement[1], subelement[0], get_species_name(subelement[0]));

                    });
                }
                else if (index === "list_of_products") {
                    $.each(element, function(index, subelement) {
                        form_list_products.add(subelement[1], subelement[0], get_species_name(subelement[0]));
                    });
                }

                else if (index === "reaction_type") {
                    $("#new_reaction_type").val(element);
                    select_reaction_type(element);
                }
                else if (index === "reaction_type_name"){
                    $("#new_reaction_type_label").html(element);
                }
                else if (index === "reversible") {
                    if (element == 0) {
                        $('#reaction_reversible').prop('checked', false);
                        updateParameters(parseInt($("#new_reaction_type").val()), false);
                    } else {
                        $('#reaction_reversible').prop('checked', true);
                        updateParameters(parseInt($("#new_reaction_type").val()), true);
                    }

                }

                else if (index === "kinetic_law"){
                    form_kinetic_law.setValue(element);
                }
                else if (index == "list_of_local_parameters"){

                    local_parameters = [];
                    $.each(element, function(index, subelement) {
                        add_local_parameter(subelement[0], subelement[1]);
                    });
                }

                else if (index == "notes") {
                    $("#specie_notes").val(element.toString());

                }
                else if (index == "sboterm") {
                   $("#sboterm").val(element.toString());
                   $("#sboterm_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + element.toString());
                }
                else if (index == "sboterm_name") { $("#sboterm_name").html(element.toString()); }
            });

           $.each(data, function(index, element) {
               if (index === "list_of_parameters") {
                   $.each(element, function (index, subelement) {
                       selected_parameters.push(element);
                       $("#reaction_parameter_" + index.toString()).val(subelement);
                       $("#reaction_parameter_" + index.toString() + "_label").html(get_parameter_name(subelement));
                   });
                   updateParametersLists();

               }
           });
           buildReactionDescription();
            form_sbmlid.check();
           form_kinetic_law.check();
           $("#loading_wait").removeClass("in");
           $("#loading_done").addClass("in");
           $("#summary").tab('show');

           // reset_errors();
        },
        function() { console.log("failed"); }
    );

    modal_show();

}
function modal_show()
{
    $("#summary").tab('show');
    $("#modal_reaction").on('shown.bs.modal', () => { $("#reaction_name").focus(); });
    $('#modal_reaction').modal('show');

}

function newReaction()
{
    $("#edit_reaction_name").val("");
    $("#edit_reaction_id").val("");

    form_group.clearForms();
    buildReactionDescription();

    $("#new_reaction_type_label").html("{{reaction_types|my_lookup:0}}");
    $('#new_reaction_type').val(0);
    updateReversibleToggle(0);
    updateParameters(0, true);
    $("#input_parameters").addClass('in');
    $("#reaction_reversible").prop('checked', true);
    $("#reaction_notes").val("");
    modal_show();
}

$(window).on('load',function()
{
    {% for reaction in list_of_reactions %}
         load_reaction_kinetic_law({{forloop.counter0}});
    {% endfor %}
});


function load_reaction_kinetic_law(reaction_id)
{
    ajax_call(
        "POST",
        "{% url 'get_reaction_kinetic_law' %}", {'reaction_id': reaction_id.toString()},
        function(data) {
            $.each(data, function(index, element) {
             if (index === 'kinetic_law') { $("#kinetic_law_" + reaction_id.toString()).html(element.toString());  }
            });
        },
        function() {}
    );
}


function save_reaction()
{
    form_group.checkErrors();

    if (form_group.nb_errors == 0)
    {
        $("#modal_reaction").hide();
    }

    return (form_group.nb_errors == 0);
}

//
//function reset_errors()
//{
//   $("#error_modal").empty();
//   form_group.resetErrors();
//}
