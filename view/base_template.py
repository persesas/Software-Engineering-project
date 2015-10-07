__author__ = 'anon'

from PyQt5 import QtWidgets


class Base(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        from view import mediator as med
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 800, 600)

        # Initialize widgets
        dpt_label = QtWidgets.QLabel('Department : ')
        user_label = QtWidgets.QLabel('user:')

        # Initialize top layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(dpt_label)
        top_layout.addStretch(1)
        top_layout.addWidget(user_label)

        # Initialize main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(top_layout)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)
        self.show()

    def set_central_widget(self, widget):
        self.main_layout.addWidget(widget)
        self.update()
