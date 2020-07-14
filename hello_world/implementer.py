from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication

# This could mean quite work and also for each of QT classes...
translate_variables = {
    '-textvariable': 'contents'
}

translate_class = {
    'frame': QWidget,
    'button': QPushButton
    #'entry': QLineEdit'
}

# Reserved words - just omit thos I think I dont need.
reserved_words = ['wm']


class Implementer(QApplication):
    def __init__(self, name):
        super(Implementer, self).__init__([])

    def translate(self, contruct_command):
        pass

    def call(self, *args):
        contruct_command = args

        #print("Command", contruct_command)

        if contruct_command[0] == 'wm': # TODO Wildcard
            return

        if contruct_command[0][0] in ['pack']: # TODO Wildcard
            return

        if contruct_command[0][1] in ['configure']: # TODO Wildcard
            return

        if contruct_command[0][0] not in reserved_words:
            print(contruct_command[0])
            class_name = translate_class[contruct_command[0][0]]
            
            if class_name == QWidget:
                widget = class_name()
                widget.resize(200,200)
                widget.move(50,50)
                self.window = widget

            if class_name == QPushButton and len(contruct_command[0])>3 and contruct_command[0][2] == '-text':
                widget = class_name(contruct_command[0][3], self.window)




        #if isinstance(contruct_command, tuple): # TODO OK?
        #try:
        #except (KeyError, TypeError): # TODO - Key because Im lazy to implement all and Type because of StringVar BS
        # Hardcore parser I think ...

    def mainloop(self, *args):
        import sys
        self.window.show()
        sys.exit(self.exec_())


