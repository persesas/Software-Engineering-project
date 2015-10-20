import sys

if ".." not in sys.path:
    sys.path.append("..")

import unittest

from lib.database import Database
from lib.auth import Authentication
from controller import Controller


class ControllerTest(unittest.TestCase):
    test_db = 'test_db.json'

    def setUp(self):
        # Change it
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        # Change it
        Database(name=self.test_db, purge=True)

    def test_login(self):
        a = Authentication(self.test_db)
        c = Controller(self.test_db)

        a.create_user('employee', 'user1')

        self.assertTrue(c.login('user1', '12345'))

    def test_create_client(self):
        c = Controller(self.test_db)

        cl_id = c.create_client('cl12345', name='Foo Bar', age='23')
        cl_data = c.get_client('id', cl_id)[0]

        self.assertEqual('Foo Bar', cl_data['name'])
        self.assertEqual('23', cl_data['age'])

    def test_create_employee(self):
        c = Controller(self.test_db)

        em_id = c.create_employee('em12345', name='Foo Bar', age='23', pos='3')
        em_data = c.get_employee('id', em_id)[0]

        self.assertEqual('Foo Bar', em_data['name'])
        self.assertEqual('23', em_data['age'])
        self.assertEqual('3', em_data['pos'])

    def test_create_client_request(self):
        c = Controller(self.test_db)
        #Create a client
        cl_id = c.create_client('username', name='Foo Bar', age='23', events=[])

        event_id = c.create_client_req(client_id=cl_id, event_type='Unicorn exhibition', description='desc',
                                       from_date='09-12-2015', exp_no='exp_no', planned_budget='planned_budget',
                                       decorations='decorations',
                                       filming='filming', poster='poster', food='food', music='music',
                                       computer='computer',
                                       other='other')
        event_data = c.get_event('id', event_id)[0]

        self.assertEqual('Unicorn exhibition', event_data['event_type'])
        self.assertEqual(cl_id, event_data['client_id'])
        self.assertEqual('09-12-2015', event_data['from_date'])


    def test_update_event(self):
        c = Controller(self.test_db)
        #Create a client
        cl_id = c.create_client('username', name='Foo Bar', age='23', events=[])

        event_id = c.create_client_req(event_type='Mohawk fans', from_date='09-12-2042', client_id=cl_id)

        updated_event = {'id': event_id, 'from_date': '08-12-2015'}
        c.update_event(**updated_event)
        event_data = c.get_event('id', event_id)[0]

        self.assertEqual('Mohawk fans', event_data['event_type'])
        self.assertEqual(cl_id, event_data['client_id'])
        self.assertEqual('08-12-2015', event_data['from_date'])

    def test_update_client_events(self):
        c = Controller(self.test_db)

        cl_id = c.create_client('cl12345', name='Foo Bar', events=['ev12345'])
        c.update_client_events(cl_id, [])
        cl_data = c.get_client('id', cl_id)[0]

        self.assertFalse(cl_data['events'])

        self.assertEqual([], cl_data['events'])

    def test_create_task(self):
        c = Controller(self.test_db)

        task_id = c.create_task(subject='Underwater photos', priority='Medium')
        task_data = c.get_task('id', task_id)[0]

        self.assertEqual('Underwater photos', task_data['subject'])
        self.assertEqual('Medium', task_data['priority'])

    def test_update_task(self):
        c = Controller(self.test_db)

        task_id = c.create_task(subject='Underwater photos', priority='Medium')
        updated_task = {'id': task_id, 'subject': 'Aerial dancing', 'priority': 'High'}
        c.update_task(**updated_task)
        task_data = c.get_task('id', task_id)[0]

        self.assertEqual('Aerial dancing', task_data['subject'])
        self.assertEqual('High', task_data['priority'])

    def test_get_user_id(self):
        c = Controller(self.test_db)

        cl_id = c.create_client('user1')
        cl_data = c.get_client('id', cl_id)[0]

        self.assertEqual(cl_id, cl_data['id'])


if __name__ == '__main__':
    unittest.main()
