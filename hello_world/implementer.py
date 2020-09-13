from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout, \
                            QGroupBox, QMainWindow, QMenu, QAction, QSpinBox, QSlider, \
                            QCheckBox, QRadioButton, QListWidget, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

import tktoqt

from layouter import Layouter

TOP="top"
RIGHT="right"
BOTTOM="bottom"
LEFT="left"
RAISED="Whatever" #TODO
BOTH="Whatever" #TODO
YES="Whatever" #TODO
RIDGE="Whatever" #TODO
E="Whatever" #TODO
W="Whatever" #TODO
N="Whatever" #TODO
S="Whatever" #TODO
END="Whatever" #TODO
HORIZONTAL="Whatever" #TODO

def tracefunc(frame, event, arg, indent=[0]): # TODO: Remove v
      if event == "call":
          indent[0] += 2
          #print("-" * indent[0] + "> call function", frame.f_code.co_name)
      elif event == "return":
          #print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
          indent[0] -= 2
      return tracefunc

import sys
sys.setprofile(tracefunc)                    # TODO: Remove ^

# --------------------------------------------

def create_class_with_master(class_name, master):
    # TODO Doc
    if class_name in [QFont]:
        return class_name()
    else:
        return class_name(master)


# --------------------------------------------

translate_class_dict = {
    'frame': QWidget,
    'button': QPushButton,
    'label': QLabel,
    'entry': QLineEdit,
    'text': QFont,
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
    ttk_dict['ttk::'+item] = translate_class_dict[item] # TODO: Rightful omitment of ttk?

translate_class_dict.update(ttk_dict)


# --------------------------------------------

def translate_class(key):
    # TODO Doc
    return translate_class_dict[key]


class Menu(QMainWindow): # TODO: Rename, naming wrong ...

    def __init__(self):
        super().__init__()

        self.label = ""

        return

    def add_menu(self, menu):
        menubar = self.menuBar()

        if self.label != "":
            menu.setTitle(self.label) # TODO: This might be doing problems. IDK yet.
            self.label = ""

        menubar.addMenu(menu)

    def remember_label(self, label):
        if self.label != "":
            print("Warning - need to make queue") # TODO Remove if possible or implement queue
        self.label = label

# --------------------------------------------

class Implementer(QApplication):
    def __init__(self, name):
        super(Implementer, self).__init__([])
        self.namer = { '.': self, '.!menu': Menu() }
        self.commands = dict()
        self.window = None
        self.layouter = Layouter()
        self.menu = False

    def add_to_namer(self, key, item):
        # TODO: Docs. For controll but mainly for forcing own menu. Even when configured at last.
        if key not in self.namer:
            self.namer[key] = item
        else:
            if key != '.!menu':
                print("Warning - duplicated key entry for namer:", key)

    def create_menu(self, menu=None):
        # TODO: Docs.
        self.menu = True

    def show(self):
        if not self.window:
            self.window = QWidget() # TODO params
            self.window.setLayout(self.layouter.layout) # TODO This might solve it

        if self.menu: # Application has menu.
            self.namer['.!menu'].setCentralWidget(self.window)
            self.namer['.!menu'].show()
        else:
            self.window.show()

    def call_method(self, o, name, params):
        # TODO: Doc - "o" is object.; params needs to be translated
        if '.' in name: # TODO: IDK what else, but . should really not be in name ...
            func = self.commands.get(params)
            # TODO: EW
            if name.split('.')[0] == 'clicked':
                return o.clicked.connect(func)
            elif name.split('.')[0] == 'triggered[QAction]': # TODO Cant get here now
                return o.triggered[QAction].connect(func)

        try: # TODO: Remove this and support most of attributes
            return getattr(o, name)(params)
        except KeyError:
            pass

    def createcommand(self, cbname, bound_method, reassign_name=None):
        #print("Assign command: ", cbname, bound_method, reassign_name)
        if reassign_name:
            self.commands[reassign_name] = bound_method
        else:
            self.commands[cbname] = bound_method

    # TODO: Since not supporting multiple Frames / Widgets, for instance packing-tkinter example, it is not working everytime. 
    def _add_widget(self, widget, kind, other_args):
        if widget.__class__ == QFont:
            return # TODO What is purpose of setting grid to label? Why not labeled?

        self.layouter.add_widget(widget, kind, other_args)


    # TODO Variable Spellcheck
    def call(self, *args): # TODO: Args
        construct_command = args[0]

        if construct_command == 'info':
            #print(*args) # TODO This is stringvar ... already made with my StringVar.
            return

        #print("--------------------------")
        #print("Construct command", construct_command)

        if construct_command[0] == 'radiobutton':
            return # TODO Implement radiobutton

        if construct_command == 'destroy': # TODO Nasty hack, memory leaks I think
            self.quit()
            return

        if construct_command == 'wm': # TODO 'WM_DELETE_WINDOW'
            return

        # TODO Omit place.

        if type(construct_command) == str: # TODO: Buddies ? => .!labelframe2.!entry
            # TODO Why this is here ...???
            return

	# Parse other additional options
        additional_options = dict()

        if len(construct_command)>2:				# TODO Next to command and cascade could be menu-checkbox and so on.
            for i in range(2+(construct_command[0] in ['pack', 'grid'])+(construct_command[1] == 'add' and construct_command[2] in ['command', 'cascade', 'separator']), len(construct_command), 2):
                if construct_command[i] != '-menu':
                    additional_options[construct_command[i]] = construct_command[i+1]
                else: # Sneak PyQT menu instead of TKinter menu.
                    additional_options[construct_command[i]] = self.namer[str(construct_command[i+1])]
            #print(additional_options)

        # If packing insert widget
        if construct_command[0] in ['pack', 'grid']: # TODO: Also Grid & place exists.
            #print("Construct command", construct_command)
            #print(self.namer[construct_command[2]], additional_options)
            self._add_widget(self.namer[construct_command[2]],
                             construct_command[0], additional_options)
            return

        if construct_command[1] in ['configure', 'add', 'insert']: # Add for menu, insert for text
            widget = self.namer[construct_command[0]]

            # TODO: Separator to menu.
            # Translate additional options # TODO Done here and later
            additional_options = tktoqt.translate_parameters_for_class(widget.__class__, additional_options)

            if widget.__class__ == QMenu: # It is menu. Needs combinations. Maybe more. TODO
               # TODO Check if labels
               label = additional_options.pop('addAction', None)
               command = additional_options.pop('triggered[QAction].connect', None)
               action = QAction(label, widget)
               if command:
                   action.triggered.connect(self.commands[command])
               widget.addAction(action)

            # TODO: QList also needs combinations.

            for key in additional_options.keys():
               self.call_method(widget, key, additional_options[key])

            return # TODO Make it nicer

        class_name = translate_class(construct_command[0])

        # Translate additional options # TODO Done here and later
        additional_options = tktoqt.translate_parameters_for_class(class_name, additional_options)

        # Save master for future use.
        master_id = construct_command[1][:construct_command[1].rfind('.!')]

        # If there is no window created, take first window as main.
        if class_name in [QWidget, QGroupBox] and self.window is None:
            widget = class_name()
            self.window = widget
            self.layouter.master = widget # TODO This needs to be gone - layouter

        # Else create class w/wo master. Even when there is master, might not use him.
        if master_id != '':
            widget = create_class_with_master(class_name,self.namer[master_id])
        else:
            widget = class_name()
                
        for key in additional_options.keys():
            self.call_method(widget, key, additional_options[key])

        self.add_to_namer(construct_command[1], widget)


    def mainloop(self, *args):
        import sys
        self.show()
        sys.exit(self.exec_())


