/**
 * Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
 *
 * This file is part of SigNetSim.
 *
 * libSigNetSim is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SigNetSim is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SigNetSim.  If not, see <http://www.gnu.org/licenses/>.
 */

/* This file contains all the class for the javascript methods of the forms used in signetsim
 * In an effort to organize things a little, we will first declare the base class, then the mixins,
 * then the inherited classes. And we'll make a list in this header

 * Base class : Form.
 *
 *
 * Mixin :
 * - HasIndicator
 *
 *
 * Derivated classes :
 * - FloatForm :        Form for floats, usign ajax verification
 * - SbmlIdForm :       Form for sbml ids, using ajax verification
 * - MathForm :         Form for math formulas, using ajax verification
 * - SliderForm :       Form for checkbox
 * - Dropdown :         Form for dropdown menus
 * - EditableInput :    Form for editable input, with post_treatment
 * - SBOTermInput :     Form for SBO term, printing the description of the term
 * - ListForm :         Form group, with the possibility to add and remove items
 * - FormGroup :        Form group, base class for the sbml elements forms
 */

class Form
{
    constructor(field, description, default_value="", on_input=null){

        this.field = field;
        this.description = description;
        this.default_value = default_value;
        this.error_message = "";

        if (on_input !== null) { $('#' + this.field).on('paste keyup', () => { on_input(); }); }
    }

    clearValue() {
        $("#" + this.field).val(this.default_value);
    }

    getValue() {
        return $.trim($("#" + this.field).val());
    }

    setValue(value) {
        $("#" + this.field).val(value);
    }

    setError(error_message){
        this.error_message = error_message;
    }

    clearError(){
        this.error_message = "";
        this.unhighlight();
    }

    hasError(){
        return this.error_message !== "";
    }

    highlight(){
        $("#" + this.field + "_label").addClass("text-danger");
        $("#" + this.field + "_group").addClass("has-error");
    }
    unhighlight(){
        $("#" + this.field + "_label").removeClass("text-danger");
        $("#" + this.field + "_group").removeClass("has-error");
    }

    clear(){
        this.clearValue();
        this.clearError();
    }

}

let HasIndicator = (superclass) => class extends superclass {
    setIndicatorValid(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_valid").addClass("in");
    }
    setIndicatorInvalid(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_valid").removeClass("in");
        $("#" + this.field + "_invalid").addClass("in");
    }
    setIndicatorValidating(){
        $("#" + this.field + "_valid").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_validating").addClass("in");
    }
    setIndicatorEmpty(){
        $("#" + this.field + "_validating").removeClass("in");
        $("#" + this.field + "_invalid").removeClass("in");
        $("#" + this.field + "_valid").removeClass("in");
    }
}

class FloatForm extends Form
{
    constructor(field, description, required, default_value=1)
    {
        super(field, description, default_value, () => { this.check(); });
        this.required = required;
    }

    check() {
        ajax_call(
            "POST", getFloatValidatorURL(),
            {'value' : this.getValue(), 'required': this.required},
            (data) => {
                $.each(data, (index, element) => {
                    if (index == "error"){ this.setError(element.toString()); }
                    else { this.setError("couldn't be validated : unknown response"); }
                });
            },
            () => { this.setError("couldn't be validated : unable to connect"); }
        );
    }

    clear() {
        super.clearError();
    }
}


class SbmlIdForm extends HasIndicator(Form)
{
    constructor(field, description, default_value="", has_scope=false, scope_field="")
    {
        super(field, description, default_value, () => { this.check(); });
        this.initial_value = "";

        // For local parameters, we need to have an extra information : the scope (global, or local to a reaction)
        this.hasScope = has_scope;
        this.scope_field = scope_field
        this.initial_scope = 0;

    }

    setInitialValue(value){
        this.initial_value = value;
    }

    setInitialScope(scope) {
        this.initial_scope = scope;
    }

