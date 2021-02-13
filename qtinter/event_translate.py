"""
This file contains support functions to translate attributes and names
used when working with events. Since it is needed when assigning binding,
when Qt event occurs, when binding is checked, when Qt event is translated
to Tk event, it has multiple usage.

Functions:
- key_translator - Translates QtKey to TkKey. Note that this translation is
                   only made with ascii comparison, which should be accurate
                   for most of usual keys, according to source. Also note
                   that PyQt events does not provide if key was capital or not.
- mouse_button_translator - Translates QtMouseButton to TkMouseButton
                            or other way.
- sequence_parser - Parses Tkinter sequence to more readable and unified dict.
- tk_modifier_to_qt - Takes tk_modifier and translates it to Qt Modifier.
                      Note that not every modifier from Tk has corresponding
                      modifier in Qt. But for instance Double modifier could be
                      interpreted as special type of event which has own
                      method/slot in QWidget. This could be done with
                      modification of get_method_for_type fucntion. TODO
- get_method_for_type - Resolves event_type from Tkinter name to PyQt widget
                        method. Note that many Tk events does not have
                        corresponding Qt QWidgets slot or other way.

Each of these functions has "settings" dicts in their definition.
Note that content of these dicts could be moved
to some unified settings of this project. TODO

Note that there are still needed translations from event_builder file: TODO
- self.tk_event.state = self.qt_event.type()
- self.tk_event.keysym = self.qt_event.text()
- self.tk_event.char = self.qt_event.text()
- self.tk_event.type = self.qt_event.type()

Note that there could be one unified function to resolve those parameters
mappings and missing values. TODO
"""
import sys

from PyQt5.QtCore import Qt


def key_translator(qt_key):
    """Translates QtKey to TkKey."""

    # Sources:
    # Tk: http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    # Qt: https://doc.bccnsoft.com/docs/PyQt4/qt.html#Key-enum

    # According to sources, key values should be the same/similar
    value = int(qt_key)
    return value


def mouse_button_translator(mouse_button, from_tk=True):
    """Translates QtMouseButton to TkMouseButton or other way."""

    # MouseButton: https://doc.bccnsoft.com/docs/PyQt4/qt.html#MouseButton-enum

    mouse_button_switch_from_tk = {
        1: Qt.LeftButton,
        2: Qt.MidButton,
        3: Qt.RightButton,
    }

    mouse_button_switch_from_qt = {
        1: 1,
        2: 3,
        4: 2,
    }

    if from_tk:
        return mouse_button_switch_from_tk[int(mouse_button)]
    else:
        return mouse_button_switch_from_qt[int(mouse_button)]


def sequence_parser(sequence):
    """Parses Tkinter sequence to more readable and unified dict."""

    # Possibilities:
    # <MODIFIER-MODIFIER-TYPE-DETAIL>
    # <MODIFIER-TYPE-DETAIL>
    # <TYPE-DETAIL>
    # <DETAIL> -> Either number or Character so this translates to:
    #   '<1>' is the same as '<Button-1>'.
    #   'x' is the same as '<KeyPress-x>'.

    sequence = sequence.replace('<', '')
    sequence = sequence.replace('>', '')
    # Split sequence and revert list so we go from right to left.
    sequence_split = sequence.split('-')
    sequence_split.reverse()

    # Setup return dict
    parsed = {
        "Detail": None,
        "Type": None,
        "Mod2": None,
        "Mod1": None,
    }

    # Iterate through keys and sequence
    iteration_counter = 0
    for key in parsed:
        if iteration_counter < len(sequence_split):
            parsed[key] = sequence_split[iteration_counter]
            iteration_counter += 1
        else:
            break

    if len(sequence_split) == 1:
        if sequence_split[0].isnumeric():
            parsed["Type"] = "Button"
        elif sequence_split[0] == "Enter":
            parsed["Type"] = "Enter"
        elif sequence_split[0] == "Key":  # Means all keys
            parsed["Type"] = "KeyPress"
            parsed["Detail"] = ""
        else:
            parsed["Type"] = "KeyPress"

    if parsed["Type"] == "Button":
        parsed["Detail"] = mouse_button_translator(parsed["Detail"])

    return parsed


def tk_modifier_to_qt(tk_modifier):
    """Takes tk_modifier and translates it to Qt Modifier."""

    # Modifier:
    # https://doc.bccnsoft.com/docs/PyQt4/qt.html#KeyboardModifier-enum

    qt_modifiers = {
        "Alt": Qt.AltModifier,
        "Any": None,
        "Control": Qt.ControlModifier,
        "Double": None,
        "Lock": None,
        "Shift": Qt.ShiftModifier,
        "Triple": None,
    }

    # Not implemented Qt modifiers:
    # Qt.NoModifier, Qt.MetaModifier, Qt.KeypadModifier, Qt.GroupSwitchModifier

    if tk_modifier not in qt_modifiers:
        print("Warning, tk modifier", tk_modifier,
              "not found in translate dict",
              file=sys.stderr)

    if qt_modifiers[tk_modifier] is None:
        print("Warning, event method for", type, "not set.",
              file=sys.stderr)
    else:
        return qt_modifiers[tk_modifier]


def get_method_for_type(event_type):
    """Resolves event_type from Tkinter name to PyQt widget method."""

    event_type_switch = {
        "Activate": None,
        "Button": "mousePressEvent",
        "ButtonPress": "mousePressEvent",  # Same as Button
        "ButtonRelease": "mouseReleaseEvent",
        "Configure": None,
        "Deactivate": None,
        "Destroy": None,
        "Enter": "enterEvent",
        "Expose": None,
        "FocusIn": "focusInEvent",
        "FocusOut": "focusOutEvent",
        "Key": "keyPressEvent",
        "KeyPress": "keyPressEvent",  # Same as Key
        "KeyRelease": "keyReleaseEvent",
        "Leave": "leaveEvent",
        "Map": None,
        "Motion": "mouseMoveEvent",
        "MouseWheel": "wheelEvent",
        "Unmap": None,
        "Visibility": None,
    }

    # Source: https://doc.qt.io/qt-5/qwidget.html
    # Not implemented / connected
    # actionEvent(QActionEvent *event)
    # changeEvent(QEvent *event)
    # closeEvent(QCloseEvent *event)
    # contextMenuEvent(QContextMenuEvent *event)
    # dragEnterEvent(QDragEnterEvent *event)
    # dragLeaveEvent(QDragLeaveEvent *event)
    # dragMoveEvent(QDragMoveEvent *event)
    # dropEvent(QDropEvent *event)
    # hideEvent(QHideEvent *event)
    # inputMethodEvent(QInputMethodEvent *event)
    # mouseDoubleClickEvent(QMouseEvent *event)
    # moveEvent(QMoveEvent *event)
    # paintEvent(QPaintEvent *event)
    # resizeEvent(QResizeEvent *event)
    # showEvent(QShowEvent *event)
    # tabletEvent(QTabletEvent *event)

    if event_type not in event_type_switch:
        print("Warning, event type", event_type, "not found in sequence",
              file=sys.stderr)

    if event_type_switch[event_type] is None:
        print("Warning, event method for", event_type, "not set.",
              file=sys.stderr)
    else:
        return event_type_switch[event_type]
