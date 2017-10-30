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
