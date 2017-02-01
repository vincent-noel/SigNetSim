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
    $(window).on('load',function(){
        $('#modal_submodel').modal('show');
    });
{% endif %}

{% if form_subs.hasErrors == True or form_subs.isEditing == True %}
    $(window).on('load',function(){
        $('#modal_modification').modal('show');
    });
{% endif %}

//////////////////////////////////////////////////////////////////////////////
// General tab, selection of type, id and name

$('#submodel_type_dropdown li').on('click', function(){

  if ($(this).index() == 0)
  {
    $("#tabs_external").removeClass("in");
    $("#tabs_internal").addClass("in");

  }
  else
  {
    $("#tabs_internal").removeClass("in");
    $("#tabs_external").addClass("in");
  }
  $("#submodel_type_label").html($(this).text());
  $('#submodel_type').val($(this).index());

});



// SbmlId Validation

var old_sbml_id = "{% if form.isEditing == True and form.sbmlId != None %}{{form.sbmlId}}{% endif %}";

function setSbmlIdValid()
{
  $("#sbmlid_invalid").removeClass("in");
  $("#sbmlid_validating").removeClass("in");
  $("#sbmlid_valid").addClass("in");
}

function setSbmlIdInvalid()
{
  $("#sbmlid_validating").removeClass("in");
  $("#sbmlid_valid").removeClass("in");
  $("#sbmlid_invalid").addClass("in");
}

function setSbmlIdValidating()
{
  $("#sbmlid_invalid").removeClass("in");
  $("#sbmlid_valid").removeClass("in");
  $("#sbmlid_validating").addClass("in");
}


$("#parameter_sbml_id").on('change paste keyup', function()
{
  new_sbml_id = $.trim($("#parameter_sbml_id").val());
  if (old_sbml_id === "" || new_sbml_id !== old_sbml_id)
  {
    setSbmlIdValidating();

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
            'sbml_id': new_sbml_id,
        },

    })
    .done(function(data)
    {
       $.each(data, function(index, element) {
         if (index === 'valid' && element === 'true') {
           setSbmlIdValid();
         } else {
           setSbmlIdInvalid();
         }
       });
    })
    .fail(function()
    {
      setSbmlIdInvalid();
    })
  }
  else if (new_sbml_id === old_sbml_id)
  {
    setSbmlIdValid();
  }
});


//////////////////////////////////////////////////////////////////////////////
// External model tab

function setSubmodelsRefsLoading()
{
  $("#submodel_refs_loaded").removeClass("in");
  $("#submodel_refs_loading_failed").removeClass("in");
  $("#submodel_refs_loading").addClass("in");

}

function setSubmodelsRefsLoaded()
{
  $("#submodel_refs_loading").removeClass("in");
  $("#submodel_refs_loading_failed").removeClass("in");
  $("#submodel_refs_loaded").addClass("in");
}

function setSubmodelsRefsLoadingFailed()
{
  $("#submodel_refs_loading").removeClass("in");
  $("#submodel_refs_loaded").removeClass("in");
  $("#submodel_refs_loading_failed").addClass("in");

}


function loadSubmodelRefs(submodels_refs)
{
    var list_models = "";
    var i;
    for (i=0; i < submodels_refs.length; i++)
    {
        if (i==0)
            list_models += "<li><a href=\"#\">" + submodels_refs[i].toString() + " (Main model)</a></li>";

        else
            list_models += "<li><a href=\"#\">" + submodels_refs[i].toString() + "</a></li>";
    }

    $("#submodel_refs_loaded").children().each(function() {
      $(this).remove();
    });

    $("#submodel_refs_loaded").append("\
    <input type=\"hidden\" name=\"submodel_submodel_ref\" id=\"submodel_submodel_ref\" value=\"0\">\
    <div class=\"dropdown\">\
      <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
        <span id=\"submodel_submodel_ref_label\">" + submodels_refs[0].toString() + " (Main model)</span>\
        <span class=\"caret\"></span>\
      </button>\
      <ul id=\"submodel_submodel_ref_dropdown\" class=\"dropdown-menu\">" + list_models.toString() + "</ul>\
    </div>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
        $(\"#submodel_submodel_ref_dropdown li\").on(\"click\", function(){\
          $(\"#submodel_submodel_ref_label\").html($(this).text());\
          $(\"#submodel_submodel_ref\").val($(this).index());});")
      .appendTo('#submodel_refs_loaded');
}




$('#submodel_source_dropdown li').on('click', function(){
  $("#submodel_source_label").html($(this).text());
  $('#submodel_source').val($(this).index());

  update_list_submodels();
  updateListOfObjects();

});


function update_list_submodels()
{

    setSubmodelsRefsLoading();
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
        url: '{% url 'get_submodels' %}',
        data: {
            'model_id': $('#submodel_source').val(),
        },

    })
    .done(function(data)
    {
       $.each(data, function(index, element) {
         if (index == 'list' && element.length > 0)
         {
            setSubmodelsRefsLoaded();
            loadSubmodelRefs(element);
         }
       });
    })
    .fail(function()
    {
      setSubmodelsRefsLoadingFailed();
    })

}


