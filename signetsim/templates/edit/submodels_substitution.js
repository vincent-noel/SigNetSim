{% load tags %}

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
