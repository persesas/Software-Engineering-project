from controller import Controller


def login(username, password):
    c = Controller()
    return c.login(username, password)
