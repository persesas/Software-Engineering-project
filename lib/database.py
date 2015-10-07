from datetime import datetime

import tinydb
from tinydb import where
from tinydb.serialize import Serializer
from tinydb.storages import JSONStorage
from tinydb.middlewares import SerializationMiddleware

"""
Main tables:
Client = id(str), name(str), age(int), address(str), events(event ids)
Employee = id(str), name(str), age(int), address(str), boss(employee id)
Department = id(str), leader(str), name(str), members(employee id list)
Event = id(str), type(string), from(date), to(date), attendees(int)
		preferences(str), budget(int), name(str), status(str)

Support tables:
Task = subject(str), priority(int), sender(employee id), description(str)
Auth = username(str), password(hashed + salt str), salt(str)
Team = boss(employee id), name(str), members(employee id list)
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
		self.tables_db = {t:self.db.table(t) for t in self.tables}

	# Get functions
	def get_row_by_id(self, tbl_name, id):
		# Search Client, Employee, Department, Event
		return self.tables_db[tbl_name].search(where('id')==id)

	def search(self, tbl_name, col_name, value):
		# Arbitrary search
		# invalid column
		return self.tables_db[tbl_name].search(where(col_name)==value)

	def get_login_data(self, username):
		return self.tables_db['auth'].search(where('username')==username)

	#Insert/Update functions
	def insert(self, tbl_name, data):
		#data = {col1:data1, col2:data2, ...}
		#name(test) = non empty and follow the rules, exists -> KeyError
		#empty data on return(where=blabla) = []
		self.tables_db[tbl_name].insert(data)

	def new_user(self, username, password, salt):
		if self.get_login_data(username):
			raise KeyError('User {} already exists.'.format(username))
		self.tables_db['auth'].insert({'username':username,
									   'password':password,
									   'salt':salt})

	def delete_user(self, username):
		self.tables_db['auth'].remove(where('username')==username)

class DateTimeSerializer(Serializer):
	OBJ_CLASS = datetime  # The class this serializer handles

	def encode(self, obj):
		return obj.strftime('%Y-%m-%dT%H:%M:%S')

	def decode(self, s):
		return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')