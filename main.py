import sys

from PyQt5.QtWidgets import QApplication, QWidget

from view.login_form import LoginForm
from test.gen_db_data import gen_db

# Testing stuff
# from view.manager_tabs import ManagerTabs
# from view.event_planning_req import EventPlanningReq
# from view.client_req import ClientReq


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gen_db()
    l = LoginForm()
    sys.exit(app.exec_())