"""
Class Implementer could be found in this file.
This class implements most of logic of Qtinter.
It also inherites from QApplication.

Main method of Implementer class is method 'call'.
This method takes argument, originally command for
Tcl/Tk, and parses it in following steps (also comments in code):
1) Forget all commands which are not helpful for Qt
2) Command usually contains some additional parameters, first extract those.
   Note that this calculation could use some refactoring - TODO.
3) If main command is about binding events, solve those and return.
   During this, function call_if_binding_holds is used, since
   Tkinter allows to bind commands to special shortcuts, but
   Qt has slots on widgets and shortcut is usually checked in this slot.
   There are two more files used for events: event_translate and event_builder.
   Note that call_if_binding_holds now supports only QKeyEvent,
   QMousePressEvent, and QEnterEvent - TODO.
4) If main command is about layout, geometry management and such,
   forward it to function which solves that,
   which delegates it to Layouter class; and return.
5) If main commands is about configuring following widgets (ListWidget,
   ComboBox, Menu and MenuAction), solve it and return.
   Note that this could be unified with some logic refactoring - TODO.
6) Construct basic widgets and return. During this, translate_class_dict
   with translation from Tk object (or Ttk) name to PyQt class is used.
Note that these steps could be refactored into facade/chain of responsibility,
or at least divide into more better organized functions.

Other methods of implementer class are:
- add_to_namer - Little function, which solves problem with menus (see below).
- create_menu - Function which triggers menu bar to show in application.
- show - Solves showing right widget as toplevel, which could be problematic
        when menu is used or main frame is not directly created (see below).
- call_method - Configures widget method with given parameters - used to
                apply additional parameters from step 2). Method name
                and parameters needs to be translated from basic Tcl/Tk
                command with translate_parameters_for_class function.
                Note that TODOs in this method should solve special step 5).
- createcommand - Since this command is already created by caller (TkWrapper),
                  this method only saves command into Implementers "cache".
- _add_widget - Adds widget to its master layout.
- mainloop - Starts PyQt application.

During all this, Implementer builds own "caches":
- namer - Stores widget under its name used in Tkinter. This is needed to find
          master widget when creating child widget, when assigning commands
          and many other.
- commands - Stores commands created by createcommand method. Used when
             command should be assigned to widget.
- layouter - Stores layout under name of widget.
- masters - Stores master widget under name of widget.
- bindings - Stores bindings under widget name. These bindings are then
            used in call_if_binding_holds function.

layouter and master "caches" are used together - each widget, on which is
any layout management applied, is placed in master widgets layout. If this
layout does not exists yet, it is created. This functions recursively.

As said, these "caches" has names of widgets as keys to its values,
because in Tcl/Tk, objects are identified with names.

The other class in this file is Menu.
This class inherites from QMainWindow toplevel widget,
which allows application to have menu. In Tkinter,
Appliaction class has availability to acquire menu, which
is not available in QApplication. When application had no menu,
Implementer class either creates own frame/widget or is given own frame,
which is shown with show method. When application should have menu,
this default widget is exchanged with this Menu class. It is not
really menu, it is just toplevel widget, which has availability to
acquire menu. Menu is created inside class with add_menu method.
Tkinter sometimes assign label of menu action before the action itself,
therefore remember_label method is implemented. Since Tkinter menu
is quite different from PyQt menu, it also needs to be given as needed,
which is solved when Implementors method add_to_namer is called.
See also Menu and Implementer method translations in parameters mapping.
Since Tkinter application can acquire menu, command -menu is translated to
Implementers create_menu, which in reality just checks flag, which is
then used to decide if Menu instance should be declared as central widget in
show method.

Note that content of translate_class_dict dict could be moved
to some unified settings of this project - TODO.
"""
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QGroupBox, QComboBox, QTextEdit,
                             QMainWindow, QMenu, QAction, QSpinBox,
                             QSlider, QCheckBox, QRadioButton, QListWidget,
                             QScrollBar)
from PyQt5.QtGui import QPixmap, QKeyEvent, QMouseEvent, QEnterEvent
from PyQt5.QtCore import QEvent

from .tktoqt import translate_parameters_for_class
from .layouter import Layouter
from .event_translate import (get_method_for_type, sequence_parser,
                              tk_modifier_to_qt)

