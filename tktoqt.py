import sys

from parameters_mapping import (get_parameters_values_mapping,
                                get_parameters_names_mapping)


def translate_parameters_values(class_name, parameters):
    # TODO: Doc
    mapping = get_parameters_values_mapping(class_name)

    for parameter in parameters:
        if parameter in mapping:
            formatted = mapping[parameter].format(parameters[parameter])
            parameters[parameter] = formatted

    return parameters


def translate_parameters_names(class_name, parameters):
    # TODO: Doc

    mapping = get_parameters_names_mapping(class_name)
    translated_parameters = {}

    for parameter in parameters:
        if parameter not in mapping:
            print("Warning,", parameter, "for class",
                  class_name, "not in mapping.",
                  file=sys.stderr)
            continue

        translated_parameters[mapping[parameter]] = parameters[parameter]

    return translated_parameters


def translate_parameters_for_class(class_name, parameters):
    # TODO: Doc - parameters are dict
    # TODO: { "parameter_name": parameter_value, ... }

    # First call renaming values
    values_translated = translate_parameters_values(class_name, parameters)

    # Then change methods to call
    translated = translate_parameters_names(class_name, values_translated)

    return translated
