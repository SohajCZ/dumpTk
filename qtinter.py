# TODO: This could be how much I want to support tkinter
from tkinter import (Frame, Button, LabelFrame, Label, Entry,
                     Radiobutton, Text, Menu, Spinbox, Scale,
                     Listbox, Checkbutton)
from tkinter.ttk import (Combobox)
# TODO Comment why - want to handle this myself.
from tkinter import StringVar as TkString
from tkinter import Tk as BaseTk
from tkinter import (TOP, RIGHT, BOTTOM, LEFT, RAISED, BOTH,
                     YES, RIDGE, E, W, N, S, END, HORIZONTAL)

from implementer import Implementer, QAction  # TODO Ok import?


class StringVar(TkString):
    def __init__(self, master=None, value=None, name=None):
        super(StringVar, self).__init__(master, value, name)
        self.value = value

    def __str__(self):
        return self.value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class QtCallWrapper:
    """Internal class. Stores function to call when some user
    defined Tcl function is called e.g. after an event occurred."""

    def __init__(self, func, subst):  # TODO Removed widget
        """Store FUNC, SUBST and WIDGET as members."""
        self.func = func
        self.subst = subst

    def __call__(self, *args):
        """Apply first function SUBST to arguments, than FUNC."""

        # if type(*args) == QAction: # TODO: Generated from Menu buttons
        #     print(*args)

        # if type(*args) == bool: # TODO: Generated from PushButtons
        #     print(*args)

        # TKinter does not send clicked / QAction / so on values, omit those.
        if type(*args) in [bool, QAction]:
            args = {}

        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit:
            raise


class TkWrapper:

    def __init__(self, screenName, baseName,
                 className, useTk, sync, use):  # TODO: Params
        self.tk = Implementer(screenName)

    def call(self, *args):  # TODO: Wildcard
        # print(*args)
        return self.tk.call(*args)

    def createcommand(self, cbname, bound_method):
        origin_call_wrapper = bound_method.__self__

        f = QtCallWrapper(origin_call_wrapper.func,
                          origin_call_wrapper.subst).__call__

        name = repr(id(f))

        try:
            name = name + f.__name__
        except AttributeError:
            pass

        return self.tk.createcommand(name, f, cbname)

    def getboolean(self, variable):  # TODO
        # print(variable)
        # return self.tk.getboolean(variable)
        # TODO: This might need some hack or research
        pass  # TODO

    def globalsetvar(self, *args):  # TODO # TODO: Wildcard
        # print(*args)
        # return self.tk.globalsetvar(*args)
        pass  # TODO

    def globalunsetvar(self, *args):  # TODO # TODO: Wildcard
        # print(*args)
        # return self.tk.globalunsetvar(*args)
        pass  # TODO

    def getvar(self, variable):
        # print(variable)
        # return self.tk.getvar(variable)
        # TODO: This might need some hack or research
        return 8.6  # TODO

    def mainloop(self, *args):  # Not really interesting.
        return self.tk.mainloop(*args)

    def deletecommand(self, cbname):
        # print(cbname)
        # return self.tk.deletecommand(cbname)
        pass  # TODO


class Tk(BaseTk):
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=True, sync=False, use=None):
        super(Tk, self).__init__(screenName, baseName,
                                 className, useTk, sync, use)
        self.tk = TkWrapper(screenName, baseName, className, useTk, sync, use)
