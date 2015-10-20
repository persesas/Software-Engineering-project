import sys

if ".." not in sys.path:
    sys.path.append("..")

import unittest

from lib.database import Database


# test hashed password

class ControllerTest(unittest.TestCase):
    test_db = 'test_db.json'

    def setUp(self):
        # Change it
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        # Change it
        Database(name=self.test_db, purge=True)

    def test_db_purge(self):
        db = Database(name=self.test_db, purge=True)

        self.assertEqual(len(db.tables), 7)

    def test_new_user(self):
        db = Database(name=self.test_db, purge=True)
        db.new_user('user1', '12345', '12345', 'cl12345')

        r = db.get_login_data('user1')
        self.assertEqual('user1', r['username'])
        self.assertEqual('12345', r['password'])
        self.assertEqual('12345', r['salt'])
        self.assertIn('cl12345', r['user_id'])

    def test_unique_user(self):
        db = Database(name=self.test_db, purge=True)
        db.new_user('user2', '12345', '12345', 'cl12345')

        with self.assertRaises(KeyError):
            db.new_user('user2', '12345', '12345', 'cl12345')

    def test_no_user(self):
        db = Database(name=self.test_db, purge=True)

        self.assertFalse(db.get_login_data('randomuser3'))

    def test_new_client(self):
        db = Database(name=self.test_db, purge=True)

        cl_id = db.new_client(name='Foo Bar', age='23')
        cl_data = db.get_client('id', cl_id)[0]

        self.assertEqual('Foo Bar', cl_data['name'])
        self.assertEqual('23', cl_data['age'])

    def test_update_client_events(self):
        db = Database(name=self.test_db, purge=True)

        cl_id = db.new_client(name='Foo Bar', events=['ev12345'])
        db.update_client_events(cl_id, [])
        cl_data = db.get_client('id', cl_id)[0]

        self.assertFalse(cl_data['events'])

    def test_new_employee(self):
        db = Database(name=self.test_db, purge=True)

        em_id = db.new_employee(name='Foo Bar', age='23', pos='3')
        em_data = db.get_employee('id', em_id)[0]

        self.assertEqual('Foo Bar', em_data['name'])
        self.assertEqual('23', em_data['age'])
        self.assertEqual('3', em_data['pos'])

    def test_new_recruitment_req(self):
        db = Database(name=self.test_db, purge=True)
        rec_req = db.new_recruitment_req(type='Full time', years_exp='23', title='Manager', description='description1',
                                         dpt_req='financial')
        rec_req_data = db.get_recruitment_req('id', rec_req)[0]

        self.assertEqual('Full time', rec_req_data['type'])
        self.assertEqual('23', rec_req_data['years_exp'])
        self.assertEqual('Manager', rec_req_data['title'])
        self.assertEqual('description1', rec_req_data['description'])
        self.assertEqual('financial', rec_req_data['dpt_req'])

    def test_update_recruitment_req(self):
        db = Database(name=self.test_db, purge=True)
        rec_req = db.new_recruitment_req(type='Full time', years_exp='23', title='Manager', description='description1',
                                         dpt_req='financial')

        db.update_recruitment_req(
            {'id': rec_req, 'type': 'part time', 'years_exp': '312', 'title': 'employee', 'description': 'desc2',
             'dpt_req': 'production'})

        rec_req_data = db.get_recruitment_req('id', rec_req)[0]

        self.assertEqual('part time', rec_req_data['type'])
        self.assertEqual('312', rec_req_data['years_exp'])
        self.assertEqual('employee', rec_req_data['title'])
        self.assertEqual('desc2', rec_req_data['description'])
        self.assertEqual('production', rec_req_data['dpt_req'])

    def test_new_task(self):
        db = Database(name=self.test_db, purge=True)

        task_id = db.new_task(subject='Underwater photos', priority='Medium')
        task_data = db.get_task('id', task_id)[0]

        self.assertEqual('Underwater photos', task_data['subject'])
        self.assertEqual('Medium', task_data['priority'])

    def test_update_task(self):
        db = Database(name=self.test_db, purge=True)

        task_id = db.new_task(subject='Underwater photos', priority='Medium')
        db.update_task({'id': task_id, 'subject': 'Aerial dancing', 'priority': 'High'})
        task_data = db.get_task('id', task_id)[0]

        self.assertEqual('Aerial dancing', task_data['subject'])
        self.assertEqual('High', task_data['priority'])

    def test_new_financial_req(self):
        db = Database(name=self.test_db, purge=True)

        fin_req_id = db.new_financial_req(event_id='ev1234', req_amount=212, reason='reason1',
                                          req_dpt='req_dpt1')
        fin_req_data = db.get_financial_req('id', fin_req_id)[0]

        self.assertEqual('ev1234', fin_req_data['event_id'])
        self.assertEqual(212, fin_req_data['req_amount'])
        self.assertEqual('reason1', fin_req_data['reason'])
        self.assertEqual('req_dpt1', fin_req_data['req_dpt'])

    def test_update_financial_req(self):
        db = Database(name=self.test_db, purge=True)

        fin_req_id = db.new_financial_req(event_id='ev1234', req_amount=212, reason='reason1',
                                          req_dpt='req_dpt1')
        db.update_financial_req(
            {'id': fin_req_id, 'event_id': 'ev9876', 'req_amount': 321321, 'reason': 'reason2', 'req_dpt': 'req_dpt2'})

        fin_req_data = db.get_financial_req('id', fin_req_id)[0]

        self.assertEqual('ev9876', fin_req_data['event_id'])
        self.assertEqual(321321, fin_req_data['req_amount'])
        self.assertEqual('reason2', fin_req_data['reason'])
        self.assertEqual('req_dpt2', fin_req_data['req_dpt'])

    def test_new_event(self):
        db = Database(name=self.test_db, purge=True)

        event_id = db.new_event(event_type='Unicorn exhibition', from_date='09-12-2015')
        event_data = db.get_event('id', event_id)[0]

        self.assertEqual('Unicorn exhibition', event_data['event_type'])
        self.assertEqual('09-12-2015', event_data['from_date'])

    def test_update_event(self):
        db = Database(name=self.test_db, purge=True)

        event_id = db.new_event(event_type='Mohawk fans', from_date='09-12-2042')
        db.update_event({'id': event_id, 'from_date': '08-12-2015'})
        event_data = db.get_event('id', event_id)[0]

        self.assertEqual('Mohawk fans', event_data['event_type'])
        self.assertEqual('08-12-2015', event_data['from_date'])


if __name__ == '__main__':
    unittest.main()
