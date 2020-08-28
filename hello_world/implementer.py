from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout , \
                            QGroupBox, QMainWindow, QMenu, QAction
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

translate_class_dict = {
    'frame': QWidget,
    'button': QPushButton,
    'label': QLabel,
    'entry': QLineEdit,
    'text': QFont,
    'labelframe': QGroupBox,
    'menu': QMenu,
}


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
        self.namer = { '.': self }
        self.commands = dict()
        self.window = None
        self.layouter = Layouter()
        self.menu = None

    def create_menu(self, menu=None):
        # TODO: Docs. Menu here is menu from TKinter and I might need it later.
        self.menu = Menu()
        self.namer['.!menu'] = self.menu # Sneak own menu ... # TODO Hardcoded naming?

    def show(self):
        if not self.window:
            self.window = QWidget() # TODO params
            self.window.setLayout(self.layouter.layout) # TODO This might solve it

        if self.menu: # Application has menu.
            self.menu.setCentralWidget(self.window)
            self.menu.show()
        else:
            self.window.show()

    def call_method(self, o, name, params):
        # TODO: Doc - "o" is object.; params needs to be translated
        if '.' in name: # TODO: IDK what else, but . should really not be in name ...
            func = self.commands.get(params)
            # TODO: EW
            if name.split('.')[0] == 'clicked':
                return o.clicked.connect(func)
            elif name.split('.')[0] == 'triggered[QAction]':
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
    def _add_widget(self, widget, side=TOP, *args): # TODO: Other args
        self.layouter.add_widget(widget, "pack", side)

        return

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

	# Parse other aditional options
        aditional_options = dict()

        if len(construct_command)>2:				# TODO Next to command and cascade could be menu-checkbox and so on.
            for i in range(2+(construct_command[0] in ['pack', 'grid'])+(construct_command[1] == 'add' and construct_command[2] in ['command', 'cascade']), len(construct_command), 2):
                if construct_command[i] != '-menu':
                    aditional_options[construct_command[i]] = construct_command[i+1]
                else: # Sneak PyQT menu instead of TKinter menu.
                    aditional_options[construct_command[i]] = self.namer[str(construct_command[i+1])]
            #print(aditional_options)

        # If packing insert widget
        if construct_command[0] in ['pack']: # TODO: Also Grid & place exists.
            #print("Construct command", construct_command)
            #print(self.namer[construct_command[2]], aditional_options)
            self._add_widget(self.namer[construct_command[2]], side=aditional_options.get("-side",TOP))
            return

        if construct_command[0] in ['grid']: # TODO: Get together
            return

        if construct_command[1] in ['configure', 'add']: # Add for menu
            widget = self.namer[construct_command[0]]

            # Translace additional options # TODO Done here and later
            aditional_options = tktoqt.translate_parameters_for_class(widget.__class__, aditional_options)

            for key in aditional_options.keys():
               self.call_method(widget, key, aditional_options[key])

            return # TODO Make it nicer
            
        #print(construct_command)
        class_name = translate_class(construct_command[0])

        # Translate additional options # TODO Done here and later
        aditional_options = tktoqt.translate_parameters_for_class(class_name, aditional_options)

        # Save master
        master_id = construct_command[1][:construct_command[1].rfind('.!')]

        if class_name == QWidget:
            if self.window is None:
                widget = class_name() # TODO Different constructors - Widget, Button ...
                widget.resize(0,0) # TODO Hardcoded
                widget.move(50,50) # TODO Hardcoded
                self.window = widget # TODO: Only first one
                self.layouter.master = widget # TODO This needs to be gone
            else:
                widget = class_name(self.namer[master_id])
            self.namer[construct_command[1]] = widget

            for key in aditional_options.keys():
                self.call_method(widget, key, aditional_options[key])

            return # TODO Make it nicer

        if class_name == QPushButton:
            widget = class_name(aditional_options.get('-text', "N/A"), self.namer[master_id])
                
            for key in aditional_options.keys():
               self.call_method(widget, key, aditional_options[key])

            self.namer[construct_command[1]] = widget
            return # TODO Make it nicer

        # "Else"

        if master_id != '':
            widget = class_name(self.namer[master_id])
        else:
            widget = class_name()
                
        for key in aditional_options.keys():
            self.call_method(widget, key, aditional_options[key])

        self.namer[construct_command[1]] = widget




        #if isinstance(contruct_command, tuple): # TODO OK?
        #try:
        #except (KeyError, TypeError): # TODO - Key because Im lazy to implement all and Type because of StringVar BS
        # Hardcore parser I think ...

    def mainloop(self, *args):
        import sys
        self.show()
        sys.exit(self.exec_())