$('#submodel_submodel_ref_dropdown li').on('click', function(){
  $("#submodel_submodel_ref_label").html($(this).text());
  $('#submodel_submodel_ref').val($(this).index());
});


///////////////////////////////////////////////////////////////////////////////
// Time conversion factor
$('#time_conversion_factor_dropdown li').on('click', function(){
  if ($(this).index() == 0) {
    $("#time_conversion_factor_label").html("Select a time conversion factor");
    $('#time_conversion_factor').val("");
  } else {
    $("#time_conversion_factor_label").html($(this).text());
    $('#time_conversion_factor').val($(this).index()-2);
  }
});

///////////////////////////////////////////////////////////////////////////////
// Extent conversion factor
$('#extent_conversion_factor_dropdown li').on('click', function(){
  if ($(this).index() == 0) {
    $("#extent_conversion_factor_label").html("Select an extent conversion factor");
    $('#extent_conversion_factor').val("");
  } else {
    $("#extent_conversion_factor_label").html($(this).text());
    $('#extent_conversion_factor').val($(this).index()-2);
  }
});

// Deletions
var nb_deletions = {% if form.listOfDeletions != None %}{{form.listOfDeletions|my_len}}{% else %}0{% endif %};
var list_of_deletions = [{% if form.listOfDeletions != None %}{% for deletion in form.listOfDeletions %}{{deletion}}, {% endfor %}{% endif %}];
var list_of_objects_names = [{% for object in form.listOfObjects %}"{{object}}", {% endfor %}];

function addDeletion(index){

  if ($.inArray(index, list_of_deletions) == -1)
  {
    nb_deletions = nb_deletions + 1;
    list_of_deletions.push(index);
    var t_name = list_of_objects_names[index];

    $("#body_list_of_deletions").append("\
    <tr class=\"row\" id=\"deletion_" + nb_deletions.toString() + "\">\
      <input type=\"hidden\" name=\"deletion_id_" + nb_deletions.toString() + "_\" id=\"deletion_id_" + nb_deletions.toString() + "_\" value=\"" + index.toString() + "\">\
      <td class=\"col-xs-10\">" + t_name.toString() + "</td>\
      <td class=\"col-xs-2 text-right\">\
        <button type=\"button\" id=\"deletion_button_" + nb_deletions.toString() + "\" class=\"btn btn-danger btn-xs\"><span class=\"glyphicon glyphicon-remove\"></span></button>\
      </td>\
    </tr>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
        $(\"#deletion_button_" + nb_deletions.toString() + "\").on(\"click\", function(){\
          list_of_deletions.splice( $.inArray($(\"#deletion_id_" + nb_deletions.toString() + "_\").val(), list_of_deletions), 1 );\
          $(\"#deletion_" + nb_deletions.toString() + "\").remove();\
          updateDeletionsForm();});")
      .appendTo("#deletion_" + nb_deletions.toString());

    updateDeletionsForm();
  }
}
$('#objects_to_delete_dropdown li').on('click', function(){
  addDeletion($(this).index());
});


function updateDeletionsForm()
{
    var m_id = 0;

    $("#body_list_of_deletions").children("tr").each(function()
    {
        $('input', $(this)).each(function()
        {
            var id = new RegExp('^deletion_id_[0-9]+_$');
            if (id.test($(this).attr('name')))
            {
              $(this).attr('name', 'deletion_id_' + m_id.toString() + '_');
            }
        });
        m_id = m_id + 1;
    });
}


function setListOfObjectsLoading()
{
  $("#list_of_objects_loaded").removeClass("in");
  $("#list_of_objects_loading_failed").removeClass("in");
  $("#list_of_objects_loading").addClass("in");

}

function setListOfObjectsLoaded()
{
  $("#list_of_objects_loading").removeClass("in");
  $("#list_of_objects_loading_failed").removeClass("in");
  $("#list_of_objects_loaded").addClass("in");
}

function setListOfObjectsLoadingFailed()
{
  $("#list_of_objects_loading").removeClass("in");
  $("#list_of_objects_loaded").removeClass("in");
  $("#list_of_objects_loading_failed").addClass("in");

}

function updateListOfObjects()
{
  $("#list_of_objects_loaded").children().each(function() {
    $(this).remove();
  });
  nb_deletions = 0;
  $("#body_list_of_deletions").children().each(function() {
    $(this).remove();
  });

  setListOfObjectsLoading();

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
      url: '{% url 'get_list_of_objects' %}',
      data: {
          'model_id': $('#submodel_source').val(),
      },

  })
  .done(function(data)
  {
     $.each(data, function(index, element) {
       if (index == 'list' && element.length > 0)
       {
          setListOfObjectsLoaded();
          loadSubmodelObjects(element);

       }
     });
  })
  .fail(function()
  {
    setListOfObjectsLoadingFailed();
  })

}


