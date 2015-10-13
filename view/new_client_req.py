import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class NewClientReq(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 450, 420)

        title_label = QtWidgets.QLabel('New Client request :')
        name_label = QtWidgets.QLabel('Name :')
        self.name_edit = QtWidgets.QLineEdit()
        age_label = QtWidgets.QLabel('Age :')
        self.age_edit = QtWidgets.QLineEdit()
        address_label = QtWidgets.QLabel('Address :')
        self.address_edit = QtWidgets.QTextEdit()
        mail_label = QtWidgets.QLabel('Email :')
        self.mail_edit = QtWidgets.QLineEdit()
        phone_label = QtWidgets.QLabel('Phone :')
        self.phone_edit = QtWidgets.QLineEdit()
        submit_button = QtWidgets.QPushButton('Submit')
        submit_button.clicked.connect(self.onSubmit)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)
        grid.addWidget(age_label, 1, 0)
        grid.addWidget(self.age_edit, 1, 1)
        grid.addWidget(address_label, 2, 0)
        grid.addWidget(self.address_edit, 2, 1)
        grid.addWidget(mail_label, 3, 0)
        grid.addWidget(self.mail_edit, 3, 1)
        grid.addWidget(phone_label, 4, 0)
        grid.addWidget(self.phone_edit, 4, 1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(grid)
        main_layout.addWidget(submit_button)
        main_layout.setAlignment(title_label, Qt.AlignHCenter)
        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        from view.mediator import get_mediator
        m = get_mediator()
        m.create_client(self.name_edit, self.age_edit, self.address_edit, self.mail_edit, self.phone_edit)
