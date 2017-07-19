{% load tags %}

///////////////////////////////////////////////////////////////////////////////
// Substitutions
var loaded_submodel_object_id = "";
var loaded_submodel_object_name = "Select an object in the submodel";

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
      url: '{% url 'get_list_of_objects_from_submodels' %}',
      data: {
          'model_id': index,
      },

  })
  .done(function(data)
  {
     $.each(data, function(index, element) {
       if (index == 'list'){
          setSubstitutionListOfObjectsLoaded();
          if (element.length > 0)
           {
              loadSubstitutionSubmodelObjects(element);

           }
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
        list_objects += "<li><a>" + submodels_objects[i].toString() + "</a></li>";

    $("#substitution_list_of_objects_loaded").append("\
    <input type=\"hidden\" name=\"substitution_submodel_object\" id=\"substitution_submodel_object\" value=\"" + loaded_submodel_object_id + "\">\
    <div class=\"dropdown\">\
      <button type=\"button\" class=\"btn btn-primary btn-sm dropdown-toggle\" data-toggle=\"dropdown\">\
        <span id=\"substitution_submodel_object_label\">" + loaded_submodel_object_name + "</span>\
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

$('#new_substitution_button').on('click', function(){

    $("#modal_substitution-title").html("New modification");

    $("#modal_substitution_id").val("");
    $("#substitution_type").val(0);
    $("#substitution_type_label").html("Replace a variable from a submodel with a variable from the main model (Replacement)");
    $("#substitution_model_object").val("");
    $("#substitution_model_object_label").html("Select an object in the main model");
    $("#substitution_submodel").val("");
    $("#substitution_submodel_label").html("Select a submodel");
    $("#substitution_submodel_object").val("");
    $("#substitution_submodel_object_label").html("Select an object in the submodel");
    reset_errors();

    $('#modal_substitution').modal('show');
});



function view_substitution(submodel_id)
{

 $("#modal_substitution-title").html("Edit substitution");

    ajax_call(
        "POST", "{{csrf_token}}",
        "{% url 'get_substitution' %}", {'id': submodel_id},
        function(data)
        {
           $.each(data, function(index, element)
           {
               if (index === "id") { $("#modal_substitution_id").val(element.toString()); }
               else if (index === "type") {
                   $("#substitution_type").val(element);
                   if (element == 0){
                       $("#substitution_type_label").html("Replace a variable from a submodel with a variable from the main model (Replacement)")
                   } else {
                       $("#substitution_type_label").html("Replace a variable from the main model with a variable from a sbmodel (Replaced by)")
                   }
               }
               else if (index === "object_id") { $("#substitution_model_object").val(element.toString()); }
               else if (index === "object_name") { $("#substitution_model_object_label").html(element.toString()); }
               else if (index === "submodel_id") {
                   $("#substitution_submodel").val(element.toString());
                   get_substitution_list_of_objects(element);
               }
               else if (index === "submodel_name") { $("#substitution_submodel_label").html(element.toString()); }
               else if (index === "submodel_object_id") {
                  loaded_submodel_object_id = element.toString();
                  $("#substitution_submodel_object").val(element.toString());
               }
               else if (index === "submodel_object_name") {
                   loaded_submodel_object_name = element.toString();
                   $("#substitution_submodel_object_label").html(element.toString());
               }

           });

        },
        function() { console.log("failed"); }
    );

    $("#modal_substitution").modal('show');

}

function reset_errors()
{
   $("#error_modal").empty();
}

function save_substitution()
{
    var nb_errors = 0;
    reset_errors();

    if ($("#substitution_model_object").val() == "") {
        add_error_modal("invalid_object", "Please select an object from the main model");
        nb_errors++;
    }

    if ($("#substitution_submodel").val() == "") {
        add_error_modal("invalid_submodel", "Please select a submodel");
        nb_errors++;
    }

    if ($("#substitution_submodel_object").val() == "") {
        add_error_modal("invalid_submodel_object", "Please select an object from the submodel");
        nb_errors++;
    }

    if (nb_errors == 0) {
        $("#substitution_form").submit()
    }
}