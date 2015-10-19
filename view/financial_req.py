from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from view.timed_label import BlinkLabel


class FinancialReq(QtWidgets.QWidget):
    def __init__(self, event_ids):
        super().__init__()

        self.event_ids = event_ids
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 350, 420)

        # Initialize widgets
        title_label = QtWidgets.QLabel('Financial Request')

        group_box = QtWidgets.QGroupBox('Requesting Departement :')
        administration_button = QtWidgets.QRadioButton('Administration')
        services_button = QtWidgets.QRadioButton('Services')
        production_button = QtWidgets.QRadioButton('Production')
        financial_button = QtWidgets.QRadioButton('Financial')

        submit_button = QtWidgets.QPushButton('Submit')
        submit_button.clicked.connect(self.onSubmit)
        project_ref_label = QtWidgets.QLabel('Project reference :')
        self.event_id_edit = QtWidgets.QComboBox()
        self.event_id_edit.setEditable(False)
        self.event_id_edit.addItems(self.event_ids)
        required_amount_label = QtWidgets.QLabel('Required amount :')
        self.required_amount_edit = QtWidgets.QLineEdit()
        reason_label = QtWidgets.QLabel('Reason :')
        self.reason_edit = QtWidgets.QTextEdit()


        # Initialize layouts
        grid_box = QtWidgets.QGridLayout()
        grid_box.addWidget(administration_button, 0, 0)
        grid_box.addWidget(services_button, 0, 1)
        grid_box.addWidget(production_button, 1, 0)
        grid_box.addWidget(financial_button, 1, 1)
        group_box.setLayout(grid_box)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(project_ref_label, 0, 0)
        grid.addWidget(self.event_id_edit, 0, 1)
        grid.addWidget(required_amount_label, 1, 0)
        grid.addWidget(self.required_amount_edit, 1, 1)
        grid.addWidget(reason_label, 2, 0)
        grid.addWidget(self.reason_edit, 2, 1)

        extras_layout = QtWidgets.QHBoxLayout()
        self.blink_label = BlinkLabel('Request submitted')
        extras_layout.addWidget(self.blink_label)
        extras_layout.setAlignment(self.blink_label, Qt.AlignRight)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addWidget(group_box)
        main_layout.addLayout(grid)
        main_layout.addWidget(submit_button)
        main_layout.addLayout(extras_layout)
        main_layout.setAlignment(title_label, Qt.AlignHCenter)

        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        if self.isInputValid():
            self.blink_label.setText('Request submitted')
        else:
            self.blink_label.setText('Empty fields')
        self.blink_label.start(2000)

    def isInputValid(self):
        return self.required_amount_edit.text() != '' and self.reason_edit.toPlainText() != ''
