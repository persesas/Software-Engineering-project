from PyQt5 import QtWidgets


class TaskReq(QtWidgets.QWidget):
    def __init__(self, event_ids, staff_names, sub_teams):
        super().__init__()
        self.event_ids = event_ids
        self.staff_names_ids = staff_names
        self.sub_teams = sub_teams
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 850, 420)

        self.event_id_edit = QtWidgets.QComboBox()
        self.event_id_edit.setEditable(False)
        # self.event_id_edit.addItems(self.event_ids.keys())

        self.staff_name_edit = QtWidgets.QComboBox()
        self.staff_name_edit.setEditable(False)
        # self.staff_name_edit.addItems(self.staff_names.keys())

        self.sub_teams_edit = QtWidgets.QComboBox()
        self.sub_teams_edit.setEditable(False)
        # self.sub_teams_edit.addItems(self.sub_teams.keys())

        project_ref_label = QtWidgets.QLabel("Project Reference:")
        description_label = QtWidgets.QLabel("Description:")
        self.description_edit = QtWidgets.QTextEdit()
        assign_to_label = QtWidgets.QLabel("Assign to:")
        priority_label = QtWidgets.QLabel("Priority:")
        self.priority_edit = QtWidgets.QComboBox()
        self.priority_edit.setEditable(False)
        self.priority_edit.addItem("High")
        self.priority_edit.addItem("Medium")
        self.priority_edit.addItem("Low")
        send_task = QtWidgets.QPushButton("Send Task")
        send_task.clicked.connect(self.onSubmit)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(project_ref_label, 0, 0)
        grid.addWidget(self.event_id_edit, 0, 1)
        grid.addWidget(description_label, 1, 0)
        grid.addWidget(self.description_edit, 1, 1)
        grid.addWidget(assign_to_label, 2, 0)
        grid.addWidget(self.staff_name_edit, 2, 1)
        grid.addWidget(priority_label, 3, 0)
        grid.addWidget(self.priority_edit, 3, 1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.sub_teams_edit)
        main_layout.addLayout(grid)
        main_layout.addWidget(send_task)
        self.setLayout(main_layout)
        self.show()

    def onSubmit(self):
        from view.mediator import get_mediator
        m = get_mediator()
        m.create_task(self.sub_teams_edit.currentText(), self.event_id_edit.currentText(),
                      self.description_edit.toPlainText(), self.staff_name_edit.currentText(),
                      self.priority_edit.currentText())
