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
