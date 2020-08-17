from PyQt5.QtWidgets import *
from parameters_mapping import get_parameters_values_mapping, get_parameters_names_mapping

def translate_parameters_values(class_name, parameters):
    # TODO: Doc
    mapping = get_parameters_values_mapping(class_name)
 
    for parameter in parameters:
        if parameter in mapping:
            formated = mapping[parameter].format(parameters[parameter])
            parameters[parameter] = formated

    return parameters


def translate_parameters_names(class_name, parameters):
    # TODO: Doc
    mapping = get_parameters_names_mapping(class_name)
    translated_parameters = {}
 
    for parameter in parameters:
        translated_parameters[mapping[parameter]] = parameters[parameter]

    return translated_parameters


def translate_parameters_for_class(class_name, parameters):
    # TODO: Doc - parameters are dict { "parameter_name": parameter_value, ... }

    #print("Parameters:", parameters)

    # First call renaming values
    values_translated = translate_parameters_values(class_name, parameters)

    #print("Values:", values_translated)

    # Then change methods to call
    translated = translate_parameters_names(class_name, values_translated)

    #print("Translated:", translated)

    return translated


