import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

class Frame(QWidget):
    def __init__(self, master=None):
        self.master = master
        super(Frame, self).__init__()

    def mainloop(self):
        # TODO No geometry
        self.resize(200,100)
        self.move(50,150)

        self.show()
        sys.exit(self.master.exec_())
        

class Tk(QApplication):
    def __init__(self):
        super(Tk, self).__init__(sys.argv) # TODO Real args?

    def geometry(self, size):
        pass # TODO


