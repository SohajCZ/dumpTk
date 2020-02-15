import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

class Frame(QWidget):
    def __init__(self, master=None):
        self.master = master

        # Solving geometry issue.
        if master.first_window is None:
            master.first_window = self

        super(Frame, self).__init__()

    def mainloop(self): # Interface solving Tkinter mainloop call on window issue.
        self.master.mainloop()
        

class Tk(QApplication):
    def __init__(self):
        super(Tk, self).__init__(sys.argv)
        # Solving geometry issue.
        self.size = None
        self.first_window = None

    def geometry(self, size):
        self.size = size

    def mainloop(self):
        # Solving geometry issue.
        self.first_window.resize(200,100)
        self.first_window.move(50,150)

        self.first_window.show()

        sys.exit(self.exec_())


