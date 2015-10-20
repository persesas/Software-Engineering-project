from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.timed_label import BlinkLabel


class RecruitmentReq(QtWidgets.QWidget):
    def __init__(self, empl_type, data=None):
        super().__init__()
        self.empl_type = empl_type
        self.data = data
        self.initUI()

    def initUI(self):

        # Initialize widgets
        title_label = QtWidgets.QLabel('Recruitment request')
        years_of_exp_label = QtWidgets.QLabel('Years of experience :')
        job_title_label = QtWidgets.QLabel('Job title')
        job_description_label = QtWidgets.QLabel('Job description :')

        self.years_of_exp_edit = QtWidgets.QLineEdit()
        self.job_title_edit = QtWidgets.QLineEdit()
        self.job_description_edit = QtWidgets.QTextEdit()

        self.full_time_button = QtWidgets.QRadioButton('Full time')
        self.part_time_button = QtWidgets.QRadioButton('Part time')

        self.administration_button = QtWidgets.QRadioButton('Administration')
        self.services_button = QtWidgets.QRadioButton('Services')
        self.production_button = QtWidgets.QRadioButton('Production')
        self.financial_button = QtWidgets.QRadioButton('Financial')

        self.administration_button.setEnabled(False)
        self.services_button.setEnabled(False)
        self.production_button.setEnabled(False)
        self.financial_button.setEnabled(False)

        if self.empl_type == 'administration':
            self.administration_button.setChecked(True)
        elif self.empl_type == 'service':
            self.services_button.setChecked(True)
        elif self.empl_type == 'production':
            self.production_button.setChecked(True)
        elif self.empl_type == 'financial':
            self.financial_button.setChecked(True)


        submit_button = QtWidgets.QPushButton("Submit")
        submit_button.clicked.connect(self.onSubmit)

        # Initialize layouts
        grid_layout_dpt = QtWidgets.QGridLayout()
        grid_layout_dpt.addWidget(self.administration_button, 0, 0)
        grid_layout_dpt.addWidget(self.services_button, 0, 1)
        grid_layout_dpt.addWidget(self.production_button, 1, 0)
        grid_layout_dpt.addWidget(self.financial_button, 1, 1)

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(years_of_exp_label, 2, 0)
        grid_layout.addWidget(self.years_of_exp_edit, 2, 1)
        grid_layout.addWidget(job_title_label, 3, 0)
        grid_layout.addWidget(self.job_title_edit, 3, 1)
        grid_layout.addWidget(job_description_label, 4, 0)
        grid_layout.addWidget(self.job_description_edit, 4, 1)

        contract_layout = QtWidgets.QHBoxLayout()
        type_button_group = QtWidgets.QGroupBox("Contract type :")

        contract_layout.addWidget(self.full_time_button)
        contract_layout.addWidget(self.part_time_button)
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
        if self.data: self._populate()
        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        from view.mediator import get_mediator
        m = get_mediator()
        if self.full_time_button.isChecked():
            self.type = 'full time'
        elif self.part_time_button.isChecked():
            self.type = 'part time'
        else:
            self.type = ''
        if self.isInputValid():
            if not self.data:
                m.create_recruitment_req(self.type, self.years_of_exp_edit.text(), self.job_title_edit.text(),
                                         self.job_description_edit.toPlainText(), self.empl_type)
                self.blink_label.setText('Request submitted')

                self.clear_form()
                self.blink_label.start(2000)
            else:
                m.update_recruitment_req(self.data['id'], self.type, self.years_of_exp_edit.text(),
                                   self.job_title_edit.text(),
                                   self.job_description_edit.toPlainText(), self.empl_type)
                self.hide()
        else:
            self.blink_label.setText('Empty field(s)')
            self.blink_label.start(2000)

    def isInputValid(self):
        return self.job_description_edit.toPlainText() != '' and self.job_title_edit.text() != '' \
               and self.years_of_exp_edit.text() != ''

    def _populate(self):
        contract_type = self.data['type']
        dpt_req = self.data['req_dpt']

        self.years_of_exp_edit.setText(self.data['years_exp'])
        self.job_title_edit.setText(self.data['title'])
        self.job_description_edit.setText(self.data['description'])

        if contract_type == 'full time':
            self.full_time_button.setChecked(True)
        elif contract_type == 'part time':
            self.part_time_button.setChecked(True)

        if dpt_req == 'administration':
            self.administration_button.setChecked(True)
            if self.data: self.empl_type = 'administration'
        elif dpt_req == 'production':
            self.production_button.setChecked(True)
            if self.data: self.empl_type = 'production'
        elif dpt_req == 'service':
            self.services_button.setChecked(True)
            if self.data: self.empl_type = 'service'
        else:
            self.financial_button.setChecked(True)
            if self.data: self.empl_type = 'financial'

    def clear_form(self):
        self.years_of_exp_edit.clear()
        self.job_title_edit.clear()
        self.job_description_edit.clear()
