from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class ManagerTabs(QtWidgets.QWidget):

    clients = 'Clients'
    employees = 'Employees'
    events = 'Events'
    tasks = 'Tasks'
    cp_panel = 'Control Panel'
    new_client = 'New Client'
    hire = 'Hire requests'

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

    # ...and show only the related tabs.
    def _show_team_member(self):
        from view.event_planning_req import EventPlanningReq
        epr = EventPlanningReq()

        self.tabs.addTab(epr, self.cp_panel)

        self.show()

    def _show_customer_service(self):
        from view.event_planning_req import EventPlanningReq
        epr = EventPlanningReq()

        self.tabs.addTab(epr, self.cp_panel)

        self.show()

    def _show_senior_customer_service_officer(self):
        # Retrieve the client IDs
        from view.mediator import get_mediator
        m = get_mediator()
        ids = {c['id']:c['name'] for c in m.get_client()}

        from view.client_req import ClientReq
        cr = ClientReq(ids)

        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(cr, self.new_client)

        self.show()

    def _show_human_resources(self):
        from view.recruitment_req import RecruitmentReq
        r = RecruitmentReq()

        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(r,  self.hire)

        self.show()

    def _show_administration(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_financial(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        #Discounts??

        self.show()

    def _show_production(self):
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_service(self):
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_vice_president(self):
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
