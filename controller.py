import sys
from pip._vendor.ipaddress import _TotalOrderingMixin

from lib.database import Database
from lib.auth import Authentication


class Controller():
    def __init__(self, db_name='db.json'):
        self.db = Database(name=db_name)
        self.a = Authentication(db_name=db_name)

    def login(self, username, password):
        return self.a.login(username, password)

    def create_client(self, username, **kwargs):
        return self.a.create_user('client', username, **kwargs)

    def create_client_req(self, **kwargs):
        event_id = self.db.new_event(**kwargs)
        clients_events = self.db.get_client('id',kwargs['client_id'], all_data=False)[0]['events']
        clients_events.append(event_id)
        self.db.update_client_events(kwargs['client_id'], clients_events)

        return event_id

    def create_employee(self, username, **kwargs):
        return self.a.create_user('employee', username, **kwargs)

    def update_event(self, **kwargs):
        self.db.update_event(kwargs)

    def create_task(self, **kwargs):
        return self.db.new_task(**kwargs)

    def update_task(self, **kwargs):
        self.db.update_task(kwargs)

    def get_user_id(self, username):
        return self.db.get_login_data(username)['user_id']

    def update_client_events(self, cl_id, events):
        self.db.update_client_events(cl_id, events)

    def get_client(self, col_name='', criteria='', all_data=True):
        return self._get_data('client', col_name, criteria, all_data)

    def get_employee(self, col_name='', criteria='', all_data=True):
        return self._get_data('employee', col_name, criteria, all_data)

    def get_task(self, col_name='', criteria='', all_data=True):
        return self._get_data('task', col_name, criteria, all_data)

    def get_event(self, col_name='', criteria='', all_data=True):
        return self._get_data('event', col_name, criteria, all_data)

    def _get_data(self, table, col_name, criteria, all_data):
        return getattr(self.db, "get_%s" % table)(col_name, criteria, all_data)
