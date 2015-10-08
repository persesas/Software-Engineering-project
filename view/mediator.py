from controller import Controller

from view.base_template import Base
from view.login_form import LoginForm
from view.manager_tabs import ManagerTabs

class Mediator():

    base = None

    def __init__(self):
        pass

    def check_credentials(self, username, password):
        c = Controller()
        return c.login(username, password)

    def login(self):
        self.base = Base()
        l = LoginForm()
        l2 = LoginForm()
        self.m = ManagerTabs({"tab1": l, "tab2": l2})
        self.base.set_central_widget(self.m)

def get_mediator(_instance=Mediator()):
    return _instance

