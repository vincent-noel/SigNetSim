{% load tags %}

//////////////////////////////////////////////////////////////////////////////
// General tab, selection of type, id and name

class ListOfDeletedObjects extends ListForm{

    constructor(field, description, parent_form_name, form_name, post_treatment=null) {
        super(field, description, parent_form_name, form_name, post_treatment, true);
    }

    add(object_id="", object_name="Object"){
        super.add(
            [
                $("<td>").attr('class', 'col-xs-10').append(
                    $("<input>").attr({
                        'type': 'hidden',
                        'name': this.field + '_id_' + this.index + "_",
                        'value': object_id
                    })
                ).text(object_name),
            ],

        ""
        );
        this.update();
    }

    remove(element_id){
        super.remove(element_id);
        this.update();
    }

    update(){

        $("#body_" + this.field + "s").children("tr").each((tr_id, tr)=>
        {
            $('input', $(tr)).each((input_id, input) =>
            {
                let id = new RegExp('^' + this.field + '_[0-9]+$');
                if (id.test($(input).attr('name')))
                {
                    $(input).attr('name', this.field + '_' + input_id.toString());
                }

                let exp = new RegExp('^' + this.field + '_[0-9]+_stoichiometry');
                if (exp.test($(input).attr('name')))
                {
                    $(input).attr('name', this.field + '_' + input_id.toString() + '_stoichiometry');
                }
            });
        })
        super.update();
    }


}


class SubmodelForm extends FormGroup {

    constructor(field) {
        super();
        this.field = field;

        this.submodel_type = new Dropdown(
            "submodel_type", "The type of submodel",
            () => { this.updateSubmodelType(); },
            0, "Internal model definition",
            true
        );
        this.addForm(this.submodel_type);

        this.submodel_name = new ValueForm("submodel_name", "The name of the submodel", "");
        this.addForm(this.submodel_name);

        this.submodel_sbmlid = new SbmlIdForm("submodel_sbml_id", "The identifier of the submodel", "");
        this.addForm(this.submodel_sbmlid, true);

        this.time_conversion = new NoneDropdown(
            "time_conversion_factor", "The time conversion factor of the submodel",
            null,
            "", "Select a time conversion factor"
        );
        this.addForm(this.time_conversion);

        this.extent_conversion = new NoneDropdown(
            "extent_conversion_factor", "The extent conversion factor of the submodel",
            null,
            "", "Select an extent conversion factor"
        );
        this.addForm(this.time_conversion);

        this.submodel_source = new Dropdown(
            "submodel_source", "The source of the external submodel",
            () => { this.loadSubmodels(); },
            "", "Select a model within your project"
        );
        this.addForm(this.submodel_source);

        this.submodel_ref = new Dropdown(
            "submodel_submodel", "The submodel reference from the choosen model",
            () => { this.loadListOfObjects(); },
            "", "Select a submodel within the model"
        );
        this.addForm(this.submodel_ref);

        this.submodel_list_of_objects = new Dropdown(
            "submodel_list_of_objects", "The list of objects of the submodel",
            () => {
                this.addDeletedObject();
            },
            "", "Select an object to delete"
        );
        this.addForm(this.submodel_list_of_objects);

         this.list_deletions = new ListOfDeletedObjects(
            "deletion",
            "The list of objects to be deleted",
            "form_submodel", "list_deletions", null
        );
        this.addForm(this.list_deletions);
    }

    updateSubmodelType()
    {
        if (this.submodel_type.getValue() == 0) {
            $("#tabs_external").removeClass("in");
            $("#tabs_internal").addClass("in");
            $("#source").removeClass('active in');

        } else {
            $("#tabs_internal").removeClass("in");
            $("#tabs_external").addClass("in");
            $("#source").addClass('in');
        }
    }

