from PyQt5 import QtWidgets


class Base(QtWidgets.QWidget):
    def __init__(self, name, department, username):
        super().__init__()

        self.name = name
        self.department = department
        self.username = username

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 800, 600)

        # Initialize widgets
        menu_bar = self._create_menu_bar()

        dpt_label = QtWidgets.QLabel(self.department)
        user_label = QtWidgets.QLabel('Logged in as: {}'.format(self.name))

        logout_btn = QtWidgets.QPushButton('Logout')
        logout_btn.clicked.connect(self.onLogout)

        refresh_btn = QtWidgets.QPushButton('Refresh')
        refresh_btn.clicked.connect(self.onRefresh)

        # Initialize top layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(dpt_label)
        top_layout.addStretch(1)
        top_layout.addWidget(user_label)
        top_layout.addWidget(refresh_btn)
        top_layout.addWidget(logout_btn)

        # Initialize main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(menu_bar)
        self.main_layout.addLayout(top_layout)
        self.setLayout(self.main_layout)
        self.center()
        self.show()

    def closeEvent(self, e):
        QtWidgets.QApplication.quit()

    def _create_menu_bar(self):
        # The empty bar
        menu_bar = QtWidgets.QMenuBar(self)
        # Entries
        file_menu = menu_bar.addMenu('File')
        # Actions
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        # Add them
        file_menu.addAction(exit_action)

        return menu_bar

    def onLogout(self):
        from view.mediator import get_mediator
        m = get_mediator()
        m.logout()

        self.destroy()

    def onRefresh(self):
        from view.mediator import get_mediator
        m = get_mediator()
        m.login(self.username)

        self.destroy()

    def set_central_widget(self, widget):
        self.main_layout.addWidget(widget)
        self.update()

    def center(self):
        appRect = self.frameGeometry()
        clientArea = QtWidgets.QDesktopWidget().availableGeometry().center()
        appRect.moveCenter(clientArea)
        self.move(appRect.topLeft())
