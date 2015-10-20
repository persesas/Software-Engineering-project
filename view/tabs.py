from collections import OrderedDict

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ManagerTabs(QtWidgets.QWidget):
    clients = 'Clients'
    employees = 'Employees'
    events = 'Events'
    tasks = 'Tasks'
    cp_panel = 'Control Panel'
    new_client = 'New Client'
    hire = 'Hire Employees'
    hire_req = 'Hire Request'
    new_event = 'New Event'
    new_task = 'New Task'
    fin_req = 'Financial requests'
    recs_req = 'Recruitment requests'
    financial_req = 'Extra Budget Request'

    event_popup = None
    task_popup = None
    financial_req_popup = None
    recruitment_req_popup = None

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
        self.financial_req_tab = self._create_financial_req_tab()
        self.recruitment_req_tab = self._create_recruitment_req_tab()

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
        empl_table = self._create_table(self._rearrange(data, ['id', 'name', 'position', 'mail', 'address', 'age']))

        return empl_table

    def _create_client_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_client()
        client_table = self._create_table(self._rearrange(data,
                                                          ['id', 'name', 'events', 'mail', 'address', 'phone', 'age']))

        return client_table

    def _create_event_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_event()
        event_table = self._create_table(
            self._rearrange(data, ['id', 'client_id', 'event_type', 'description', 'approved', 'from_date', 'to_date',
                                   'exp_no',
                                   'planned_budget', 'decorations', 'filming', 'poster', 'food', 'music', 'computer',
                                   'other']))
        event_table.cellDoubleClicked.connect(self.onEventDoubleClick)
        # Event contains a lot of information, hide some...
        for i in range(8, event_table.columnCount()):
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

    def _create_financial_req_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()

        data = m.get_financial_req()
        financial_req_table = self._create_table(self._rearrange(data,
                                                          ['id','event_id', 'req_dpt', 'req_amount', 'reason']))
        financial_req_table.cellDoubleClicked.connect(self.onFinReqDoubleClick)
        return financial_req_table

    def _create_recruitment_req_tab(self):
        from view.mediator import get_mediator
        m = get_mediator()
        data = m.get_recruitment_req()
        recruitment_req_table = self._create_table(self._rearrange(data,
                                                          ['id', 'req_dpt', 'type', 'years_exp', 'title', 'description']))
        recruitment_req_table.cellDoubleClicked.connect(self.onRecReqDoubleClick)
        return recruitment_req_table

    def onRecReqDoubleClick(self, row, col):
        if not self.recruitment_req_popup or not self.recruitment_req_popup.isVisible():
            from view.recruitment_req import RecruitmentReq
            from view.mediator import get_mediator
            m = get_mediator()
            # the event id
            rec_req = self.recruitment_req_tab.item(row, 0).text()
            fin_req_data = m.get_recruitment_req('id', rec_req, all_data=False)[0]
            fin_req_data.update({'id': rec_req})
            self.recruitment_req_popup = RecruitmentReq(self.employee_type, fin_req_data)
        else:
            self.recruitment_req_popup.setFocus()

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
            self.event_popup = ClientReq({cl_id: name}, event_data,
                                         self.employee_type == 'senior_customer_service_officer')
        else:
            self.event_popup.setFocus()

    def onFinReqDoubleClick(self, row, col):
        if not self.financial_req_popup or not self.financial_req_popup.isVisible():
            from view.financial_req import FinancialReq
            from view.mediator import get_mediator
            m = get_mediator()
            # the event id
            event_ids = [c['id'] for c in m.get_event()]
            fin_req = self.financial_req_tab.item(row, 0).text()
            fin_req_data = m.get_financial_req('id', fin_req, all_data=False)[0]
            fin_req_data.update({'id': fin_req})
            self.event_popup = FinancialReq(self.employee_type, event_ids, fin_req_data)
        else:
            self.financial_req_popup.setFocus()

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
            sub_teams = ['Photography', 'Decoration', 'Audio', 'Graphic designer', 'Network Engineer', 'Technician']
            if self.employee_type == 'team_member':
                self.task_popup = TaskReq(event_ids, team_members, sub_teams, task_data, True)
            else:
                self.task_popup = TaskReq(event_ids, team_members, sub_teams, task_data, False)
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

        from view.new_client import NewClient
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
        self.tabs.addTab(self.recruitment_req_tab, self.recs_req)

        self.show()

    def _show_administration(self):
        from view.recruitment_req import RecruitmentReq
        r = RecruitmentReq(self.employee_type)
        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(r, self.hire_req)

        self.show()

    def _show_financial(self):
        from view.recruitment_req import RecruitmentReq
        r = RecruitmentReq(self.employee_type)

        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.financial_req_tab, self.fin_req)
        self.tabs.addTab(r, self.hire_req)

        self.show()

    def _show_production(self):
        from view.recruitment_req import RecruitmentReq
        from view.task_req import TaskReq
        from view.mediator import get_mediator
        from view.financial_req import FinancialReq

        m = get_mediator()

        r = RecruitmentReq(self.employee_type)
        sub_teams = ['Photography', 'Decoration', 'Audio', 'Graphic designer', 'Network Engineer', 'Technician']
        event_ids = [c['id'] for c in m.get_event()]
        f = FinancialReq(self.employee_type, event_ids)

        staff_data = m.get_employee('position', '0', all_data=False)
        team_members = [{'id': s['id'], 'name': s['name']} for s in staff_data]

        t = TaskReq(event_ids, team_members, sub_teams)

        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.task_tab, self.tasks)
        self.tabs.addTab(t, self.new_task)
        self.tabs.addTab(r, self.hire_req)
        self.tabs.addTab(f, self.financial_req)

        self.show()

    def _show_service(self):
        from view.recruitment_req import RecruitmentReq
        from view.task_req import TaskReq
        from view.mediator import get_mediator
        from view.financial_req import FinancialReq
        m = get_mediator()

        r = RecruitmentReq(self.employee_type)

        sub_teams = ['Photography', 'Decoration', 'Audio', 'Graphic designer', 'Network Engineer', 'Technician']
        event_ids = [c['id'] for c in m.get_event()]
        f = FinancialReq(self.employee_type, event_ids)

        staff_data = m.get_employee('position', '0', all_data=False)
        team_members = [{'id': s['id'], 'name': s['name']} for s in staff_data]

        t = TaskReq(event_ids, team_members, sub_teams)

        self.tabs.addTab(self.event_tab, self.events)
        self.tabs.addTab(self.task_tab, self.tasks)
        self.tabs.addTab(t, self.new_task)
        self.tabs.addTab(r, self.hire_req)
        self.tabs.addTab(f, self.financial_req)

        self.show()

    def _show_vice_president(self):

        self.tabs.addTab(self.employee_tab, self.employees)
        self.tabs.addTab(self.client_tab, self.clients)
        self.tabs.addTab(self.event_tab, self.events)
        self.show()

    def _create_table(self, data):
        table = QtWidgets.QTableWidget()

        if data:
            hor_headers = list(data[0].keys())
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            table.setRowCount(len(data))
            table.setColumnCount(len(hor_headers))

            flags = Qt.NoItemFlags | Qt.ItemIsEnabled

            for n, row in enumerate(data):
                # for every row
                for m, item in enumerate(row.values()):
                    if isinstance(item, list):
                        item = ', '.join(item)
                    newitem = QtWidgets.QTableWidgetItem(str(item))
                    newitem.setFlags(flags)
                    table.setItem(n, m, newitem)
            table.setHorizontalHeaderLabels(hor_headers)

        return table
