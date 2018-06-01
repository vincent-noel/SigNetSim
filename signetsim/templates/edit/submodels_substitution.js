
class FormSubstitution extends FormGroup {

    constructor(field) {
        super();
        this.field = field;

        this.substitution_type = new Dropdown(
          "substitution_type", "The type of substitution",
          null,
          "0", "Replace a variable from a submodel with a variable from the main model (Replacement)",
          true
        );
        this.addForm(this.substitution_type);

        this.substitution_model_object = new Dropdown(
            "substitution_model_object", "The object from the model",
            null,
            "", "Select an object from the model",
            true
        )
        this.addForm(this.substitution_model_object, true);

        this.substitution_submodel = new Dropdown(
            "substitution_submodel", "The submodel",
            () => { this.loadSubmodelObjects(); },
            "", "Select a submodel",
            true
        )
        this.addForm(this.substitution_submodel, true);

        this.substitution_submodel_object = new Dropdown(
            "substitution_submodel_object", "The object of the submodel",
            null,
            "", "Select an object from the submodel",
            true
        )
        this.addForm(this.substitution_submodel_object, true);

        this.substitution_id = new ValueForm("substitution_id", "The id of the substitution", "");
        this.addForm(this.substitution_id);
    }

    loadSubmodelObjects()
    {
        this.substitution_submodel_object.showLoading();
        ajax_call(
            "POST",
            '{% url 'get_list_of_objects_from_submodels' %}',
            { 'model_id': this.substitution_submodel.getValue() },
            (data) =>
            {
                $.each(data, (index, element) =>
                {
                    if (index == 'list'){
                        this.substitution_submodel_object.showLoaded();
                        if (element.length > 0)
                        {
                            this.substitution_submodel_object.setList(element);
                        }
                    }
                });
            },
            () => { this.substitution_submodel_object.showLoadingFailed(); }
        );
    }

    show(){
        $('#' + this.field).modal('show');
    }

    new()
    {
        $("#modal_substitution-title").html("New modification");

//        this.resetErrors();
        this.clearForms();
        this.substitution_submodel_object.hide();
        this.show();
    }

    load(substitution_id)
    {
        $("#modal_substitution-title").html("Edit substitution");

        ajax_call(
            "POST",
            "{% url 'get_substitution' %}", {'id': substitution_id},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                   if (index === "id") {
                       this.substitution_id.setValue(element.toString());

                   } else if (index === "type") {
                       this.substitution_type.setValue(element);
                       if (element == 0){
                           this.substitution_type.setLabel(
                               "Replace a variable from a submodel with a variable from the main model (Replacement)"
                           );
                       } else {
                           this.substitution_type.setLabel(
                               "Replace a variable from the main model with a variable from a sbmodel (Replaced by)"
                           );
                       }

                   } else if (index === "object_id") {
                       this.substitution_model_object.setValue(element);

                   } else if (index === "object_name") {
                       this.substitution_model_object.setLabel(element.toString());

                   } else if (index === "submodel_id") {
                       this.substitution_submodel.setValue(element.toString());
                       this.loadSubmodelObjects();

                   } else if (index === "submodel_name") {
                       this.substitution_submodel.setLabel(element.toString());

                   } else if (index === "submodel_object_id") {
                      this.substitution_submodel_object.setValue(element.toString());

                   } else if (index === "submodel_object_name") {
                       this.substitution_submodel_object.setLabel(element.toString());

                   }

               });

            },
            () => { console.log("failed"); }
        );

        this.show();
    }

    save()
    {
//        this.resetErrors();
        this.checkErrors();

        if (this.nb_errors === 0){
            $("#modal_substitution").hide();
        }

        return (this.nb_errors === 0);
    }
}

let form_substitution = new FormSubstitution("modal_substitution");
