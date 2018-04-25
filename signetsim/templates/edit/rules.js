{% comment %}

 Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.

{% endcomment %}

class RuleForm extends FormGroup{
    constructor(field){
        super();
        this.field = field;

        this.form_id = new ValueForm("rule_id", "The id of the rule", "");
        this.addForm(this.form_id);

        this.form_expression = new MathForm("rule_expression", "The expression of the rule", "");
        this.addForm(this.form_expression, true);

        this.form_expression_alg = new MathForm("rule_expression_alg", "The expression of the algebraic rule", "");
        this.addForm(this.form_expression_alg, true);

        this.form_variable = new Dropdown("variable_id", "The variable affected by the rule", null, "", "Choose a variable", true);
        this.addForm(this.form_variable);

        this.form_type = new Dropdown(
            "rule_type",
            "The type of rule",
            (() =>
            {
                this.form_variable.clear();
                this.form_expression.clear();
                this.form_expression_alg.clear()
                if (this.form_type.getValue() === 0) { this.show_alg(); }
                else { this.show_others(); }
            }),
            "", "Choose a rule type", true
        );
        this.addForm(this.form_type);

    }

    checkErrors(){
        this.resetErrors();

        if (this.form_type.hasError()){

            this.addError(this.form_type);
            this.form_type.highlight();
            this.nb_errors++;

        } else if (this.form_type.getValue() === 0){

            if (this.form_expression_alg.hasError()){
                this.addError(this.form_expression_alg);
                this.form_expression_alg.highlight();
                this.nb_errors++;
            }

        } else {

            if (this.form_variable.hasError()){
                this.addError(this.form_variable);
                this.form_variable.highlight();
                this.nb_errors++;
            }

            if (this.form_expression.hasError()){
                this.addError(this.form_expression);
                this.form_expression.highlight();
                this.nb_errors++;
            }
        }
    }

    show_alg()
    {
        $("#rule_species").removeClass("in");
        $("#rule_exp_others").removeClass("in");
        $("#rule_exp_alg").addClass("in");
    }

    show_others()
    {
        $("#rule_species").addClass("in");
        $("#rule_exp_others").addClass("in");
        $("#rule_exp_alg").removeClass("in");
    }

    show_none()
    {
        $("#rule_species").removeClass("in");
        $("#rule_exp_others").removeClass("in");
        $("#rule_exp_alg").removeClass("in");
    }

    show(){
        $('#' + this.field).modal('show');
    }

    new(){
        $("#modal_rule-title").html("New rule");

        form_rule.clearForms();
        form_rule.show_none();
        form_rule.show();
    }

    load(rule_ind)
    {
        $("#modal_rule-title").html("Edit rule");
        this.clearForms();

        ajax_call(
            "POST",
            "{% url 'get_rule' %}", {'rule_ind': rule_ind},
            (data) =>
            {
                $.each(data, (index, element) => {

                    if (index == "rule_id") {
                        this.form_id.setValue(element);

                    } else if (index === "rule_type") {

                      this.form_type.setValue(element);

                      if (element == 0) {
                        this.show_alg();
                      } else {
                        this.show_others();
                      }

                    } else if (index === "rule_type_label") {
                        this.form_type.setLabel(element.toString());

                    } else if (index === "variable_label") {
                        this.form_variable.setLabel(element.toString());

                    } else if (index === "variable") {
                        this.form_variable.setValue(element);

                    } else if (index === "expression"){

                      if (this.form_type.getValue() == 0) {
                        this.form_expression_alg.setValue(element);
                        this.form_expression_alg.check();
                      } else {
                        this.form_expression.setValue(element);
                        this.form_expression.check();
                      }
                    }
                });

            },
            () => { console.log("failed"); }
        );

        this.show();
    }

    save()
    {

        form_rule.checkErrors();

        if (form_rule.nb_errors === 0){
            $("#" + this.field).hide();
        }

        return (form_rule.nb_errors === 0);
    }
}

let form_rule = new RuleForm("modal_rule");

