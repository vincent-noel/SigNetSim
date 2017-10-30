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

class SliderForm extends Form
{
    constructor(field, description, default_value=1)
    {
        super(field, description, default_value);
        this.disabled = false;
    }

    getValue()
    {
        return ($('#' + this.field).prop('checked') == true);
    }

    switch_on()
    {
        if (!this.disabled) {
            $('#' + this.field).prop('checked', true);
        }
    }

    switch_off()
    {
        if (!this.disabled){
            $('#' + this.field).prop('checked', false);
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
