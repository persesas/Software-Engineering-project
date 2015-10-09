from PyQt5 import QtWidgets


class Base(QtWidgets.QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 800, 600)

        # Initialize widgets
        dpt_label = QtWidgets.QLabel('Blablablaa Department')
        user_label = QtWidgets.QLabel('Logged in as: {}'.format(self.username))

        # Initialize top layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(dpt_label)
        top_layout.addStretch(1)
        top_layout.addWidget(user_label)

        # Initialize main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(top_layout)
        self.setLayout(self.main_layout)
        self.show()

    def set_central_widget(self, widget):
        self.main_layout.addWidget(widget)
        self.update()
