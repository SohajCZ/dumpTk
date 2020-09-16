import sys

import tktoqt

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QGroupBox, QComboBox, QTextEdit,
                             QMainWindow, QMenu, QAction, QSpinBox,
                             QSlider, QCheckBox, QRadioButton, QListWidget)

from layouter import Layouter

translate_class_dict = {
    'frame': QWidget,
    'button': QPushButton,
    'label': QLabel,
    'entry': QLineEdit,
    'text': QTextEdit,
    'labelframe': QGroupBox,
    'menu': QMenu,
    'spinbox': QSpinBox,
    'scale': QSlider,
    'checkbutton': QCheckBox,
    'radiobutton': QRadioButton,
    'listbox': QListWidget,
    'combobox': QComboBox,
}

ttk_dict = {}

for item in translate_class_dict:
    # TODO: Rightful omit of ttk?
    ttk_dict['ttk::'+item] = translate_class_dict[item]

translate_class_dict.update(ttk_dict)


def translate_class(key):
    # TODO Doc
    return translate_class_dict[key]


class Menu(QMainWindow):  # TODO: Rename, naming wrong ...

    def __init__(self):
        super().__init__()

        self.label = ""

        return

    def add_menu(self, menu):
        menubar = self.menuBar()

        if self.label != "":
            menu.setTitle(self.label)
            self.label = ""

        menubar.addMenu(menu)

    def remember_label(self, label):
        if self.label != "":
            # TODO Remove if possible or implement queue
            print("Warning - need to make queue", file=sys.stderr)
        self.label = label


