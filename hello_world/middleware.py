import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QHBoxLayout, QVBoxLayout, QGridLayout, \
                            QLineEdit
from PyQt5.QtCore import pyqtSlot

TOP="top"
RIGHT="right"
BOTTOM="bottom"
LEFT="left"
RAISED="Whatever"
BOTH="Whatever"
YES="Whatever"


class StringVar(): # Wth

    def __init__(self):
        self.text = ""

    def set(self, text):
        self.text = text

    def __str__(self):
        return self.text


class PackageManager():

    def __init__(self, master):
        self.master = master
        self.state = LEFT # Default
        self.row = 0 # Default
        self.column = 0 # Default
        self.layout = QGridLayout()
        self.content = QHBoxLayout() # Default
        self.layout.addLayout(self.content, self.row, self.column)

    def _decide_layout(self, side=TOP): # TODO: Other args
        # TODO: Support all, now only left and top (others need more manipulation)
        if self.state != side:
            if side == LEFT:
                self.content = QHBoxLayout()
                self.state = LEFT
                self.column += 1
            else:
                self.content = QVBoxLayout()
                self.state = TOP
                self.row += 1

            self.layout.addLayout(self.content, self.row, self.column)

    def insert_widget(self, widget, **other_args): # TODO: Other args
        self._decide_layout(other_args.get("side",TOP)) # TODO: Works?
        self.content.addWidget(widget)


class Packable(): # TODO

    def pack(self, **other_args): # TODO: Other args
        # TODO Isn't this kinda abusive?
        self.get_top_master().package_manager.insert_widget(self, **other_args)

    def get_top_master(self): # Recusive
        # TODO Isn't this kinda abusive?
        return self.master.get_top_master()


class Subscriptable(): # TODO

    def __setitem__(self, key, data):
        # TODO - Should throw some exceptions
        if key == 'text': # TODO 8 milion lines problem...
            self.setText(data)
        return setattr(self, key, data)

    def __getitem__(self, key):
        return getattr(self, key) # TODO - Should throw some exceptions


class Entry(QLineEdit, Packable):

    def __init__(self, master, textvariable=None):
        self.master = master
        super(QLineEdit, self).__init__(str(textvariable), master)


class Button(QPushButton, Packable, Subscriptable):
    def __init__(self, master, text=None, fg=None, command=None): # TODO That params
        super(Button, self).__init__(text, master) # TODO fg, command
        self.command = command
        self.master = master
        self.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.command()


class Frame(QWidget, Packable):
    def __init__(self, master, **other_args): # TODO: Other args
        self.master = master # Master could be frame !!!

        super(Frame, self).__init__()

        # Solving geometry issue.
        if hasattr(master, 'first_window') and master.first_window is None:
            master.first_window = self
            self.package_manager = PackageManager(self)
            self.setLayout(self.package_manager.layout)

        self.show() # TODO Uf uf hacks - needs to be recursive

    def mainloop(self): # Interface solving Tkinter mainloop call on window issue.
        self.master.mainloop()

    def get_top_master(self): # Override
        if hasattr(self.master, 'first_window'): # TODO: Hacks
            return self

        return self.master.get_top_master()
        

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

