import sys

from PyQt5.QtWidgets import QApplication, QWidget, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot

class Packable(): # TODO

    def pack(self, side=None): # TODO - side and also more params
        pass

class Subscriptable(): # TODO

    def __setitem__(self, key, data):
        # TODO - Should throw some exceptions
        if key == 'text': # TODO 8 milion lines problem...
            self.setText(data)
        return setattr(self, key, data)

    def __getitem__(self, key):
        return getattr(self, key) # TODO - Should throw some exceptions


class Button(QPushButton, Packable, Subscriptable):
    def __init__(self, master, text=None, fg=None, command=None): # TODO That params
        super(Button, self).__init__(text, master) # TODO fg, command
        self.command = command
        self.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.command()


class Frame(QWidget):
    def __init__(self, master):
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
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0

    def geometry(self, size): # TODO: Refactor, ints?
        self.size = size

        size_width = size[:size.find('x')]
        size = size[size.find('x'):][1:]
        self.width = int(size_width)

        size_height = size[:size.find('+')]
        size = size[size.find('+'):][1:]
        self.height = int(size_height)

        size_x = size[:size.find('+')]
        size = size[size.find('+'):][1:]
        self.x = int(size_x)

        self.y = int(size)


    def mainloop(self):
        # Solving geometry issue.
        if self.size is not None:
            self.first_window.resize(self.width,self.height)
            self.first_window.move(self.x,self.y)

        self.first_window.show()

        sys.exit(self.exec_())

    def destroy(self): # What about not window stuff?
        self.quit()

