from collections import OrderedDict

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
    hire = 'Hire Employees'
    new_event = 'New Events'
    new_task = 'New Task'

    event_popup = None
    task_popup = None

    def __init__(self, empl_type, user_id, name):
        super().__init__()
        self.user_id = user_id
        self.name = name
        self.employee_type = empl_type

        self.initUI()
        getattr(self, '_show_{}'.format(empl_type))()

    def initUI(self):
        # Initialize tab widgets
        self.tabs = QtWidgets.QTabWidget()
        self.employee_tab = self._create_employee_tab()
        self.client_tab = self._create_client_tab()
        self.event_tab = self._create_event_tab()
        self.task_tab = self._create_task_tab()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def _rearrange(self, table, cols):
        tbl = []
        for r in table:
            d = OrderedDict(r)
            for c in reversed(cols):
                d.move_to_end(c)
            tbl.append(OrderedDict(reversed(list(d.items()))))
        return tbl

    # Create everything...
    def _create_employee_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_employee()

        empl_table = self._create_table(self._rearrange(data, ['id', 'name']))

        return empl_table

    def _create_client_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_client()

        client_table = self._create_table(self._rearrange(data, ['id', 'name']))

        return client_table

    def _create_event_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_event()

        event_table = self._create_table(
            self._rearrange(data, ['id', 'client_id', 'from_date', 'to_date', 'seen']))
        event_table.cellDoubleClicked.connect(self.onEventDoubleClick)
        # Event contains a lot of information, hide some...
        for i in range(5, event_table.columnCount()):
            event_table.setColumnHidden(i, True)

        return event_table

    def _create_task_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()


        if self.employee_type == 'team_member':
            data = m.get_task('staff_id', '{}-{}'.format(self.user_id, self.name), all_data=False)
        else:
            data = m.get_task()

        task_table = self._create_table(self._rearrange(data, ['id', 'priority']))
        task_table.cellDoubleClicked.connect(self.onTaskDoubleClick)

        return task_table

    def onEventDoubleClick(self, row, col):
        if not self.event_popup or not self.event_popup.isVisible():
            from view.event_req import ClientReq
            from view.mediator import get_mediator
            m = get_mediator()
            # get the client id from the table
            cl_id = self.event_tab.item(row, 1).text()
            # the event id
            ev_id = self.event_tab.item(row, 0).text()
            event_data = m.get_event('id', ev_id, all_data=False)[0]
            event_data.update({'id': ev_id})
            # and his/her name
            name = m.get_client('id', cl_id, all_data=False)[0]['name']

            self.event_popup = ClientReq({cl_id: name}, event_data)
        else:
            self.event_popup.setFocus()

    def onTaskDoubleClick(self, row, col):
        if not self.event_popup or not self.event_popup.isVisible():
            from view.task_req import TaskReq
            from view.mediator import get_mediator
            m = get_mediator()

            task_id = self.task_tab.item(row, 0).text()
            task_data = m.get_task('id', task_id, all_data=False)[0]
            task_data.update({'id': task_id})

            event_ids = [c['id'] for c in m.get_event()]
            # ----
            staff_data = m.get_employee('position', '0', all_data=False)
            team_members = [{'id': s['id'], 'name': s['name']} for s in staff_data]
            # ----
            sub_teams = ['Photography', 'Decoration']
            self.task_popup = TaskReq(event_ids, team_members, sub_teams, task_data)
        else:
            self.task_popup.setFocus()

    # ...and show only the related tabs.
    def _show_team_member(self):
        self.tabs.addTab(self.task_tab, self.tasks)

        self.show()

    def _show_customer_service(self):
        from view.mediator import get_mediator
        m = get_mediator()
        ids = {c['id']: c['name'] for c in m.get_client()}

        from view.event_req import ClientReq
        cr = ClientReq(ids)

        self.tabs.addTab(cr, self.new_event)

        self.show()

    def _show_senior_customer_service_officer(self):
        # Retrieve the client IDs
        from view.mediator import get_mediator
        m = get_mediator()
        ids = {c['id']: c['name'] for c in m.get_client()}

        from view.new_client_req import NewClient
        nc = NewClient()

        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(nc, self.new_client)

        self.show()

    def _show_human_resources(self):
        from view.new_employee import NewEmployee
        e = NewEmployee()

        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(e, self.hire)

        self.show()

    def _show_administration(self):
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)

        self.show()

    def _show_financial(self):
        from view.recruitment_req import RecruitmentReq
        r = RecruitmentReq()

        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(r, self.hire)

        self.show()

    def _show_production(self):
        from view.recruitment_req import RecruitmentReq
        from view.task_req import TaskReq
        from view.mediator import get_mediator

        m = get_mediator()

        r = RecruitmentReq()
        sub_teams = ['Photography', 'Decorations']
        event_ids = [c['id'] for c in m.get_event()]

        staff_data = m.get_employee('position', '0', all_data=False)
        team_members = [{'id': s['id'], 'name': s['name']} for s in staff_data]

        t = TaskReq(event_ids, team_members, sub_teams)

        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.task_tab, self.tasks)
        self.tabs.addTab(t, self.new_task)
        self.tabs.addTab(r, self.hire)

        self.show()

    def _show_service(self):
        from view.recruitment_req import RecruitmentReq
        from view.task_req import TaskReq
        from view.mediator import get_mediator
        m = get_mediator()

        r = RecruitmentReq()
        sub_teams = ['Photography', 'Decorations']
        event_ids = [c['id'] for c in m.get_event()]

        staff_data = m.get_employee('position', '0')
        team_members = {'id': staff_data['id'], 'name': staff_data['name']}

        t = TaskReq(event_ids, team_members, sub_teams)

        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.task_tab, self.tasks)
        self.tabs.addTab(t, self.new_task)
        self.tabs.addTab(r, self.hire)

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