    getScope() {
        return parseInt($("#" + this.scope_field).val());
    }

    check()
    {
        let sbml_id = this.getValue();
        let scope;
        if (this.hasScope){ scope = this.getScope(); }

        if (sbml_id !== "")
        {
            // We actually only need to check
            if (
                // If there is no scope, but the value has been changed
                (!this.hasScope && this.initial_value !== sbml_id)

                // Or if there is a scope, and either the value or the scope has been changed
                || (this.hasScope && (this.initial_value !== sbml_id || this.initial_scope !== scope))
            ){

                this.setIndicatorValidating();
                let post_data;
                if (!this.hasScope){
                    post_data = {'sbml_id': sbml_id };}
                else{
                    post_data = {'sbml_id': sbml_id, 'reaction_id': scope};}

                ajax_call(
                    "POST", getSbmlIdValidatorURL(),
                    post_data,
                    (data) => {
                        $.each(data, (index, element) => {
                            if (index === 'error')
                            {
                                this.setError(element.toString());
                                if (element == "") {
                                    this.setIndicatorValid();
                                } else {
                                    this.setIndicatorInvalid();
                                }
                            }
                            else
                            {
                                this.setError("Unkown error while checking the identifier");
                                this.setIndicatorInvalid();
                            }
                        });
                    },
                    () => {
                        this.setError("Connection failed while checking the identifier");
                        this.setIndicatorInvalid();
                    }
                );
            }
            // Otherwise no need to check, it's valid
            else { this.setIndicatorValid(); super.clearError(); }
        }
        else
        {
            this.setError("Please input an identifier");
            this.setIndicatorInvalid();
        }

    }

    clear()
    {
        super.clear();
        super.unhighlight();
        super.setIndicatorEmpty();
        this.initial_scope = 0;
    }

}

class MathForm extends HasIndicator(Form)
{
    constructor(field, description, default_value="")
    {
        super(field, description, default_value);
        $("#" + this.field).on('paste keyup', () => { this.check(); });

    }

    check()
    {
        this.setIndicatorValidating();

        ajax_call(
            "POST", getMathValidatorURL(),
            {'math' : this.getValue()},
            (data) => {
                $.each(data, (index, element) => {
                    if (index === "valid" && element === "true"){
                        this.clearError();
                        this.setIndicatorValid();

                    } else {
                        this.setError("is invalid");
                        this.setIndicatorInvalid();
                    }
                });
            },
            () => {
                this.setError("couldn't be validated : unable to connect");
                this.setIndicatorInvalid();
            }
        );
    }

    clear() {
        super.clear();
    }
}

class SliderForm extends Form
{
    constructor(field, description, default_value=1, post_treatment=null)
    {
        super(field, description, default_value);
        this.disabled = false;
        this.post_treatment = post_treatment;
    }

    getValue()
    {
        return $('#' + this.field).prop('checked');
    }

    switch_on()
    {
        if (!this.disabled) {
            $('#' + this.field).prop('checked', true);
            if (this.post_treatment !== null){
                this.post_treatment();
            }
        }
    }

    switch_off()
    {
        if (!this.disabled){
            $('#' + this.field).prop('checked', false);
            if (this.post_treatment !== null){
                this.post_treatment();
            }
        }
    }

    disable()
    {
        this.disabled = true;
    }

    enable()
    {
        this.disabled = false;
    }

    toggle()
    {
        if (this.getValue()) {
            this.switch_off();
        } else {
            this.switch_on();
        }
    }

    clear()
    {
        super.clear();

        if (this.default_value === 1) {
            this.switch_on();
        } else {
            this.switch_off();
        }
    }
}

