import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QEvent


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('PyQt events with keyboard')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            print("clicked escape")

    def catch_event(self, e):
        print("mouse catch")

    def catch_event_shift_escape(self, e):
        print("shift escape catch")

    def catch_event_escape(self, e):
        print("escape catch")

    def catch_event_a(self, e):
        print("a catch")


def call_if(bindings, event):
    for binding in bindings:
        or_modifier = 0
        for modifier in binding[1]:
            or_modifier |= modifier

        if issubclass(type(event), QEvent):
            if event.key() == binding[0] and \
                    int(event.modifiers()) == int(or_modifier):
                binding[2](event)
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # Mouse click binding example
    ex.mousePressEvent = ex.catch_event
    # Specific key binding example
    bindings = {}
    bindings["Example"] = []
    # Structure: key: name from "namer", value: array
    # of tuples: (Key, Modifiers, Method to call)
    bindings["Example"].append((Qt.Key_Escape, [Qt.ShiftModifier],
                                ex.catch_event_shift_escape))
    bindings["Example"].append((Qt.Key_Escape, [],
                                ex.catch_event_escape))
    bindings["Example"].append((Qt.Key_A, [], ex.catch_event_a))

    ex.keyPressEvent = lambda event: call_if(bindings["Example"], event)
    sys.exit(app.exec_())
