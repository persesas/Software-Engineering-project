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

    def create_client(self, username, **kwargs):
        return self.a.create_user('client', username, kwargs)

    def create_client_req(self, **kwargs):
        self.db.new_event(**kwargs)

    def create_task(self, **kwargs):
        self.db.new_task(**kwargs)

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
