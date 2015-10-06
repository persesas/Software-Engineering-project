from datetime import datetime

import tinydb
from tinydb.serialize import Serializer
from tinydb.storages import JSONStorage
from tinydb.middlewares import SerializationMiddleware

"""
Client = id(str), name(str), age(int), address(str), events(event ids)
Event = id(str), type(string), from(date), to(date), attendees(int)
		preferences(str), budget(int), name(str), status(str)
Employee = id(str), name(str), age(int), address(str), boss(employee id)
Team = id(str), boss(employee id), name(str), members(employee id list)
Department = id(str), leader(str), name(str), members(employee id list)
Task = subject(str), priority(int), sender(employee id), description(str)
Auth = username(str), password(hashed + salt str), salt(str)
"""


class Database():
	"""Docstring for database manager"""

	tables = ['client', 'event', 'employee', 'team', 'department', 'task', 'auth']

	def __init__(self, name='db.json'):
		serialization = SerializationMiddleware()
		serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
		self.db = tinydb.TinyDB('Data/' + name, storage=serialization)

		self.init_db()

	def init_db(self):
		# Ensure that the tables exist
		self.tables_db = {t:self.db.table(t) for t in self.tables}

	def insert(self, tbl_name, data):
		#data = {col1:data1, col2:data2, ...}
		#name(test) = non empty and follow the rules, exists -> KeyError
		self.tables_db[tbl_name].insert(data)


class DateTimeSerializer(Serializer):
	OBJ_CLASS = datetime  # The class this serializer handles

	def encode(self, obj):
		return obj.strftime('%Y-%m-%dT%H:%M:%S')

	def decode(self, s):
		return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')