function loadSubmodelObjects(submodels_objects)
{
    var list_objects = "";
    list_of_objects_names = submodels_objects;
    var i;
    for (i=0; i < submodels_objects.length; i++)
        list_objects += "<li><a href=\"#\">" + submodels_objects[i].toString() + "</a></li>";

    $("#list_of_objects_loaded").append("\
    <div class=\"dropdown\">\
      <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
        <span>Select an object to delete in the submodel</span>\
        <span class=\"caret\"></span>\
      </button>\
      <ul id=\"objects_to_delete_dropdown\" class=\"dropdown-menu\">" + list_objects.toString() + "</ul>\
    </div>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
      $('#objects_to_delete_dropdown li').on('click', function(){\
      addDeletion($(this).index());});")
    .appendTo('#list_of_objects_loaded');
}


///////////////////////////////////////////////////////////////////////////////
// New submodel
$('#new_submodels_button').on('click', function(){

    $("#modal_title").html("New submodel");

    $("#submodel_name").attr("value", "");
    $("#submodel_sbml_id").attr("value", "");

    $("#submodel_type").attr("value", 0);
    $("#submodel_type_label").html("Internal model definition");

    $("#submodel_source").attr("value", "");
    $("#submodel_source_label").attr("value", "Select a model within your project");

    $("#submodel_submodel_ref").attr("value", "");
    $("#submodel_submodel_ref_label").attr("value", "Choose a submodel");
    // $("#table_submodel_ref").removeClass("in");

    $('#submodel_type').val($(this).index());
    $("#source").removeClass('active in');
    $("#general").addClass('active in');
    $("#tabs_external").removeClass("in");
    $("#tabs_internal").addClass("in");

    $('#modal_submodel').modal('show');

    nb_deletions = 0;
    $("#body_list_of_deletions").children().each(function() {
      $(this).remove();
    });

    old_sbml_id = ""
});

///////////////////////////////////////////////////////////////////////////////
// Substitutions


$('#substitution_type_dropdown li').on('click', function(){
  $("#substitution_type_label").html($(this).text());
  $('#substitution_type').val($(this).index());
});

$('#substitution_submodel_dropdown li').on('click', function(){
  $("#substitution_submodel_label").html($(this).text());
  $('#substitution_submodel').val($(this).index());
  get_substitution_list_of_objects($(this).index());
});


function setSubstitutionListOfObjectsLoading()
{
  $("#substitution_list_of_objects_loaded").removeClass("in");
  $("#substitution_list_of_objects_loading_failed").removeClass("in");
  $("#substitution_list_of_objects_loading").addClass("in");

}

function setSubstitutionListOfObjectsLoaded()
{
  $("#substitution_list_of_objects_loading").removeClass("in");
  $("#substitution_list_of_objects_loading_failed").removeClass("in");
  $("#substitution_list_of_objects_loaded").addClass("in");
}

function setSubstitutionListOfObjectsLoadingFailed()
{
  $("#substitution_list_of_objects_loading").removeClass("in");
  $("#substitution_list_of_objects_loaded").removeClass("in");
  $("#substitution_list_of_objects_loading_failed").addClass("in");

}

function get_substitution_list_of_objects(index)
{
  $("#substitution_list_of_objects_loaded").children().each(function() {
    $(this).remove();
  });

  setSubstitutionListOfObjectsLoading();

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
      url: '{% url 'get_list_of_objects' %}',
      data: {
          'model_id': index,
      },

  })
  .done(function(data)
  {
     $.each(data, function(index, element) {
       if (index == 'list' && element.length > 0)
       {
          setSubstitutionListOfObjectsLoaded();
          loadSubstitutionSubmodelObjects(element);

       }
     });
  })
  .fail(function()
  {
    setSubstitutionListOfObjectsLoadingFailed();
  })

}

function loadSubstitutionSubmodelObjects(submodels_objects)
{
    var list_objects = "";
    list_of_objects_names = submodels_objects;
    var i;
    for (i=0; i < submodels_objects.length; i++)
        list_objects += "<li><a href=\"#\">" + submodels_objects[i].toString() + "</a></li>";

    $("#substitution_list_of_objects_loaded").append("\
    <input type=\"hidden\" name=\"substitution_submodel_object\" id=\"substitution_submodel_object\" value=\"\">\
    <div class=\"dropdown\">\
      <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
        <span id=\"substitution_submodel_object_label\">Select an object in the submodel</span>\
        <span class=\"caret\"></span>\
      </button>\
      <ul id=\"substitution_submodel_object_dropdown\" class=\"dropdown-menu\">" + list_objects.toString() + "</ul>\
    </div>\
    ");

    $("<script>").attr("type", "text/javascript").text("\
      $(\"#substitution_submodel_object_dropdown li\").on(\"click\", function(){\
        $(\"#substitution_submodel_object_label\").html($(this).text());\
        $(\"#substitution_submodel_object\").val($(this).index());\
      });")
    .appendTo('#substitution_list_of_objects_loaded');
}

$('#substitution_model_object_dropdown li').on('click', function(){
  $("#substitution_model_object_label").html($(this).text());
  $('#substitution_model_object').val($(this).index());
});

$('#new_modification_button').on('click', function(){

    $("#modal_modification_title").html("New modification");
    $('#modal_modification').modal('show');

});
