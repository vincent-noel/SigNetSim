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

        for (var [index, form] of this.list.entries()) {
            if (this.listErrorChecking[index] && form.hasError()){
                add_error_modal_v3(form);
                form.highlight();
                this.nb_errors++;
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