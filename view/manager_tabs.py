from PyQt5 import QtWidgets


class ManagerTabs(QtWidgets.QWidget):
    def __init__(self, tab_names):
        super().__init__()
        self.tab_names = tab_names
        self.initUI()

    def initUI(self):
        # Initialize tab widgets

        self.tabs = QtWidgets.QTabWidget()
        for name, w in self.tab_names.items():
            self.tabs.addTab(w, name)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.show()