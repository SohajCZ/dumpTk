"""
This file contains mappings:
parameters_names_mapping - Mapping of Tcl/Tk command attributes
                           to methods of Qt/own objects.
                           Own objects are included because
                           of implementation details such as
                           menu problem (see description of
                           Implementer file.
parameters_values_mapping - Mapping of Tcl/Tk attributes values
                           to valid values for parameters of
                           methods got from parameters_names_mapping.

Mappigs are obtained with get_parameters_names_mapping and
get_parameters_values_mapping functions respectively with
private _get_mapping function.

Mappings are used by tktoqt file.

Note that this could be heavily extended - TODO.
Note that this might get changed when problem with step 5) from Implementer
will be solved - TODO.
"""

parameters_names_mapping = {
    "all": {
        '-text': 'setText',
        '-fg': 'setStyleSheet',
        '-padx': 'setStyleSheet',
        '-pady': 'setStyleSheet',
        # TODO Margins and so on.
    },
    "QPushButton": {
        '-command': 'clicked.connect',
    },
    "QWidget": {
        '-width': 'setMinimumWidth',
        '-height': 'setMinimumHeight',
        '-background': 'setStyleSheet',
    },
    "QGridBox": {
        '-text': 'setTitle',
        '-relief': 'setStyleSheet',
    },
    "QMenu": {
        # TODO Remove if combinations working.
        '-label': 'addAction',
        # TODO Remove if combinations working.
        '-command': 'triggered[QAction].connect',
        '-menu': 'addMenu',
    },
    "QListWidget": {
        '-insert': 'addItem',
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
    "QRadioButton": {
        # TODO finish StringVar '-variable': 'setText',
        '-command': 'toggled.connect'
    },
    "QComboBox": {
        '-values': 'addItems',
        # TODO finish StringVar'-textvariable': 'setText',
    },
    "QPixmap": {
        '-file': 'load',
        # TODO finish StringVar'-textvariable': 'setText',
    },
    "Menu": {  # TODO: Might change name
        '-menu':  'add_menu',  # My own function
        '-label': 'remember_label',
    },
    "Implementer": {  # TODO: Might change name
        '-menu': 'create_menu',  # My own function
    },
}


def get_parameters_names_mapping(class_name):
    # TODO Docs.
    return _get_mapping(class_name, parameters_names_mapping)


parameters_values_mapping = {
    "all": {
        '-padx': 'padding: {} px;',
        # TODO Difference between horizontal and vertical padding? ...
        '-pady': 'padding: {} px;',
        '-fg': 'color: {} ;',
    },
    "QWidget": {
        '-background': 'background-color: {} ;',
    },
}


def get_parameters_values_mapping(class_name):
    # TODO Docs.
    return _get_mapping(class_name, parameters_values_mapping)


def _get_mapping(class_name, mapping):
    # TODO Docs.
    output = mapping["all"].copy()
    override_and_extra_parameters = mapping.get(class_name.__name__, {})
    for key in override_and_extra_parameters:
        output[key] = override_and_extra_parameters[key]
    return output
