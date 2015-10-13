import string
import random
from datetime import datetime

import tinydb
from tinydb import where
from tinydb.serialize import Serializer
from tinydb.storages import JSONStorage
from tinydb.middlewares import SerializationMiddleware

"""
Main tables:
Client = id(str), name(str), age(int), address(str), email(str), phone(str),
		 events(event ids)
Employee = id(str), name(str), age(int), address(str), boss(employee id), position(str)
Department = id(str), leader(str), name(str), members(employee id list) -----TO BE DELETED---
Event = id(str), type(string), from(date), to(date), attendees(int)
		preferences(str), budget(int), name(str), status(str)
Task = id(str), subject(str), priority(int), sender(employee id), description(str)

Support tables:
Auth = username(str), password(hashed + salt str), salt(str), user_id(cl, empl str)
Team = boss(employee id), name(str), members(employee id list) -----TO BE DELETED-------
"""


class Database():
    """Docstring for database manager"""

    tables = ['client', 'event', 'employee', 'team', 'department', 'task', 'auth']

    def __init__(self, name='db.json', purge=False):
        # test initial number of tables
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
        self.db = tinydb.TinyDB('Data/' + name, storage=serialization)

        if purge:
            self.db.purge_tables()

        self._init_db()

    def _init_db(self):
        # Ensure that the tables exist
        self.tables_db = {t: self.db.table(t) for t in self.tables}

    def _gen_id(self, length=6, chars=string.digits):
        return ''.join([random.choice(chars) for _ in range(length)])

    # Generic functions
    def get_row_by_id(self, tbl_name, id):
        # Search Client, Employee, Department, Event
        return self.tables_db[tbl_name].search(where('id') == id)

    def search(self, tbl_name, col_name, value):
        # Arbitrary search
        # invalid column
        return self.tables_db[tbl_name].search(where(col_name) == value)

    def insert(self, tbl_name, data):
        # data = {col1:data1, col2:data2, ...}
        # name(test) = non empty and follow the rules, exists -> KeyError
        # empty data on return(where=blabla) = []
        self.tables_db[tbl_name].insert(data)

    # Specific functions
    def new_client(self, **kwargs):
        # Client = id(str), name(str), age(int), address(str), events(event ids)
        user_id = 'cl' + self._gen_id()
        data = {'id': user_id}
        data.update(kwargs)
        self.insert('client', data)

        return user_id

    def get_client(self, col_name, criteria, all_data=False):
        if not all_data:
            return self.tables_db['client'].search(where(col_name) == criteria)
        else:
            return self.tables_db['client'].all()

    def new_employee(self, **kwargs):
        # Employee = id(str), name(str), age(int), address(str), boss(employee id)
        user_id = 'em' + self._gen_id()
        data = {'id': user_id}
        data.update(kwargs)
        self.insert('employee', data)

        return user_id

    def get_employee(self, col_name, criteria, all_data=False):
        if not all_data:
            return self.tables_db['employee'].search(where(col_name) == criteria)
        else:
            return self.tables_db['employee'].all()

    def new_dept(self, **kwargs):
        # Department = id(str), leader(str), name(str), members(employee id list)
        user_id = 'dt' + self._gen_id()
        data = {'id': user_id}
        data.update(kwargs)
        self.insert('dept', data)

        return user_id

    def get_dept(self, col_name, criteria, all_data=False):
        if not all_data:
            return self.tables_db['dept'].search(where(col_name) == criteria)
        else:
            return self.tables_db['dept'].all()

    def new_task(self, **kwargs):
        # Task = id(str), subject(str), priority(int), sender(employee id), description(str)
        user_id = 't' + self._gen_id()
        data = {'id': user_id}
        data.update(kwargs)
        self.insert('task', data)

        return user_id

    def get_task(self, col_name, criteria, all_data=False):
        if not all_data:
            return self.tables_db['task'].search(where(col_name) == criteria)
        else:
            return self.tables_db['task'].all()

    def new_event(self, **kwargs):
        # Event = id(str), type(string), from(date), to(date), attendees(int)
        #         preferences(str), budget(int), name(str), status(str)
        user_id = 'ev' + self._gen_id()
        data = {'id': user_id}
        data.update(kwargs)
        self.insert('event', data)

        return user_id

    def get_event(self, col_name, criteria, all_data=False):
        if not all_data:
            return self.tables_db['event'].search(where(col_name) == criteria)
        else:
            return self.tables_db['event'].all()

    def get_login_data(self, username):
        r = self.tables_db['auth'].search(where('username') == username)
        return r[0] if r else []

    # Create accounts(admin, pending)
    def new_user(self, username, password, salt, user_id):
        if self.get_login_data(username):
            raise KeyError('User {} already exists.'.format(username))

        self.tables_db['auth'].insert({'username': username,
                                       'password': password,
                                       'salt': salt,
                                       'user_id': user_id})


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
