from database import Database


class Authentication():
	def __init__(self):
		self.db = Database()

	def login(self, username, password):
		pass