__author__ = 'anon'

from PyQt5 import QtWidgets


#TODO no user
#TODO handle wrong values
class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 120)

        # Initialize widgets

        title = QtWidgets.QLabel('Welcome to SEP')

        username = QtWidgets.QLabel('username :')
        password = QtWidgets.QLabel('password :')

        self.wrong_login = QtWidgets.QLabel('(Invalid user/password)')
        self.wrong_login.setVisible(False)

        self.userEdit = QtWidgets.QLineEdit("e1")
        self.userEdit.returnPressed.connect(self.onLogin)

        self.passwordEdit = QtWidgets.QLineEdit("12345")
        self.passwordEdit.returnPressed.connect(self.onLogin)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        loginButton = QtWidgets.QPushButton("Login")
        loginButton.clicked.connect(self.onLogin)


        # Add widgets to layout
        grid = QtWidgets.QGridLayout()

        grid.addWidget(title, 1, 0)
        grid.addWidget(self.wrong_login, 1, 1)

        grid.addWidget(username, 2, 0)
        grid.addWidget(self.userEdit, 2, 1)

        grid.addWidget(password, 3, 0)
        grid.addWidget(self.passwordEdit, 3, 1)

        grid.addWidget(loginButton, 4, 1)
        self.setLayout(grid)

        self.show()

    def closeEvent(self, e):
        QtWidgets.QApplication.quit()

    def onLogin(self):
        from view.mediator import get_mediator
        m = get_mediator()

        if not m.check_credentials(self.userEdit.text(), self.passwordEdit.text()):
            self.wrong_login.setVisible(True)
        else:
            m.login(self.userEdit.text())
            self.hide()
