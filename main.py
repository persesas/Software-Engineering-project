import sys

from PyQt5.QtWidgets import QApplication, QWidget

from view.login_form import LoginForm
from test.gen_db_data import gen_db

# Testing stuff
# from view.manager_tabs import ManagerTabs
# from view.event_planning_req import EventPlanningReq
# from view.client_req import ClientReq
from view.new_client_req import NewClientReq

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gen_db()
    l = NewClientReq()
    sys.exit(app.exec_())