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

class MathForm extends HasIndicator(Form)
{
    constructor(field, description, required, default_value="")
    {
        super(field, description, default_value);
        this.required = required;
        $("#" + this.field).on('paste keyup', () => { this.check(); });

    }

    check()
    {
        this.setIndicatorValidating();

        ajax_call(
            "POST", "{% url 'math_validator' %}",
            {'math' : $.trim($("#" + this.field).val())},
            (data) => {
                $.each(data, (index, element) => {
                    if (index === "valid" && element === "true"){
//                        this.setError(element.toString());
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
        super.clearError();
    }
}
