from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout , \
                            QGroupBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication

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

# This could mean quite work and also might need 1 for each of QT classes...
# TODO Yep, Labeld Frame :(
translate_variables_dict_all = {
    '-text': 'setText',
    '-command': 'clicked.connect',
    '-fg': 'setStyleSheet',
    '-padx': 'setStyleSheet',
    '-pady': 'setStyleSheet',
    '-width': 'setMaxLength', # Entry
    '-height': 'setPointSize', # Text
}

translate_variables_dict_grid_box = {
    '-text': 'setTitle',
    '-command': 'clicked.connect',
    '-fg': 'setStyleSheet',
    '-padx': 'setStyleSheet',
    '-pady': 'setStyleSheet',
    '-relief': 'setStyleSheet',
}

def translate_variables(class_name, key):
    if class_name == QGroupBox: # TODO Switch? (pythonic)
        return translate_variables_dict_grid_box[key]
    else:
        return translate_variables_dict_all[key]

# For translating styling => # TODO Rework
translate_params = {
    'red': 'color: red;', # TODO: This could be improved to not have line for every needed color :) , also stating that red means foreground-color (color in PyQt) is quite bad
    5: 'padding:5px' # TODO THIS
}

# For translating styling
def translate(param):
    return translate_params.get(param, param) # Getter or ommiter

translate_class = {
    'frame': QWidget,
    'button': QPushButton,
    'label': QLabel,
    'entry': QLineEdit,
    'text': QFont,
    'labelframe': QGroupBox,
}


class Implementer(QApplication):
    def __init__(self, name):
        super(Implementer, self).__init__([])
        self.namer = { '.': self }
        self.commands = dict()
        self.content = None
        self.layout = None
        self.state = None # Default
        self.window = None
        #print("Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)

    def show(self):
        if not self.window:
            self.window = QWidget() # TODO params

        self.window.show()

    def call_method(self, o, name, params):
        if 'clicked.' in name: # TODO: IDK what else, but . should really not be in name ...
            func = self.commands.get(params)
            return o.clicked.connect(func)

        try: # TODO: Remove this and support most of attributes
            return getattr(o, name)(translate(params))
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
        #print("Before:: Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)
        if self.state is None: # First time
             if side in [TOP, BOTTOM]:
                 self.content = QVBoxLayout()
                 if side == BOTTOM: # According to TK testing - once it is set up, it remains.
                    self.content.setDirection(QBoxLayout.BottomToTop)
             elif side in [LEFT, RIGHT]:
                 self.content = QHBoxLayout()
                 if side == RIGHT: # According to TK testing - once it is set up, it remains.
                    self.content.setDirection(QBoxLayout.RightToLeft)
             self.layout = self.content
             self.window.setLayout(self.content)
             self.state = side
             #print("After:: Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)
             return

        if side in [TOP, BOTTOM]:
            if self.state not in [TOP, BOTTOM]:
                content = QVBoxLayout()
                if side == BOTTOM: # According to TK testing - once it is set up, it remains.
                    content.setDirection(QBoxLayout.BottomToTop)
                self.content.addLayout(content)
                self.content = content
            self.content.addWidget(widget)
        elif side in [LEFT, RIGHT]:
            if self.state not in [LEFT, RIGHT]: 
                content = QHBoxLayout()
                if side == RIGHT: # According to TK testing - once it is set up, it remains.
                    content.setDirection(QBoxLayout.RightToLeft)
                self.content.addLayout(content)
                self.content = content
            self.content.addWidget(widget)

        self.state = side
        #print("After:: Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)
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

        if len(construct_command)>2:
            for i in range(2+(construct_command[0] in ['pack', 'grid']), len(construct_command), 2):
                aditional_options[construct_command[i]] = construct_command[i+1]
            #print(aditional_options)

        # If packing insert widget
        if construct_command[0] in ['pack']: # TODO: Also Grid & place exists.
            #print("Construct command", construct_command)
            #print(self.namer[construct_command[2]], aditional_options)
            self._add_widget(self.namer[construct_command[2]], side=aditional_options.get("-side",TOP))
            return

        if construct_command[0] in ['grid']: # TODO: Get together
            return

        if construct_command[1] in ['configure']:
            widget = self.namer[construct_command[0]]
            for key in aditional_options.keys():
               self.call_method(widget, translate_variables(widget.__class__, key), aditional_options[key])

            return # TODO Make it nicer
            
        #print(construct_command)
        class_name = translate_class[construct_command[0]]

        if class_name == QWidget:
            if self.window is None:
                widget = class_name() # TODO Different constructors - Widget, Button ...
                widget.resize(0,0) # TODO Hardcoded
                widget.move(50,50) # TODO Hardcoded
                self.window = widget # TODO: Only first one
            else:
                widget = class_name(self.namer[construct_command[1][:construct_command[1].rfind('.!')]])
            self.namer[construct_command[1]] = widget
            return # TODO Make it nicer

        if class_name == QPushButton:
            widget = class_name(aditional_options.get('-text', "N/A"), self.namer[construct_command[1][:construct_command[1].rfind('.!')]])
                
            for key in aditional_options.keys():
               self.call_method(widget, translate_variables(widget.__class__, key), aditional_options[key])

            self.namer[construct_command[1]] = widget
            return # TODO Make it nicer

        # "Else"

        if construct_command[1][:construct_command[1].rfind('.!')] != '':
            widget = class_name(self.namer[construct_command[1][:construct_command[1].rfind('.!')]])
        else:
            widget = class_name()
                
        for key in aditional_options.keys():
            self.call_method(widget, translate_variables(widget.__class__, key), aditional_options[key])

        self.namer[construct_command[1]] = widget




        #if isinstance(contruct_command, tuple): # TODO OK?
        #try:
        #except (KeyError, TypeError): # TODO - Key because Im lazy to implement all and Type because of StringVar BS
        # Hardcore parser I think ...

    def mainloop(self, *args):
        import sys
        self.show()
        sys.exit(self.exec_())


