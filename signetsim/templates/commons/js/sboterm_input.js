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
{% include 'commons/js/editable_input.js' %}

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
            "POST", "{% url 'get_sbo_name' %}",
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