from tkinter import Event
from PyQt5.QtGui import (QEnterEvent, QInputEvent, QKeyEvent,
                         QMouseEvent, QWheelEvent, QFocusEvent)

from .event_translate import mouse_button_translator

# Not implemented events:
# QNativeGestureEvent, QTabletEvent, QContextMenuEvent,
# QHoverEvent, QTouchEvent, ... other not inheriting QInputEvent

SUPPORTED_EVENTS = [QEnterEvent, QInputEvent, QKeyEvent,
                    QMouseEvent, QWheelEvent]


class EventBuilder:
    """Builds TkEvent from QtEvent."""

    def __init__(self, qt_event):
        self.qt_event = qt_event
        self.tk_event = None

    def get_tk_event(self):
        """Returns TkEvent from QtEvent."""

        if self.tk_event is not None:
            return self.tk_event

        return self._build_tk_event()

    def _build_tk_event(self):
        """Builds TkEvent from QtEvent."""

        # Tkinter Event:
        # %# %b %f %h %k %s %t %w %x %y %A %E %K %N %W %T %X %Y %D

        # Source:
        # http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html

        # TODO: Future improvement: Write setter method

        self.tk_event = Event()

        # serial - serial number of event - did no come to conclusion when used
        self.tk_event.serial = 42

        # num - mouse button pressed (ButtonPress, ButtonRelease)
        if type(self.qt_event) == QMouseEvent:
            self.tk_event.num = mouse_button_translator(self.qt_event.button(),
                                                        from_tk=False)
        else:
            self.tk_event.num = "??"

        # focus - whether the window has the focus (Enter, Leave)
        if type(self.qt_event) == QFocusEvent:
            self.tk_event.focus = self.qt_event.gotFocus()
        else:
            pass
            # Decided to pass this since it is not set usually.

        # height - height of the exposed window (Configure, Expose)
        # width - width of the exposed window (Configure, Expose)
        self.tk_event.height = "??"  # Set as "default"
        self.tk_event.width = "??"  # Set as "default"

        # keycode - keycode of the pressed key (KeyPress, KeyRelease)
        if type(self.qt_event) == QKeyEvent:
            # TODO: This need translation !!!
            self.tk_event.keycode = self.qt_event.key()
        else:
            self.tk_event.keycode = "??"

        # state - state of the event as a number (ButtonPress, ButtonRelease,
        #                         Enter, KeyPress, KeyRelease,
        #                         Leave, Motion)
        # state - state as a string (Visibility)
        if type(self.qt_event) in [QMouseEvent, QKeyEvent, QEnterEvent]:
            # TODO: This need translation !!!
            self.tk_event.state = self.qt_event.type()
            # TODO: + self.qt_event.modifiers()
            # TODO: No translation for Motion, Visibility
        else:
            self.tk_event.state = "??"

        # time - when the event occurred - only successors of QInputEvent
        if issubclass(type(self.qt_event), QInputEvent):
            self.tk_event.time = self.qt_event.timestamp()
        else:
            self.tk_event.time = "??"

        # x - x-position of the mouse
        # y - y-position of the mouse
        if type(self.qt_event) in [QMouseEvent, QEnterEvent]:
            self.tk_event.x = self.qt_event.x()
            self.tk_event.y = self.qt_event.y()
        else:
            self.tk_event.x = "??"
            self.tk_event.y = "??"

        # x_root - x-position of the mouse on the screen
        #          (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)
        # y_root - y-position of the mouse on the screen
        #          (ButtonPress, ButtonRelease, KeyPress, KeyRelease, Motion)
        if type(self.qt_event) in [QMouseEvent]:
            self.tk_event.x_root = self.qt_event.screenPos().x()
            self.tk_event.y_root = self.qt_event.screenPos().y()
            # TODO: No translation for Motion
            # QKeyEvent does not have this
        else:
            self.tk_event.x_root = "??"
            self.tk_event.y_root = "??"

        # char - pressed character (KeyPress, KeyRelease)
        if type(self.qt_event) == QKeyEvent:
            # TODO: This need translation !!!
            self.tk_event.char = self.qt_event.text()
        else:
            self.tk_event.char = "??"

        # send_event - see X/Windows documentation
        # TODO: see X/Windows documentation
        self.tk_event.send_event = False

        # keysym - keysym of the event as a string (KeyPress, KeyRelease)
        # keysym_num - keysym of the event as a number (KeyPress, KeyRelease)
        if type(self.qt_event) == QKeyEvent:
            # TODO: This need translation !!!
            self.tk_event.keysym = self.qt_event.text()
            self.tk_event.keysym_num = ord(self.qt_event.text())
        else:
            self.tk_event.keysym = "??"
            self.tk_event.keysym_num = "??"

        # type - type of the event as a number
        # TODO: This need translation !!!
        self.tk_event.type = self.qt_event.type()

        # widget - widget in which the event occurred
        # TODO: There is no way to get this in PyQt?

        # delta - delta of wheel movement (MouseWheel)
        if type(self.qt_event) == QWheelEvent:
            self.tk_event.delta = self.qt_event.angleDelta()
        else:
            self.tk_event.delta = 0

        return self.tk_event
