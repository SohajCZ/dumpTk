parameters_names_mapping = { # TODO All
    "all": {
        '-text': 'setText',
        '-fg': 'setStyleSheet', # TODO For all? Test + implement
        '-padx': 'setStyleSheet', # TODO Implement
        '-pady': 'setStyleSheet', # TODO Implement
        # TODO Margins and so on.
    },
    "QPushButton": {
        '-command': 'clicked.connect',
    },
    "QWidget": {
        '-width': 'setMinimumWidth', # TODO Test
        '-height': 'setMinimumHeight', # TODO Test
        '-background': 'setStyleSheet', # TODO Test
    },
    "QGridBox": {
        '-text': 'setTitle',
        '-relief': 'setStyleSheet', # TODO Not really implemented
    },
#        '-width': 'setMaxLength', # Entry # TODO IDK if OK.
#        '-height': 'setPointSize', # Text # TODO IDK if OK.
}

def get_parameters_names_mapping(class_name):
    # TODO Docs.
    return _get_mapping(class_name, parameters_names_mapping)

# ----------------------------------------------

parameters_values_mapping = {
    "all": {
        '-padx': 'padding: {} px;',
        '-fg': 'color: {} ;',
        # TODO: Other common options
    },
    "QWidget": {
        '-background': 'background-color: {} ;', # TODO - This wont work.
    }
    # TODO - If any widget (or subclass) behaves differently.
}

def get_parameters_values_mapping(class_name):
    # TODO Docs.
    return _get_mapping(class_name, parameters_values_mapping)

# ----------------------------------------------

def _get_mapping(class_name, mapping):
    # TODO Docs.
    output = mapping["all"]
    override_and_extra_parameters = mapping.get(class_name.__name__, {})
    
    for key in override_and_extra_parameters:
         output[key] = override_and_extra_parameters[key]

    return output
    

