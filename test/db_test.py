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

    def test_db_purge(self):
        db = Database(name=self.test_db, purge=True)
        self.assertEqual(len(db.tables), 5)

    def test_new_user(self):
        db = Database(name=self.test_db)
        db.new_user('randomuser1', '12345', '12345')
        r = db.get_login_data('randomuser1')
        self.assertEqual('randomuser1', r['username'])
        self.assertEqual('12345', r['password'])
        self.assertEqual('12345', r['salt'])
        self.assertIn('user_id', r)

    def test_unique_user(self):
        db = Database(name=self.test_db)
        db.new_user('randomuser2', '12345', '12345')

        with self.assertRaises(KeyError):
            db.new_user('randomuser2', '12345', '12345')

    def test_no_user(self):
        db = Database(name=self.test_db)
        self.assertFalse(db.get_login_data('randomuser3'))

    def test_(self):
        db = Database(name=self.test_db)


if __name__ == '__main__':
    unittest.main()