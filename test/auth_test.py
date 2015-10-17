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
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        Database(name=self.test_db, purge=True)

    def test_create_user(self):
        a = Authentication(self.test_db)

        self.assertTrue(a.create_user('client', 'user1'))

    def test_username_exists(self):
        a = Authentication(self.test_db)

        a.create_user('employee', 'user2')
        with self.assertRaises(KeyError):
            a.create_user('employee', 'user2')

    def test_no_such_kind(self):
        a = Authentication(self.test_db)

        with self.assertRaises(Exception):
            a.create_user('invalid', 'user3')

    def test_success_login(self):
        a = Authentication(self.test_db)

        a.create_user('employee', 'user4')
        self.assertTrue(a.login('user4', '12345'))

    def test_wrong_username_login(self):
        a = Authentication(self.test_db)

        a.create_user('employee', 'user5')
        self.assertFalse(a.login('userWrong', '12345'))

    def test_wrong_password_login(self):
        a = Authentication(self.test_db)

        a.create_user('employee', 'user6')
        self.assertFalse(a.login('user6', '1'))

if __name__ == '__main__':
    unittest.main()