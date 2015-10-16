import string
import hashlib
import random

from lib.database import Database


class Authentication():
    def __init__(self, db_name='db.json'):
        self.db = Database(name=db_name)

    def _gen_salt(self, length=6, chars=string.ascii_letters):
        return ''.join([random.choice(chars) for _ in range(length)])

    def _gen_password(self):
        return '12345'

    def create_user(self, kind, username, **kwargs):
        # Create client in the database
        if kind == 'client':
            user_id = self.db.new_client(**kwargs)
        elif kind == 'employee':
            user_id = self.db.new_employee(**kwargs)
        else:
            raise Exception('Invalid user.')

        # Create new user in the database
        salt = self._gen_salt()

        m = hashlib.sha256()
        m.update(self._gen_password().encode('utf-8'))
        m.update(salt.encode('utf-8'))

        self.db.new_user(username, m.hexdigest(), salt, user_id)

    # Client needs to know the password

    def login(self, username, password):
        # retrieve the data from db
        # test: no such user, wrong/correct login
        info = self.db.get_login_data(username)
        if not info:
            # wrong username
            return False

        # generate the password
        m = hashlib.sha256()
        m.update(password.encode('utf-8'))
        m.update(info['salt'].encode('utf-8'))

        return info['password'] == m.hexdigest()
