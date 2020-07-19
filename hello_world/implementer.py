from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication

def tracefunc(frame, event, arg, indent=[0]): # TODO: Remove v
      if event == "call":
          indent[0] += 2
          print("-" * indent[0] + "> call function", frame.f_code.co_name)
      elif event == "return":
          print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
          indent[0] -= 2
      return tracefunc

import sys
sys.setprofile(tracefunc)                    # TODO: Remove ^

# This could mean quite work and also might need 1 for each of QT classes...
translate_variables = {
    '-text': 'setText',
    '-command': 'clicked.connect'
    #'-fg': pass # TODO: # Might need tuples for style
}

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

    def call_method(self, o, name, params):
        if 'clicked.' in name: # TODO: IDK what else, but . should really nat be in name ...
            return o.clicked.connect(self.commands[params])
        return getattr(o, name)(params)

    def createcommand(self, cbname, bound_method):
        #print("Assign command: ", cbname, bound_method)

        self.commands[cbname] = bound_method

    def call(self, *args):
        construct_command = args

        #print("--------------------------")
        #print("Construct command", construct_command)

        if construct_command[0] == 'destroy': # TODO Nasty hack, memory leaks I think
            self.quit()
            return

        if construct_command[0] == 'wm': # TODO 'WM_DELETE_WINDOW'
            return

        if construct_command[0][0] in ['pack']: # TODO Needs to setup packing manager
            return
        # TODO: Also Grid & place exists.

	# Parse other aditional options
        aditional_options = dict()

        if len(construct_command[0])>2:
            for i in range(2, len(construct_command[0]), 2):
                if construct_command[0][i] != '-fg': # TODO: styling
                        aditional_options[construct_command[0][i]] = construct_command[0][i+1]

        if construct_command[0][1] in ['configure']: # TODO Configuration of existing - via namer 
            widget = self.namer[construct_command[0][0]]
            for key in aditional_options.keys():
               self.call_method(widget, translate_variables[key], aditional_options[key])

            return # TODO Make it nicer
            
        print(construct_command[0])
        class_name = translate_class[construct_command[0][0]]

        if class_name == QWidget:
            widget = class_name() # TODO Different constructors - Widget, Button ...
            widget.resize(200,200) # TODO Hardcoded
            widget.move(50,50) # TODO Hardcoded
            self.window = widget
            self.namer[construct_command[0][1]] = widget

        if class_name == QPushButton:
            widget = class_name(aditional_options.get('-text', "N/A"), self.window)
                
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