class Implementer(QApplication):
    def __init__(self, name):
        super(Implementer, self).__init__([])
        #: Dict of widgets ids as keys and widget objects as values
        self.namer = {'.': self, '.!menu': Menu()}
        self.commands = dict()
        self.window = None
        #: Dict of widgets ids as keys and their layouts (Layouter) as values
        self.layouter = {'.': Layouter()}
        self.menu = False
        #: Dict of widgets ids as keys and their master widgets ids as values
        self.masters = dict()

    def add_to_namer(self, key, item):
        # TODO: Docs. For controll but mainly for forcing own menu.
        #  TODO: Even when configured at last.
        if key not in self.namer:
            self.namer[key] = item
        else:
            if key != '.!menu':
                print("Warning - duplicated key entry for namer:",
                      key, file=sys.stderr)

    def create_menu(self, menu=None):
        # TODO: Docs.
        self.menu = True

    def show(self):
        if not self.window:  # TODO Check this part after master layout rework
            self.window = QWidget()

        # Some applications might not have layouts.
        if self.layouter['.'].inited:
            self.window.setLayout(self.layouter['.'].layout)

        if self.menu:  # Application has menu.
            self.namer['.!menu'].setCentralWidget(self.window)
            self.namer['.!menu'].show()
        else:
            self.window.show()

    def call_method(self, o, name, params):
        # TODO: Doc - "o" is object.; params needs to be translated

        # TODO: Prepare combinations.
        if '.' in name:
            func = self.commands.get(params)
            # TODO: Switch, different file
            # TODO: Could connect more observables.
            if name.split('.')[0] == 'clicked':  # QPushButton
                return o.clicked.connect(func)
            elif name.split('.')[0] == 'toggled':  # QRadioButton
                return o.toggled.connect(func)
            # elif name.split('.')[0] == 'triggered[QAction]':
                # TODO Cant get here now - stays until combinations
                # return o.triggered[QAction].connect(func)

        try:  # TODO: Remove this and support most of attributes
            return getattr(o, name)(params)
        except KeyError:
            pass

    def createcommand(self, cbname, bound_method, reassign_name=None):
        # print("Assign command: ", cbname, bound_method, reassign_name)
        if reassign_name:
            self.commands[reassign_name] = bound_method
        else:
            self.commands[cbname] = bound_method

    def _add_widget(self, widget_id, kind, other_args):
        master_id = self.masters[widget_id]
        widget = self.namer[widget_id]
        master_created = False

        # Check if master needs layout.
        if master_id not in self.layouter:
            self.layouter[master_id] = Layouter()
            master_created = True

        # Add widget to masters layout.
        self.layouter[master_id].add_widget(widget, kind, other_args)

        # If new master, set its layout.
        if master_created:
            self.namer[master_id].setLayout(self.layouter[master_id].layout)

    def call(self, *args):
        construct_command = args[0]

        if construct_command == 'info':
            # This is stringvar ... already made with my StringVar.
            return

        # print("--------------------------")
        # print("Construct command", construct_command)

        if construct_command == 'destroy':
            self.quit()
            # TODO: If destroy, then in args is second parameter,
            # TODO: which is master of deleted widget.
            return

        if construct_command == 'wm':  # TODO 'WM_DELETE_WINDOW'
            return

        # TODO Omit place (???)

        # Adding text to QLineEdit
        if type(construct_command) == str:
            construct_command = args

        # Parse other additional options
        additional_options = dict()

        if len(construct_command) > 2:
            # TODO: Calculate range from line by line
            for i in range(
                    2 +
                    (construct_command[0] in ['pack', 'grid']) +
                    (construct_command[1] in ['add'] and construct_command[2]
                        in ['command', 'cascade', 'separator']) -
                    (construct_command[1] in ['current']),
                    len(construct_command), 2):
                if construct_command[i] != '-menu':
                    additional_options[construct_command[i]] = \
                        construct_command[i+1]
                else:  # Sneak PyQT menu instead of TKinter menu.
                    additional_options[construct_command[i]] = \
                        self.namer[str(construct_command[i+1])]

        # If packing insert widget
        if construct_command[0] in ['pack', 'grid']:
            self._add_widget(construct_command[2],
                             construct_command[0], additional_options)
            return  # TODO Nicer?

        # Add for menu, insert for text, current for combobox
        if construct_command[1] in ['configure', 'add', 'insert', 'current']:
            widget = self.namer[construct_command[0]]

            # Inserting to List. # TODO Combinations
            if widget.__class__ == QListWidget:
                additional_options['-insert'] = construct_command[3]
                # TODO: Others? Remove?
                # TODO: Support orientation

            if (widget.__class__ == QComboBox and
                    '-values' in additional_options):
                # Translate string of {values} into array with values.
                additional_options['-values'] = additional_options[
                    '-values'][1:].replace('{', '')[:-1].split('} ')

            if (widget.__class__ in [QTextEdit, QLineEdit] and
                    len(construct_command) > 3):
                additional_options['-text'] = construct_command[3]

            # TODO: QComboBoxCurrent???

            # TODO: Separator to menu.
            # Translate additional options # TODO Done here and later
            additional_options = tktoqt.translate_parameters_for_class(
                widget.__class__, additional_options)

            if widget.__class__ == QMenu:  # TODO Combinations
                # TODO Check if labels
                label = additional_options.pop('addAction', None)
                command = additional_options.pop(
                    'triggered[QAction].connect', None)
                action = QAction(label, widget)
                if command:
                    action.triggered.connect(self.commands[command])
                widget.addAction(action)

            for key in additional_options.keys():
                self.call_method(widget, key, additional_options[key])

            return  # TODO Make it nicer

        class_name = translate_class(construct_command[0])

        # Translate additional options # TODO Done here and later
        additional_options = tktoqt.translate_parameters_for_class(
            class_name, additional_options)

        # Save master for future use.
        master_id = construct_command[1][:construct_command[1].rfind('.!')]

        # If there is no window created, take first window as main.
        if class_name in [QWidget, QGroupBox] and self.window is None:
            widget = class_name()
            self.window = widget

        # Else create class w/wo master.
        if master_id != '':
            # Create widget, some might not need master, let function decide.
            widget = class_name(self.namer[master_id])
            # Insert master to mapping
            self.masters[construct_command[1]] = master_id
        else:
            self.masters[construct_command[1]] = '.'
            widget = class_name()

        for key in additional_options.keys():
            self.call_method(widget, key, additional_options[key])

        self.add_to_namer(construct_command[1], widget)

    def mainloop(self, *args):
        import sys
        self.show()
        sys.exit(self.exec_())