    loadSubmodels()
    {

        this.submodel_ref.showLoading();
        ajax_call(
            "POST",
            "{% url 'get_submodels' %}", {'model_id': this.submodel_source.getValue()},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                 if (index == 'list' && element.length > 0)
                 {
                    this.submodel_ref.showLoaded();
                    this.submodel_ref.setList(element);
                 }
               });
            },
            () => {
                this.submodel_ref.showLoadingFailed();
            }
        );
    }

    loadListOfObjects(){
        this.submodel_list_of_objects.showLoading();
        ajax_call(
            "POST",
            "{% url 'get_list_of_objects' %}",
            {'model_id': this.submodel_source.getValue(), 'submodel_id': this.submodel_ref.getValue()},
            (data) =>
            {
                $.each(data, (index, element) => {
                    if (index == 'list' && element.length > 0)
                    {
                        this.submodel_list_of_objects.showLoaded();
                        this.submodel_list_of_objects.setList(element);

                    }
                });
            },
            () =>
            {
                this.submodel_list_of_objects.showLoadingFailed();
            }

        );
    }

    addDeletedObject(){

        this.list_deletions.add(this.submodel_list_of_objects.getValue(), this.submodel_list_of_objects.getLabel());
    }

    show(){
        $("#" + this.field).on('shown.bs.modal', () => { $("#submodel_name").focus(); });
        $("#" + this.field).modal('show');
        $('.nav-tabs a[href="#general"]').tab('show');
    }

    new()
    {
        $("#modal_title").html("New submodel");


        this.clearForms();

        $("#submodel_submodel_ref").val("");
        $("#submodel_submodel_ref_label").html("Choose a submodel");

        $("#general").addClass('active in');
        this.updateSubmodelType();
//        this.resetErrors();

        this.show();
        this.nb_deletions = 0;
        $("#body_list_of_deletions").children().each(function() {
          $(this).remove();
        });
    }

    load(submodel_id)
    {

        $("#modal_submodel-title").html("Edit submodel");

        let model_loaded = 0;
        ajax_call(
            "POST",
            "{% url 'get_submodel' %}", {'id': submodel_id},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                   if (index === "id") {
                       $("#modal_submodel_id").val(element.toString());

                   } else if (index === "name") {
                       this.submodel_name.setValue(element);

                   } else if (index === "sbml_id") {
                       this.submodel_sbmlid.setValue(element);

                   } else if (index === "type") {

                        this.submodel_type.setValue(element);

                        if (element === 0) {
                            this.submodel_type.setLabel("Internal model definition");
                        } else {
                            this.submodel_type.setLabel("External model definition");
                        }

                        this.updateSubmodelType();

                   } else if (index === "source") {
                       this.submodel_source.setValue(element);
                       this.loadSubmodels();
                        model_loaded++;

                   } else if (index === "source_name") {
                       this.submodel_source.setLabel(element);

                   } else if (index === "source_submodel_ref") {
                       this.submodel_ref.setValue(element);
                       model_loaded++;

                   } else if (index === "source_submodel_ref_name") {
                       this.submodel_ref.setLabel(element);

                   } else if (index === "time_conversion_factor") {
                       this.time_conversion.setValue(element);

                   } else if (index === "time_conversion_factor_name") {

                       if (element !== ""){
                           this.time_conversion.setLabel(element);

                       } else {
                           this.time_conversion.setLabel("Select a time conversion factor");

                       }

                   } else if (index === "extent_conversion_factor") {
                       this.extent_conversion.setValue(element);

                   } else if (index === "extent_conversion_factor_name") {

                       if (element !== ""){
                           this.extent_conversion.setLabel(element);

                       } else {
                           this.extent_conversion.setLabel("Select an extent conversion factor");

                       }
                   }
                   if (model_loaded == 2) { model_loaded = 0; this.loadListOfObjects(); }
               });
               this.submodel_sbmlid.check();
//               this.resetErrors();
            },
            () => { console.log("failed"); }
        )

        this.show();
    }

    checkErrors()
    {
        super.checkErrors();

        if (this.submodel_type.getValue() === 1){

            this.submodel_source.check();

            if (this.submodel_source.hasError())
            {
                this.addError(this.submodel_source);
                this.submodel_source.highlight();
                this.nb_errors++;
            }
        }

    }

    save()
    {
//        this.resetErrors();
        this.checkErrors();

        if (this.nb_errors == 0) {
            $("#modal_submodel").hide();
        }

        return (this.nb_errors == 0);
    }
}


let form_submodel = new SubmodelForm("modal_submodel");