# TODO: Future improvement: Move to "settings".
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
    'photo': QPixmap,
    'toplevel': QMainWindow,
    'scrollbar': QScrollBar,
}

ttk_dict = {}

for item in translate_class_dict:
    # Ttk is not supported differently.
    ttk_dict['ttk::'+item] = translate_class_dict[item]

translate_class_dict.update(ttk_dict)


def translate_class(key):
    """Returns Qt class for Tk class name."""
    return translate_class_dict[key]


def call_if_binding_holds(bindings, event):
    """ This method serves as guard which checks if binding holds."""
    for binding in bindings:
        or_modifier = 0
        for modifier in binding[1]:
            or_modifier |= modifier

        if issubclass(type(event), QEvent):
            if type(event) == QKeyEvent:
                if (binding[0] == '' or
                    int(event.key()) == ord(binding[0].upper())) and \
                        int(event.modifiers()) == int(or_modifier):
                    binding[2](event)
                    return
            elif type(event) == QMouseEvent:
                if (binding[0] == '' or
                    int(event.button()) == int(binding[0])) and \
                        int(event.modifiers()) == int(or_modifier):
                    binding[2](event)
                    return
            if issubclass(type(event), QEvent):
                if type(event) == QEnterEvent:
                    binding[2](event)

            # TODO: More events ...


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
        #: Key bindings for widgets
        self.bindings = {}
        self.menu = False
        #: Dict of widgets ids as keys and their master widgets ids as values
        self.masters = dict()

    def add_to_namer(self, key, item):
        """Function for controll what is added to cache of names of widgets.
        This is implemented mainly because of exchanging QtMenu for TkMenu."""

        if key not in self.namer:
            self.namer[key] = item
        else:
            if key != '.!menu':
                print("Warning - duplicated key entry for namer:",
                      key, file=sys.stderr)

    def create_menu(self, menu=None):
        """Function which triggers menu bar to show in application."""
        self.menu = True

    def show(self):
        """Solves showing right widget as toplevel, which could be problematic
        when menu is used or main frame is not directly created."""

        if not self.window:
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
        """Configures "o" widgets "name" method with "params".
        Note that name and params needs to be translated with
        "translate_parameters_for_class" function. Note that
        TODOs in this method should solve special step 5) as
        mentioned at start of this file."""

        # TODO: Prepare combinations.
        if '.' in name:
            func = self.commands.get(params)
            return getattr(o, name.split('.')[0]).connect(func)

        # elif name.split('.')[0] == 'triggered[QAction]':
            # TODO Cant get here now - stays until combinations
            # return o.triggered[QAction].connect(func)

        try:  # TODO: Remove this and support most of attributes
            return getattr(o, name)(params)
        except KeyError:
            print("Warning, method", name, "for object",
                  o, "does not exists.",
                  file=sys.stderr)
            pass

    def createcommand(self, cbname, bound_method, reassign_name=None):
        """Since this command is already created by caller (TkWrapper),
        this method only saves command into Implementers "cache"."""
        # print("Assign command: ", cbname, bound_method, reassign_name)
        if reassign_name:
            self.commands[reassign_name] = bound_method
        else:
            self.commands[cbname] = bound_method

    def _add_widget(self, widget_id, kind, other_args):
        """Adds widget to its master layout"""
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

        # -------- Begin of step 1 - Omit clutter -----------------------------

        if construct_command == 'info':
            # This is stringvar ... already made with my StringVar.
            return

        # print("--------------------------")
        # print("Construct command", construct_command)

        if construct_command == 'destroy':
            self.quit()
            return

        if construct_command in ['wm', 'bind']:  # TODO 'WM_DELETE_WINDOW'
            # print(args)
            return

        # -------- Begin of step 2 - Parsing assitional arguments -------------

        # Omitting place

        # Adding text to QLineEdit # TODO This is "other arg bs"
        if type(construct_command) == str:
            construct_command = args

        # TODO: Really needed like this? IDK yet
        if construct_command[0] == 'image':
            construct_command = construct_command[2:]

        # Parse other additional options
        additional_options = dict()

        if len(construct_command) > 2:
            # TODO: Calculate range from line by line
            for i in range(
                    2 +
                    (construct_command[0] in ['pack', 'grid']) +
                    (construct_command[1] in ['add'] and construct_command[2]
                        in ['command', 'cascade', 'separator', 'checkbutton'])
                    -
                    (construct_command[1] in ['current', 'rowconfigure',
                                              'mark', 'columnconfigure',
                                              'entryconfigure']),
                    len(construct_command), 2):
                if construct_command[i] != '-menu':
                    if (i+1 >= len(construct_command) and
                            construct_command[1] == 'insert'):
                        print("There are 2 different commands",
                              "with same format.")
                        break
                    additional_options[construct_command[i]] = \
                        construct_command[i+1]
                else:  # Sneak PyQT menu instead of TKinter menu.
                    additional_options[construct_command[i]] = \
                        self.namer[str(construct_command[i+1])]

        # -------- Begin of step 3 - bindings ---------------------------------
        if construct_command[0] in ['bind']:
            # We might need to rename from 'all' to '.' (bind_all)
            name_of_widget = construct_command[1]

            if name_of_widget == 'all':
                # Map it to main widget. Camouflage it as toplevel.
                if not self.window:
                    self.window = QWidget()

                widget = self.window
                name_of_widget = '.'
            else:
                widget = self.namer[name_of_widget]

            sequence_parsed = sequence_parser(construct_command[2])
            widget_method = get_method_for_type(sequence_parsed["Type"])

            # Prepare bindings, if not yet
            if name_of_widget not in self.bindings:
                self.bindings[name_of_widget] = {}

            if widget_method not in self.bindings[name_of_widget]:
                self.bindings[name_of_widget][widget_method] = []

            modifiers = []
            if sequence_parsed["Mod1"]:
                modifiers.append(tk_modifier_to_qt(sequence_parsed["Mod1"]))
            if sequence_parsed["Mod2"]:
                modifiers.append(tk_modifier_to_qt(sequence_parsed["Mod2"]))

            command = self.commands[construct_command[3][6:].split(' ')[0]]

            self.bindings[name_of_widget][widget_method].append(
                (sequence_parsed["Detail"], modifiers, command))

            setattr(widget, widget_method, lambda event: call_if_binding_holds(
                self.bindings[name_of_widget][widget_method], event))

            return

        # -------- Begin of step 4 - layouts ----------------------------------
        # If packing insert widget
        if construct_command[0] in ['pack', 'grid']:
            self._add_widget(construct_command[2],
                             construct_command[0], additional_options)
            return  # TODO Nicer?

        # -------- Begin of step 5 - "special" widgets ------------------------
        # Add for menu, insert for text, current for combobox
        if construct_command[1] in ['configure', 'add', 'insert', 'current',
                                    'tag', 'entryconfigure']:
                        # TODO: Why tag, entryconfigure
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
            additional_options = translate_parameters_for_class(
                widget.__class__, additional_options)

            if widget.__class__ == QMenu:  # TODO Combinations
                # TODO Check if labels
                label = additional_options.pop('addAction', None)
                command = additional_options.pop(
                    'triggered[QAction].connect', None)
                accelerator = additional_options.pop(
                    '-accelerator', None)
                checkable = construct_command[2] == 'checkbutton'
                if accelerator:
                    action = QAction(label, widget, accelerator,
                                     checkable=checkable)
                else:
                    action = QAction(label, widget)
                if command:
                    action.triggered.connect(self.commands[command])
                widget.addAction(action)

            for key in additional_options.keys():
                self.call_method(widget, key, additional_options[key])

            return  # TODO Make it nicer

        # -------- Begin of step 6 - construct basic widgets ------------------

        class_name = translate_class(construct_command[0])

        # Translate additional options # TODO Done here and later
        additional_options = translate_parameters_for_class(
            class_name, additional_options)

        # Save master for future use.
        master_id = construct_command[1][:construct_command[1].rfind('.!')]

        # If there is no window created, take first window as main.
        if class_name in [QWidget, QGroupBox,
                          QMainWindow] and self.window is None:
            widget = class_name()
            self.window = widget

        # Else create class w/wo master.
        if class_name in [QPixmap]:
            self.masters[construct_command[1]] = None
            widget = class_name()
        elif master_id != '':
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
        """Starts PyQt application."""
        import sys
        self.show()
        sys.exit(self.exec_())
