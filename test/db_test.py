import sys
if ".." not in sys.path:
    sys.path.append("..")

import unittest

from lib.database import Database

#test hashed password

class TestDatabase(unittest.TestCase):

    test_db = 'test_db.json'

    def setUp(self):
        #Change it
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        #Change it
        Database(name=self.test_db, purge=True)

    def test_01_db_purge(self):
        db = Database(name=self.test_db, purge=True)
        self.assertEqual(len(db.tables), 7)

    def test_02_new_user(self):
        db = Database(name=self.test_db)
        db.new_user('randomuser1', '12345', '12345')
        r = db.get_login_data('randomuser1')
        self.assertIn('username', r)
        self.assertIn('password', r)
        self.assertIn('salt', r)

    def test_03_unique_user(self):
        db = Database(name=self.test_db)
        db.new_user('randomuser2', '12345', '12345')

        with self.assertRaises(KeyError):
            db.new_user('randomuser2', '12345', '12345')

    def test_04_no_user(self):
        db = Database(name=self.test_db)
        self.assertFalse(db.get_login_data('randomuser3'))

    def test_05_delete_user(self):
        db = Database(name=self.test_db)
        db.new_user('randomuser4', '12345', '12345')
        db.delete_user('randomuser4')
        self.assertFalse(db.get_login_data('randomuser4'))

if __name__ == '__main__':
    unittest.main()