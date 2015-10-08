import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class EventPlanningReq(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 350, 420)

        # Initialize widgets
        title = QtWidgets.QLabel('Request for Event Planning')
        rec_no_label = QtWidgets.QLabel('Record number :')
        client_name_label = QtWidgets.QLabel('Client name :')
        event_type_label = QtWidgets.QLabel('Event type :')
        from_date_label = QtWidgets.QLabel('From:')
        to_date_label = QtWidgets.QLabel('To :')
        exp_no_attendees_label = QtWidgets.QLabel('Expected number of attendees: ')
        exp_budget_label = QtWidgets.QLabel('Expected budget :')

        rec_no_edit = QtWidgets.QLineEdit()
        client_name_edit = QtWidgets.QLineEdit()
        event_type_edit = QtWidgets.QLineEdit()
        exp_no_attendees_edit = QtWidgets.QLineEdit()
        exp_budget_edit = QtWidgets.QLineEdit()

        group_box = QtWidgets.QGroupBox('Preferences :')

        decorations_check = QtWidgets.QCheckBox('Decorations')
        parties_check = QtWidgets.QCheckBox('Parties')
        photos_check = QtWidgets.QCheckBox('Photos/fimling')
        breakfast_check = QtWidgets.QCheckBox('Breakfast')
        drinks_check = QtWidgets.QCheckBox('Soft/hot drinks')

        from_date = QtWidgets.QDateEdit(datetime.date.today())
        to_date = QtWidgets.QDateEdit(datetime.date.today())

        submit_button = QtWidgets.QPushButton('Submit')

        # Add widgets to layout

        date_from_layout = QtWidgets.QHBoxLayout()
        date_from_layout.addWidget(from_date_label)
        date_from_layout.addWidget(from_date)

        date_to_layout = QtWidgets.QHBoxLayout()
        date_to_layout.addWidget(to_date_label)
        date_to_layout.addWidget(to_date)

        grid_group_box = QtWidgets.QGridLayout()
        grid_group_box.addWidget(decorations_check, 0, 0)
        grid_group_box.addWidget(breakfast_check, 0, 1)
        grid_group_box.addWidget(parties_check, 1, 0)
        grid_group_box.addWidget(drinks_check, 1, 1)
        grid_group_box.addWidget(photos_check, 2, 0)

        group_box.setLayout(grid_group_box)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(rec_no_label, 0, 0)
        grid.addWidget(rec_no_edit, 0, 1)
        grid.addWidget(client_name_label, 1, 0)
        grid.addWidget(client_name_edit, 1, 1)
        grid.addWidget(event_type_label, 2, 0)
        grid.addWidget(event_type_edit, 2, 1)
        grid.addLayout(date_from_layout, 3, 0)
        grid.addLayout(date_to_layout, 3, 1)
        grid.addWidget(exp_no_attendees_label, 4, 0)
        grid.addWidget(exp_no_attendees_edit, 4, 1)
        grid.addWidget(exp_budget_label, 5, 0)
        grid.addWidget(exp_budget_edit, 5, 1)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addWidget(group_box)
        main_layout.addWidget(submit_button)
        main_layout.setAlignment(title, Qt.AlignHCenter)

        self.setLayout(main_layout)
        self.show()
