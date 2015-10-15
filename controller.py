import sys
from pip._vendor.ipaddress import _TotalOrderingMixin

from lib.database import Database
from lib.auth import Authentication


class Controller():
    def __init__(self):
        self.db = Database()
        self.a = Authentication()

    def login(self, username, password):
        return self.a.login(username, password)

    def create_client(self, name, age, address, mail, phone):
        dict = {'name': name, 'age': age, 'address': address, 'mail': mail, 'phone': phone}
        return self.a.create_user('client', name, **dict)

    def create_client_req(self, client_id, event_type, description, from_date, to_date, exp_no,
                          planned_budget, decorations, filming, poster,
                          food, music, computer, other):
        dict = {'client_id': client_id, 'type': event_type, "description": description, 'from': from_date,
                'to': to_date, 'expected': exp_no,
                'budget': planned_budget, 'decorations': decorations, 'filming': filming,
                'poster': poster, 'food': food, 'music': music, 'computer': computer, 'other': other}
        self.db.new_event(**dict)

    def create_task(self, sub_team, event_id, description, staff_name, priority):
        dict = {'sub_team': sub_team, 'event_id': event_id, 'description': description, 'staff_name': staff_name,
                'priority': priority}
        self.db.new_task(**dict)

    def get_user_id(self, username):
        return self.db.get_login_data(username)['user_id']

    def get_client(self, col_name='', criteria='', all_data=True):
        return self._get_data('client', col_name, criteria, all_data)

    def get_employee(self, col_name='', criteria='', all_data=True):
        return self._get_data('employee', col_name, criteria, all_data)

    def get_dept(self, col_name='', criteria='', all_data=True):
        return self._get_data('dept', col_name, criteria, all_data)

    def get_task(self, col_name='', criteria='', all_data=True):
        return self._get_data('task', col_name, criteria, all_data)

    def get_event(self, col_name='', criteria='', all_data=True):
        return self._get_data('event', col_name, criteria, all_data)

    def _get_data(self, table, col_name, criteria, all_data):
        return getattr(self.db, "get_%s" % table)(col_name, criteria, all_data)
