{% load static from staticfiles %}


function getStaticURL(){
    return "{% static '' %}";
}

function getMathValidatorURL(){
    return "{% url 'math_validator' %}";
}

function getSbmlIdValidatorURL(){
    return "{% url 'sbml_id_validator' %}";
}

function getModelNameValidatorURL(){
    return "{% url 'modelname_validator' %}";
}

function getFloatValidatorURL(){
    return "{% url 'float_validator' %}";
}

function getSBOTermURL(){
    return "{% url 'get_sbo_name' %}";
}

function getUsernameValidatorURL(){
    return "{% url 'username_validator' %}";
}
