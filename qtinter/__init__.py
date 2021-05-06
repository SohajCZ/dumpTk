"""
Main Qtinter file.

In following imports, one can find imported classes Tkinter.
This decides how many classes from Tkinter are supported in Qtinter.

Tkinter is usually imported with one of following:
- star import - from tkinter import *
- import with as keyword - import tkinter as tk
After import, Tk class must be instantiated.

Class Tk here inherits from Tkinter class, which
means that most of methods stays same, therefore Tkinter
is used as some kind of preprocessor. To apply custom
logic, similar to Tkinter, Tk class here uses own TkWrapper
class to wrap around tk, but in reality TkWrapper here
wraps own class - Implementer - which implements main logic.

Outcome of all this is that when regular Tkinter call
methods from regular TkWrapper, it calls custom methods.
These custom methods are mainly:
- call - This method originally calls _tkinter module,
which forwards arguments to Tcl/Tk, which processes them.
These arguments have given structure for Tcl/Tk,
therefore are easily parse-able
in Implementer.
- createcommand - This method also calls _tkinter module,
with intention to create command in Tcl/Tk. QtCallWrapper,
similarly as original CallWrapper from Tkinter, encapsulates
this command (after decomposition from CallWrapper encapsulation)
and forwards it to Implementer as well to store this command.

StringVar class here prototypes usage of Tk variables.
Since Tk variables are originally stored in Tcl, it is
not easy to get value of variable from there. Therefore
Qtinter inherits original variable and substitutes it
for own class, of which value is not stored in Tcl.
"""
from tkinter import (Frame, Button, LabelFrame, Label, Entry,  # noqa
                     Radiobutton, Text, Menu, Spinbox, Scale,  # noqa
                     Listbox, Checkbutton, Event)  # noqa
from tkinter.ttk import (Combobox)  # noqa
from tkinter import StringVar as TkString
from tkinter import Tk as BaseTk

from .constants import * # noqa
from .implementer import Implementer, QAction
from .event_builder import EventBuilder, SUPPORTED_EVENTS


class StringVar(TkString):
    """This class overwrites default Tkinter variable string
    so we can work with it."""

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

    def __init__(self, func, subst):
        """Store FUNC, SUBST as members. Widget from original
        tkinter has been removed."""
        self.func = func
        self.subst = subst

    def __call__(self, *args):
        """Apply first function SUBST to arguments, than FUNC."""

        # Tkinter does not send clicked (button property
        # or QAction (menu) - so on those values, omit those.
        if type(*args) in [bool, QAction]:
            args = {}
        elif type(*args) in SUPPORTED_EVENTS:
            # Support bound events.
            eb = EventBuilder(*args)
            args = {eb.get_tk_event()}

        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit:
            raise


class TkWrapper:
    """Exchanges class from Tkinter for own class
    so methods are reimplemented with Qtinter."""

    def __init__(self, screenName, *args):
        """Creates Implementer instance."""
        self.tk = Implementer(screenName)

    def call(self, *args):
        """Main function which delegates call method from Tkinter
        to the Implemented"""
        return self.tk.call(*args)

    def createcommand(self, cbname, bound_method):
        """Implements encapsulating method to use own CallWrapper."""

        origin_call_wrapper = bound_method.__self__

        f = QtCallWrapper(origin_call_wrapper.func,
                          origin_call_wrapper.subst).__call__

        name = repr(id(f))

        try:
            name = name + f.__name__
        except AttributeError:
            pass

        return self.tk.createcommand(name, f, cbname)

    def mainloop(self, *args):
        """Delegates handling main loop."""
        return self.tk.mainloop(*args)

    # TODO: Methods below only for keeping interface.

    def getboolean(self, variable):
        # print(variable)
        # return self.tk.getboolean(variable)
        pass

    def globalsetvar(self, *args):
        # print(*args)
        # return self.tk.globalsetvar(*args)
        pass

    def globalunsetvar(self, *args):
        # print(*args)
        # return self.tk.globalunsetvar(*args)
        pass  # TODO

    def getvar(self, variable):
        # print(variable)
        # return self.tk.getvar(variable)
        return 8.6

    def deletecommand(self, cbname):
        # print(cbname)
        # return self.tk.deletecommand(cbname)
        pass

    # TODO: Upper methods below only for keeping interface.


class Tk(BaseTk):
    def __init__(self, screenName=None, baseName=None, className='Tk',
                 useTk=True, sync=False, use=None):
        """Initiates Tkinter but exchanges it for own TkWrapper."""
        super(Tk, self).__init__(screenName, baseName,
                                 className, useTk, sync, use)
        self.tk = TkWrapper(screenName, baseName, className, useTk, sync, use)
