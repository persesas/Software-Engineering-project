import unittest

from lib.database import Database
from lib.auth import Authentication
from view.mediator import Mediator
from controller import Controller


class MediatorTest(unittest.TestCase):
    test_db = 'test_db.json'

    def setUp(self):
        Database(name=self.test_db, purge=True)

    def tearDown(self):
        Database(name=self.test_db, purge=True)

    def test_login(self):
        a = Authentication(self.test_db)
        m = Mediator('test_db.json')

        a.create_user('employee', 'user1')
        a.create_user('client', 'cl1')

        self.assertTrue(m.check_credentials('user1', '12345'))
        self.assertTrue(m.check_credentials('cl1', '12345'))

    def test_create_client(self):
        m = Mediator('test_db.json')

        cl_id = m.create_client('Foo Bar', '23', 'address', 'mail', 'phone')
        cl_data = m.get_client('id', cl_id)[0]

        self.assertEqual('Foo Bar', cl_data['name'])
        self.assertEqual('23', cl_data['age'])
        self.assertEqual('address', cl_data['address'])
        self.assertEqual('mail', cl_data['mail'])
        self.assertEqual('phone', cl_data['phone'])

    def test_create_employee(self):
        m = Mediator(self.test_db)

        em_id = m.create_employee('Foo Bar', '23', 'address', 'mail', '3', )
        em_data = m.get_employee('id', em_id)[0]

        self.assertEqual('Foo Bar', em_data['name'])
        self.assertEqual('23', em_data['age'])
        self.assertEqual('3', em_data['position'])
        self.assertEqual('address', em_data['address'])
        self.assertEqual('mail', em_data['mail'])

    def test_create_task(self):
        m = Mediator(self.test_db)
        task_id = m.create_task('Underwater photos', 'ev123456', 'description', '123456', 'Medium')
        task_data = m.get_task('id', task_id)[0]

        self.assertEqual('Underwater photos', task_data['sub_team'])
        self.assertEqual('ev123456', task_data['event_id'])
        self.assertEqual('description', task_data['description'])
        self.assertEqual('123456', task_data['staff_id'])
        self.assertEqual('Medium', task_data['priority'])

    def test_create_event(self):
        m = Mediator(self.test_db)

        cl_id = m.create_client('Foo Bar 2', '23', 'address', 'mail', 'phone')
        event_id = m.create_client_req(cl_id, 'Super Party', 'description', '01-01-01', '02-02-02', 20, 100, 'deco',
                                       'filming', 'poster', 'food', 'music', 'computer', 'other', False)

        event_data = m.get_event('id', event_id)[0]
        self.assertEqual('Super Party', event_data['event_type'])
        self.assertEqual('description', event_data['description'])
        self.assertEqual('01-01-01', event_data['from_date'])
        self.assertEqual('02-02-02', event_data['to_date'])
        self.assertEqual(20, event_data['exp_no'])
        self.assertEqual(100, event_data['planned_budget'])
        self.assertEqual('deco', event_data['decorations'])
        self.assertEqual('filming', event_data['filming'])
        self.assertEqual('poster', event_data['poster'])
        self.assertEqual('food', event_data['food'])
        self.assertEqual('music', event_data['music'])
        self.assertEqual('computer', event_data['computer'])
        self.assertEqual('other', event_data['other'])

    def test_create_financial_req(self):
        m = Mediator(self.test_db)
        fin_req_id = m.create_financial_req('ev12345', 123456, 'reason', 'req_dpt')
        fin_req_data = m.get_financial_req('id', fin_req_id)[0]

        self.assertEqual('ev12345', fin_req_data['event_id'])
        self.assertEqual(123456, fin_req_data['req_amount'])
        self.assertEqual('reason', fin_req_data['reason'])
        self.assertEqual('req_dpt', fin_req_data['req_dpt'])

    def test_update_financial_req(self):
        m = Mediator(self.test_db)
        fin_req_id = m.create_financial_req('ev12345', 123456, 'reason', 'req_dpt')

        m.update_financial_req(fin_req_id, 'ev321', 321321, 'reason2', 'req_2')

        fin_req_data = m.get_financial_req('id', fin_req_id, all_data=False)[0]

        self.assertEqual('ev321', fin_req_data['event_id'])
        self.assertEqual(321321, fin_req_data['req_amount'])
        self.assertEqual('reason2', fin_req_data['reason'])
        self.assertEqual('req_2', fin_req_data['req_dpt'])

    def test_create_recruitment_req(self):
        m = Mediator(self.test_db)
        rec_req_id = m.create_recruitment_req('full time', 123456, 'title job','description1', 'financial')
        rec_req_data = m.get_recruitment_req('id', rec_req_id)[0]

        self.assertEqual('full time', rec_req_data['type'])
        self.assertEqual(123456, rec_req_data['years_exp'])
        self.assertEqual('title job', rec_req_data['title'])
        self.assertEqual('financial', rec_req_data['req_dpt'])
        self.assertEqual('description1', rec_req_data['description'])

    def test_update_recruitment_req(self):
        m = Mediator(self.test_db)
        rec_req_id = m.create_recruitment_req('full time', 123456, 'title job','description1', 'financial')

        m.update_recruitment_req(rec_req_id, 'part time', 54321, 'title job2', 'description2' ,'financial2')
        rec_req_data = m.get_recruitment_req('id', rec_req_id)[0]

        self.assertEqual('part time', rec_req_data['type'])
        self.assertEqual(54321, rec_req_data['years_exp'])
        self.assertEqual('title job2', rec_req_data['title'])
        self.assertEqual('financial2', rec_req_data['req_dpt'])
        self.assertEqual('description2', rec_req_data['description'])

    def test_update_task(self):
        m = Mediator(self.test_db)

        task_id = m.create_task('Aerial dancing', 'ev123456', 'description', 'em123456', 'High')

        m.update_task(task_id, 'Hot dancing', 'ev654321', 'description2', 'em9876543', 'Low')

        task_data = m.get_task('id', task_id, all_data=False)[0]

        self.assertEqual('Hot dancing', task_data['sub_team'])
        self.assertEqual('Low', task_data['priority'])
        self.assertEqual('ev654321', task_data['event_id'])
        self.assertEqual('description2', task_data['description'])
        self.assertEqual('em9876543', task_data['staff_id'])

    def test_update_event(self):
        m = Mediator(self.test_db)
        c = Controller(self.test_db)

        cl_id = m.create_client('Foo Bar 2', '23', 'address', 'mail', 'phone')
        cl_id_up = m.create_client('Foo Bar 3', '23', 'address', 'mail', 'phone')

        event_id = m.create_client_req(cl_id, 'Super Party', 'description', '01-01-01', '02-02-02', 20, 100, 'deco',
                                       'filming', 'poster', 'food', 'music', 'computer', 'other', False)

        m.update_event(event_id, cl_id_up, 'Dancing', 'description2', '01-01-03', '02-02-05', 30, 200, 'decos',
                       'filmings', 'posters', 'foods', 'musics', 'computers', 'others', False)

        event_data = c.get_event('id', event_id, all_data=False)[0]

        self.assertEqual('Dancing', event_data['event_type'])
        self.assertEqual('description2', event_data['description'])
        self.assertEqual('01-01-03', event_data['from_date'])
        self.assertEqual('02-02-05', event_data['to_date'])
        self.assertEqual(30, event_data['exp_no'])
        self.assertEqual(200, event_data['planned_budget'])
        self.assertEqual('decos', event_data['decorations'])
        self.assertEqual('filmings', event_data['filming'])
        self.assertEqual('posters', event_data['poster'])
        self.assertEqual('foods', event_data['food'])
        self.assertEqual('musics', event_data['music'])
        self.assertEqual('computers', event_data['computer'])
        self.assertEqual('others', event_data['other'])


if __name__ == '__main__':
    unittest.main()
