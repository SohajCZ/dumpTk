from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

class SimpleWindow(QWidget):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    wind = SimpleWindow()
    wind.resize(200,100)
    wind.move(50,150)
    wind.show()

    sys.exit(app.exec_())
