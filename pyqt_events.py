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

    def catch_event_escape(self, e):
        print("shift escape catch")


def call_if(key, modifiers, method, *arg):
    or_modifier = 0
    for modifier in modifiers:
        or_modifier |= modifier

    if issubclass(type(*arg), QEvent):
        event = arg[0]
        if event.key() == key and event.modifiers() == or_modifier:
            method(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    # Mouse click binding example
    ex.mousePressEvent = ex.catch_event
    # Specific key binding example
    ex.keyPressEvent = lambda e: call_if(Qt.Key_Escape, [Qt.ShiftModifier],
                                         ex.catch_event_escape, e)
    sys.exit(app.exec_())
