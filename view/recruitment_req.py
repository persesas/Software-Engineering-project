
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.timed_label import BlinkLabel


class RecruitmentReq(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.setGeometry(500, 200, 350, 420)

        # Initialize widgets
        title_label = QtWidgets.QLabel('Recruitment request')
        years_of_exp_label = QtWidgets.QLabel('Years of experience :')
        job_title_label = QtWidgets.QLabel('Job title')
        job_description_label = QtWidgets.QLabel('Job description :')

        years_of_exp_edit = QtWidgets.QLineEdit()
        job_title_edit = QtWidgets.QLineEdit()
        job_description_edit= QtWidgets.QTextEdit()

        full_time_button = QtWidgets.QRadioButton('Full time')
        part_time_button = administration_button = QtWidgets.QRadioButton('Part time')
        administration_button = QtWidgets.QRadioButton('Administration')
        services_button = QtWidgets.QRadioButton('Services')
        production_button = QtWidgets.QRadioButton('Production')
        financial_button = QtWidgets.QRadioButton('Financial')

        submit_button = QtWidgets.QPushButton("Submit")
        submit_button.clicked.connect(self.onSubmit)

        #Initialize layouts
        grid_layout_dpt = QtWidgets.QGridLayout()
        grid_layout_dpt.addWidget(administration_button, 0, 0)
        grid_layout_dpt.addWidget(services_button, 0, 1)
        grid_layout_dpt.addWidget(production_button, 1, 0)
        grid_layout_dpt.addWidget(financial_button, 1, 1)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(years_of_exp_label, 2, 0)
        grid_layout.addWidget(years_of_exp_edit, 2, 1)
        grid_layout.addWidget(job_title_label, 3, 0)
        grid_layout.addWidget(job_title_edit, 3, 1)
        grid_layout.addWidget(job_description_label, 4, 0)
        grid_layout.addWidget(job_description_edit, 4, 1)

        contract_layout = QtWidgets.QHBoxLayout()
        type_button_group = QtWidgets.QGroupBox("Contract type :")

        contract_layout.addWidget(full_time_button)
        contract_layout.addWidget(part_time_button)
        type_button_group.setLayout(contract_layout)

        dpt_button_group = QtWidgets.QGroupBox("Requesting department :")
        dpt_button_group.setLayout(grid_layout_dpt)

        extras_layout = QtWidgets.QHBoxLayout()
        self.blink_label = BlinkLabel('Request submitted')
        extras_layout.addWidget(self.blink_label)
        extras_layout.setAlignment(self.blink_label, Qt.AlignRight)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.setAlignment(title_label, Qt.AlignHCenter)
        main_layout.addWidget(type_button_group)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(dpt_button_group)
        main_layout.addWidget(submit_button)
        main_layout.addLayout(extras_layout)
        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        self.blink_label.start(2000)