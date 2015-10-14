import sys

from PyQt5.QtWidgets import QApplication, QWidget

from view.login_form import LoginForm
from test.gen_db_data import gen_db
from view.client_req import ClientReq
from view.task_req import TaskReq
# Testing stuff
# from view.manager_tabs import ManagerTabs
# from view.financial_req import FinancialReq
# from view.event_planning_req import EventPlanningReq

# from view.new_client_req import NewClientReq

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gen_db()
    l = TaskReq("1","2", "3")
    sys.exit(app.exec_())