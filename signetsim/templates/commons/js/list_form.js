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