class Dropdown extends Form {
    constructor(field, description="", post_treatment=null, default_value="", default_label="Choose an item", required=false) {

        super(field, description, default_value);

        this.default_label = default_label;
        this.required = required;
        this.post_treatment = post_treatment;
        $("#" + this.field + "_list li").on('click', (element) =>
        {
            this.clearError();
            this.setLabel($(element.currentTarget).text());
            this.setValue($(element.currentTarget).index());

            if (post_treatment !== null) {
                post_treatment();
            }
            if (this.required){
                this.check();
            }
        });
    }
    setLabel(label){
        $("#" + this.field + "_label").html(label);
    }

    setValue(value){
        $("#" + this.field + "_value").val(value);
    }

    getLabel(){
        return $("#" + this.field + "_label").html();
    }

    getValue(){
        return parseInt($("#" + this.field + "_value").val());
    }

    clear(){
        this.setLabel(this.default_label);
        this.setValue(this.default_value);
    }

    check(){
        if (this.required && Number.isNaN(this.getValue())){
            this.setError("isn't selected");
        }
    }

    setList(list) {
        let ul_element = $("#" + this.field + "_list");
        ul_element.empty();

        for (var value of list) {
            ul_element.append($("<li>").append($("<a>").attr('href', '#').text(value)));
        }
        $("#" + this.field + "_list li").on('click', (element) =>
        {
            this.clearError();
            this.setLabel($(element.currentTarget).text());
            this.setValue($(element.currentTarget).index());

            if (this.post_treatment !== null) {
                this.post_treatment();
            }
            if (this.required){
                this.check();
            }
        });
    }

    hide()
    {
        $("#" + this.field + "_loaded").removeClass("in");
        $("#" + this.field + "_loading_failed").removeClass("in");
        $("#" + this.field + "_loading").removeClass("in");
    }

    showLoading()
    {
        $("#" + this.field + "_loaded").removeClass("in");
        $("#" + this.field + "_loading_failed").removeClass("in");
        $("#" + this.field + "_loading").addClass("in");
    }

    showLoaded()
    {
        $("#" + this.field + "_loading").removeClass("in");
        $("#" + this.field + "_loading_failed").removeClass("in");
        $("#" + this.field + "_loaded").addClass("in");
    }

    showLoadingFailed(){
        $("#" + this.field + "_loading").removeClass("in");
        $("#" + this.field + "_loaded").removeClass("in");
        $("#" + this.field + "_loading_failed").addClass("in");
    }
}


class NoneDropdown extends Dropdown {
    constructor(field, description="", post_treatment=null, default_value="", default_label="Choose an item", required=false) {

        super(field, description, post_treatment, default_value, default_label, required);
        $("#" + this.field + "_list li").on('click', (element) =>
        {
            this.clearError();
            this.setLabel($(element.currentTarget).text());
            this.setValue($(element.currentTarget).index()-2);

            if (post_treatment !== null) {
                post_treatment();
            }
            if (this.required){
                this.check();
            }
        });
    }
}


class EditableInput extends Form
{
    constructor(field) {
        super(field);
        this.field = field;

        $("#" + this.field + "_edit").on('click', () => { this.edit_on(); });
        $("#" + this.field + "_edit_cancel").on('click', () => { this.edit_off(); });
    }

    edit_on() {
        $("#" + this.field + "_edit_on").addClass("in");
        $("#" + this.field + "_edit_off").removeClass("in");
        $("#" + this.field + "_edit_off_actions").addClass("in");
        $("#" + this.field + "_edit_on_actions").removeClass("in");
    }

    edit_off() {
        $("#" + this.field + "_edit_off").addClass("in");
        $("#" + this.field + "_edit_on").removeClass("in");
        $("#" + this.field + "_edit_on_actions").addClass("in");
        $("#" + this.field + "_edit_off_actions").removeClass("in");
    }

    validate() {
        ;
    }
}

class SBOTermInput extends EditableInput
{
    constructor(field)
    {
        super(field);
    }

    setValue(value) {
        $("#" + this.field).val(value);
    }

    setName(name){
        $("#" + this.field + "_name").html(name);
    }

