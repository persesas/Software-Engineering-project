from lib.auth import Authentication


class Controller():
    def __init__(self):
        pass

    def login(self, username, password):
        a = Authentication()
        return a.login(username, password)

