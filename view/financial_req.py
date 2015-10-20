from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from view.timed_label import BlinkLabel


class FinancialReq(QtWidgets.QWidget):
    def __init__(self, empl_type, event_ids, data=None):
        super().__init__()
        self.data = data
        self.empl_type = empl_type
        self.event_ids = event_ids
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 350, 420)

        # Initialize widgets
        title_label = QtWidgets.QLabel('Financial Request')

        group_box = QtWidgets.QGroupBox('Requesting Departement :')
        self.administration_button = QtWidgets.QRadioButton('Administration')
        self.services_button = QtWidgets.QRadioButton('Services')
        self.production_button = QtWidgets.QRadioButton('Production')

        self.administration_button.setEnabled(False)
        self.services_button.setEnabled(False)
        self.production_button.setEnabled(False)

        if self.empl_type == 'administration':
            self.administration_button.setChecked(True)
        elif self.empl_type == 'production':
            self.production_button.setChecked(True)
        elif self.empl_type == 'service':
            self.services_button.setChecked(True)

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
        grid_box.addWidget(self.administration_button, 0, 0)
        grid_box.addWidget(self.services_button, 0, 1)
        grid_box.addWidget(self.production_button, 1, 0)
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

        if self.data: self._populate()
        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        from view.mediator import get_mediator
        m = get_mediator()
        if self.isInputValid():
            if not self.data:
                if self.administration_button.isChecked():
                    m.create_financial_req(self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'administration')
                elif self.production_button.isChecked():
                    m.create_financial_req(self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'production')
                else:
                    m.create_financial_req(self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'service')

                self.blink_label.setText('Request submitted')

                self.clear_form()
                self.blink_label.start(2000)
            else:
                if self.administration_button.isChecked():
                    m.update_financial_req(self.data['id'], self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'administration')
                elif self.production_button.isChecked():
                    m.update_financial_req(self.data['id'], self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'production')
                else :
                    m.update_financial_req(self.data['id'], self.event_id_edit.currentText(), self.required_amount_edit.text(),
                                           self.reason_edit.toPlainText(), 'service')
                self.hide()


        else:
            self.blink_label.setText('Empty fields')
            self.blink_label.start(2000)

    def isInputValid(self):
        return self.required_amount_edit.text() != '' and self.reason_edit.toPlainText() != ''

    def _populate(self):
        self.required_amount_edit.setText(self.data['req_amount'])
        self.reason_edit.setText(self.data['reason'])
        i = self.event_id_edit.findText(self.data['event_id'])
        self.event_id_edit.setCurrentIndex(i)
        req_dpt = self.data['req_dpt']
        if req_dpt == 'administration':
            self.administration_button.setChecked(True)
        elif req_dpt == 'production':
            self.production_button.setChecked(True)
        else :
            self.services_button.setChecked(True)


    def clear_form(self):
        self.required_amount_edit.clear()
        self.reason_edit.clear()