    setLink(link){
        if (link !== ""){
           $("#" + this.field + "_link").attr("href", "http://www.ebi.ac.uk/sbo/main/display?nodeId=" + link);
        } else {
            $("#" + this.field + "_link").removeAttr("href");
        }
    }

    resolve()
    {
        ajax_call(
            "POST", getSBOTermURL(),
            {'sboterm': this.getValue()},
            (data) =>
            {
               $.each(data, (index, element) =>
               {
                    if (index === "name")
                    {
                        this.setName(element.toString());
                        this.setLink(this.getValue());
                    }

                });
                super.edit_off();
            },
            () => { console.log("resolve sbo failed"); }

        );
    }
}


class ListForm {
    constructor(field, description, form_name, post_treatment=null, removable=true) {
        this.field = field;
        this.description = description;
        this.form_name = form_name;
        this.index = 0;
        this.post_treatment = post_treatment;
        this.removable = removable;
    }

    add(content="", script="")
    {
        if (this.removable) {

            $("#body_" + this.field + "s")
            .append($("<tr>").attr({'class': 'row', 'id': this.field + "_" + this.index.toString() + "_tr"})
                .append(
                    content,
                    $("<td>").attr({'class': 'col-xs-2 text-right'})
                    .append(
                        $("<button>").attr({
                            'type': 'button',
                            'onclick': this.form_name + ".remove(" + this.index + ")",
                            'class': 'btn btn-danger btn-xs'
                        })
                        .append(
                            $("<span>").attr({
                                'class': 'glyphicon glyphicon-remove'
                            })
                        )
                    ),
                    $("<script>").attr('type', 'application/javascript')
                    .text(script)
                )
            );

        } else {
             $("#body_" + this.field + "s")
            .append(
                $("<tr>").attr({'class': 'row', 'id': this.field + "_" + this.index.toString() + "_tr"})
                .append(
                    content,
                    $("<script>").attr('type', 'application/javascript')
                    .text(script)
                )
            );
        }

        this.index++;
    }

    remove(element_id)
    {
        $("#" + this.field + "_" + element_id + "_tr").remove();
    }

    update()
    {
        if (this.post_treatment !== null) {
            this.post_treatment();
        }
    }

    clear()
    {
        $("#body_" + this.field + "s").children("tr").each((index, element) => {$(element).remove();});
        this.index = 0;
    }
}


class FormGroup {
    constructor()
    {
        this.list = [];
        this.listErrorChecking = [];
        this.nbErrors = 0;
    }

    addForm(form, error_checking=false) {
        this.list.push(form);
        this.listErrorChecking.push(error_checking);
    }

    addError(form)
    {
        if ($("#error_modal").children().length === 0)
        {
            $("#error_modal").append(
                "<div class=\"alert alert-danger fade in\" id=\"error_modal_list\">\
                    <a href=\"#\" class=\"close\" data-dismiss=\"alert\" aria-label=\"close\">&times;</a>\
                </div>"
            );
        }

        if ($("#error_modal_list").find("#error_message_" + form.field).length === 0)
        {
            $("#error_modal_list").append(
                "<span id=\"error_message_" + form.field + "\">\
                    <strong>Error : </strong>" + form.description + " " + form.error_message + "\
                </span><br/>"
            );
        }
    }

    resetErrors()
    {
        for (var [index, form] of this.list.entries()) {
            if (this.listErrorChecking[index]) {
                form.unhighlight();
            }
        }

        $("#error_modal").empty();
        this.nb_errors = 0;
    }

    checkErrors() {

        this.resetErrors();

        for (var [index, form] of this.list.entries())
        {
            if (this.listErrorChecking[index]){
                form.check();
                if (form.hasError()){
                    this.addError(form);
                    form.highlight();
                    this.nb_errors++;
                }
            }
        }

    }

    clearForms() {

        this.resetErrors();

        for (var form of this.list) {
            form.clear();
        }
    }
}
