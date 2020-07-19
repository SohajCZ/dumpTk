from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, QBoxLayout
from PyQt5.QtCore import QCoreApplication

TOP="top"
RIGHT="right"
BOTTOM="bottom"
LEFT="left"
RAISED="Whatever"
BOTH="Whatever"
YES="Whatever"

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
translate_variables = {
    '-text': 'setText',
    '-command': 'clicked.connect',
    '-fg': 'setStyleSheet',
}

# For translating styling
translate_params = {
    'red': 'color: red;', # TODO: This could be improved to not have line for every needed color :) , also stating that red means foreground-color (color in PyQt) is quite bad
}

# For translating styling
def translate(param): 
    #print(param, translate_params.get(param, param))
    return translate_params.get(param, param) # Getter or ommiter

translate_class = {
    'frame': QWidget,
    'button': QPushButton
    #'entry': QLineEdit'
}


class Implementer(QApplication):
    def __init__(self, name):
        super(Implementer, self).__init__([])
        self.window = None
        self.namer = dict()
        self.commands = dict()
        self.content = QHBoxLayout()
        self.layout = self.content
        self.state = LEFT # Default
        #print("Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)

    def call_method(self, o, name, params):
        if 'clicked.' in name: # TODO: IDK what else, but . should really not be in name ...
            return o.clicked.connect(self.commands.get(params))
        return getattr(o, name)(translate(params))

    def createcommand(self, cbname, bound_method):
        #print("Assign command: ", cbname, bound_method)

        self.commands[cbname] = bound_method

    def _add_widget(self, widget, side=TOP, *args): # TODO: Other args
        #print("Before:: Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)

        if side in [LEFT, RIGHT]:
            if self.state not in [LEFT, RIGHT]: 
                self.content = QHBoxLayout()
                self.layout.addLayout(self.content)
                if side == RIGHT: # According to TK testing - once it is set up, it remains.
                    self.content.setDirection(QBoxLayout.RightToLeft)
            self.content.addWidget(widget)
        elif side in [TOP, BOTTOM]:
            if self.state not in [TOP, BOTTOM]: 
                self.content = QVBoxLayout()
                self.layout.addLayout(self.content)
                if side == BOTTOM: # According to TK testing - once it is set up, it remains.
                    self.content.setDirection(QBoxLayout.BottomToTop)
            self.content.addWidget(widget)

        self.state = side
        #print("After:: Content: ", self.content, "Layout: ", self.layout, "State: ", self.state)

    def call(self, *args): # TODO: Args
        construct_command = args

        #print("--------------------------")
        #print("Construct command", construct_command)

        if construct_command[0] == 'destroy': # TODO Nasty hack, memory leaks I think
            self.quit()
            return

        if construct_command[0] == 'wm': # TODO 'WM_DELETE_WINDOW'
            return

	# Parse other aditional options
        aditional_options = dict()

        if len(construct_command[0])>2:
            for i in range(2+(construct_command[0][0] in ['pack']), len(construct_command[0]), 2):
                aditional_options[construct_command[0][i]] = construct_command[0][i+1]
            #print(aditional_options)

        # If packing insert widget
        if construct_command[0][0] in ['pack']: # TODO: Also Grid & place exists.
            # print("Construct command", construct_command)
            # TODO: Side hardcoded below
            # print(self.namer[construct_command[0][2]], aditional_options)
            #self.package_manager.insert_widget(self.namer[construct_command[0][2]], side=aditional_options.get("-side",TOP))
            if self.namer[construct_command[0][2]] != self.window: # TODO: Hacking
                self._add_widget(self.namer[construct_command[0][2]], side=aditional_options.get("-side",TOP))
            return

        if construct_command[0][1] in ['configure']:
            widget = self.namer[construct_command[0][0]]
            for key in aditional_options.keys():
               self.call_method(widget, translate_variables[key], aditional_options[key])

            return # TODO Make it nicer
            
        #print(construct_command[0])
        class_name = translate_class[construct_command[0][0]]

        if class_name == QWidget:
            widget = class_name() # TODO Different constructors - Widget, Button ...
            widget.resize(0,0) # TODO Hardcoded
            widget.move(50,50) # TODO Hardcoded
            self.window = widget # TODO: Only first one
            self.window.setLayout(self.layout) # TODO: Hardcoded
            self.namer[construct_command[0][1]] = widget

        if class_name == QPushButton:
            widget = class_name(aditional_options.get('-text', "N/A"), self.window) # TODO This could not be the right "master".
                
            for key in aditional_options.keys():
               self.call_method(widget, translate_variables[key], aditional_options[key])

            self.namer[construct_command[0][1]] = widget
                
        return 



        #if isinstance(contruct_command, tuple): # TODO OK?
        #try:
        #except (KeyError, TypeError): # TODO - Key because Im lazy to implement all and Type because of StringVar BS
        # Hardcore parser I think ...

    def mainloop(self, *args):
        import sys
        self.window.show()
        sys.exit(self.exec_())


