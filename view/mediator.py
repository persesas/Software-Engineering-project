from controller import Controller

from view.base_template import Base
from view.login_form import LoginForm
from view.tabs import ManagerTabs


class Mediator():
    base = None
    login_form = None

    roles = {'0': 'team_member',
             '1': 'customer_service',
             '2': 'senior_customer_service_officer',
             '3': 'human_resources',
             '4': 'administration',
             '5': 'financial',
             '6': 'production',
             '7': 'service',
             '8': 'vice_president'}

    def __init__(self):
        self.c = Controller()

    def check_credentials(self, username, password):
        return self.c.login(username, password)

    def login(self, username):
        # Get that employee id, clients cant login...
        user_id = self.c.get_user_id(username)
        empl_data = self.get_employee('id', user_id, False)[0]
        name = empl_data['name']
        pos = empl_data['position']

        self.base = Base(name, self.roles[pos].title().replace('_', ' '))
        self.m = ManagerTabs(self.roles[pos])
        self.base.set_central_widget(self.m)

    def logout(self):
        self.login_form.show()

    def create_client(self, name, age, address, mail, phone):
        return self.c.create_client(name, name=name, age=age, address=address, mail=mail, phone=phone)

    def create_client_req(self, client_id, event_type, description, from_date, to_date, exp_no,
                          planned_budget, decorations, filming, poster,
                          food, music, computer, other):
        return self.c.create_client_req(client_id=client_id, event_type=event_type, description=description,
                                        from_date=from_date,
                                        to_date=to_date, exp_no=exp_no, planned_budget=planned_budget,
                                        decorations=decorations,
                                        filming=filming, poster=poster, food=food, music=music, computer=computer,
                                        other=other)

    def create_employee(self, name, age, address, mail, phone):
        return self.c.create_employee(name, name=name, age=age, address=address, mail=mail, phone=phone)

    def create_task(self, sub_team, event_id, description, staff_id, priority):
        self.c.create_task(sub_team=sub_team, event_id=event_id, description=description, staff_id=staff_id,
                           priority=priority)

    def get_client(self, col_name='', criteria='', all_data=True):
        return self._get_data('client', col_name, criteria, all_data)

    def get_employee(self, col_name='', criteria='', all_data=True):
        return self._get_data('employee', col_name, criteria, all_data)

    def get_task(self, col_name='', criteria='', all_data=True):
        return self._get_data('task', col_name, criteria, all_data)

    def get_event(self, col_name='', criteria='', all_data=True):
        return self._get_data('event', col_name, criteria, all_data)

    def update_event(self, ev_id, client_id, event_type, description, from_date, to_date, exp_no,
                     planned_budget, decorations, filming, poster,
                     food, music, computer, other):
        return self.c.update_event(id=ev_id, client_id=client_id, event_type=event_type, description=description,
                                   from_date=from_date,
                                   to_date=to_date, exp_no=exp_no, planned_budget=planned_budget,
                                   decorations=decorations,
                                   filming=filming, poster=poster, food=food, music=music, computer=computer,
                                   other=other)

    def _get_data(self, table, col_name, criteria, all_data):
        return getattr(self.c, "get_%s" % table)(col_name, criteria, all_data)


def get_mediator(_instance=Mediator()):
    return _instance
