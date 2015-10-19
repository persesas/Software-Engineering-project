import sys

from PyQt5.QtWidgets import QApplication, QWidget

from view.login_form import LoginForm
from test.gen_db_data import gen_db

# Testing stuff
# from view.event_req import ClientReq
# from view.task_req import TaskReq
# from view.manager_tabs import ManagerTabs
# from view.financial_req import FinancialReq
# from view.event_planning_req import EventPlanningReq
# from view.new_client_req import NewClientReq

if __name__ == '__main__':
    from view.mediator import get_mediator
    m = get_mediator()
    app = QApplication(sys.argv)

    #gen_db()
    m.login_form = LoginForm()

    sys.exit(app.exec_())