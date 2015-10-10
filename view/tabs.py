from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class ManagerTabs(QtWidgets.QWidget):

    clients = 'Clients'
    employees = 'Employees'
    events = 'Events'
    tasks = 'Tasks'

    def __init__(self, empl_type):
        super().__init__()

        self.initUI()
        getattr(self, '_show_{}'.format(empl_type))()

    def initUI(self):
        # Initialize tab widgets
        self.tabs = QtWidgets.QTabWidget()

        self.employee_tab = self._create_employee_tab()
        self.client_tab = self._create_client_tab()
        self.event_tab = self._create_event_tab()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)

    # Create everything...
    def _create_employee_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        empl_table = self._create_table(m.get_employee())

        return empl_table

    def _create_client_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        client_table = self._create_table(m.get_client())

        return client_table

    def _create_event_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        event_table = self._create_table(m.get_event())

        return event_table

    # ...and hide what we dont want to show.
    def _show_cstm_srvc(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)

        self.show()

    def _show_snr_cs_offcr(self):
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_hr(self):
        self.tabs.addTab(self.employee_tab, self.employees)

        self.show()

    def _show_admin(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_fncl(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)

        self.show()

    def _show_prod(self):
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_srvc(self):
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_vp(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _create_table(self, data):
        table = QtWidgets.QTableWidget()

        if data:
            horHeaders = list(data[0].keys())
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            table.setRowCount(len(data))
            table.setColumnCount(len(horHeaders))

            flags = Qt.NoItemFlags | Qt.ItemIsEnabled

            for n, row in enumerate(data):
                # for every row
                for m, item in enumerate(row.values()):
                    if isinstance(item, list):
                        item = ', '.join(item)
                    newitem = QtWidgets.QTableWidgetItem(str(item))
                    newitem.setFlags(flags)
                    table.setItem(n, m, newitem)
            table.setHorizontalHeaderLabels(horHeaders)

        return table
