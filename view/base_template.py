from PyQt5 import QtWidgets


class Base(QtWidgets.QWidget):
    def __init__(self, username, department):
        super().__init__()

        self.username = username
        self.department = department

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 800, 600)

        # Initialize widgets
        menu_bar = self._create_menu_bar()

        dpt_label = QtWidgets.QLabel(self.department)
        user_label = QtWidgets.QLabel('Logged in as: {}'.format(self.username))

        # Initialize top layout
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(dpt_label)
        top_layout.addStretch(1)
        top_layout.addWidget(user_label)

        # Initialize main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(menu_bar)
        self.main_layout.addLayout(top_layout)
        self.setLayout(self.main_layout)
        self.show()

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

    def set_central_widget(self, widget):
        self.main_layout.addWidget(widget)
        self.update()
