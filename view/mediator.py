from controller import Controller

from view.base_template import Base
from view.login_form import LoginForm


class Mediator():

    base = None

    def __init__(self):
        pass

    def check_credentials(self, username, password):
        c = Controller()
        return c.login(username, password)

    def login(self):
        self.base = Base()
        self.base.set_central_widget(LoginForm())

def get_mediator(_instance=Mediator()):
    return _instance

