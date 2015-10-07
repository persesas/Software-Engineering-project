import string
import hashlib
import random

from lib.database import Database


class Authentication():
	def __init__(self):
		self.db = Database()

	def _gen_salt(self, length=6, chars=string.ascii_letters):
		return ''.join([ random.choice(chars) for _ in range(length)])

	def delete_user(self, username):
		pass

	def create_user(self, username, password):
		salt = self._gen_salt()

		m = hashlib.sha256()
		m.update(password.encode('utf-8'))
		m.update(salt.encode('utf-8'))

		self.db.new_user(username, m.hexdigest(), salt)

	def login(self, username, password):
		#the user already exists
		#retrieve the data from db
		#test: no such user, wrong/correct login
		info = self.db.get_login_data(username)

		#generate the password
		m = hashlib.sha256()
		m.update(password.encode('utf-8'))
		m.update(info['salt'].encode('utf-8'))

		return info['password'] == m.hexdigest()
