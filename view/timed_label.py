import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class BlinkLabel(QtWidgets.QLabel):
    def __init__(self, text):
        super().__init__(text)

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)

        self.setVisible(False)

    def start(self, time):
        self.timer.start(time)
        self.show()

    def onTimeout(self):
        self.hide()
