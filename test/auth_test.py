import sys
if ".." not in sys.path:
    sys.path.append("..")

import unittest

from lib.database import Database
from lib.auth import Authentication

#test hashed password

class AuthTest(unittest.TestCase):

    test_db = 'test_db.json'

    def setUp(self):
        #Change it
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        #Change it
        Database(name=self.test_db, purge=True)

    def test_create_user(self):
        Database(name=self.test_db, purge=True)
        a = Authentication(self.test_db)



    def test_username_exists(self):
        Database(name=self.test_db, purge=True)
        a = Authentication(self.test_db)

    def test_no_such_kind(self):
        Database(name=self.test_db, purge=True)
        a = Authentication(self.test_db)

    def test_success_login(self):
        Database(name=self.test_db)
        a = Authentication(self.test_db)

        db.new_user('randomuser1', '12345', '12345')
        r = db.get_login_data('randomuser1')
        self.assertIn('username', r)
        self.assertIn('password', r)
        self.assertIn('salt', r)

    def test_invalid_login(self):
        Database(name=self.test_db)
        a = Authentication(self.test_db)

        with self.assertRaises(KeyError):
            db.new_user('randomuser2', '12345', '12345')

    def test_wrong_username_login(self):
        Database(name=self.test_db)
        a = Authentication(self.test_db)

        self.assertFalse(db.get_login_data('randomuser3'))

    def test_wrong_password_login(self):
        Database(name=self.test_db)
        a = Authentication(self.test_db)

        db.new_user('randomuser4', '12345', '12345')
        self.assertFalse(db.get_login_data('randomuser4'))

if __name__ == '__main__':
    unittest.main()