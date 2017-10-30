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

{% load static from staticfiles %}

class SbmlIdForm extends HasIndicator(Form)
{
    constructor(field, description, has_scope=false, scope_field="", default_value="")
    {
        super(field, description, default_value);
        this.initial_value = "";

        // For local parameters, we need to have an extra information : the scope (global, or local to a reaction)
        this.hasScope = has_scope;
        this.scope_field = scope_field
        this.initial_scope = 0;
        $("#" + this.field).on('paste keyup', () => { this.check(); });

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
                "POST", "{% url 'sbml_id_validator' %}",
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
                            this.setIndicatorInValid();
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

    clear()
    {
        super.clear();
        super.unhighlight();
        super.setIndicatorEmpty();
        this.initial_scope = 0;
    }

}