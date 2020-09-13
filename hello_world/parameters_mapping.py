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
    "QMenu": {
        '-label': 'addAction', # TODO Remove if combinations working.
        '-command': 'triggered[QAction].connect', # TODO Remove if combinations working.
        '-menu': 'addMenu',
    },
    "QGroupBox": {
        '-text': 'setTitle',
    },
    "QLabel": {
        '-text': 'setText',
    },
    "QSpinBox": {
        '-from': 'setMinimum',
        '-to': 'setMaximum',
    },
    "QComboBox": {
        # TODO '-values': 'addItems',
    },
    "Menu": { # TODO: Might change name
        '-menu':  'add_menu', # My own function
        '-label': 'remember_label',
    },
    "Implementer": { # TODO: Might change name
        '-menu': 'create_menu', # My own function
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
        '-pady': 'padding: {} px;', # TODO Well there is no difference between horizontal and vertical padding? ...
        '-fg': 'color: {} ;',
    },
    "QWidget": {
        '-background': 'background-color: {} ;',
    },
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
    

