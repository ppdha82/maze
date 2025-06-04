import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

option = 1
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.initUI()

    def initUI(self):
        if option == 1:
            self.statusBar.showMessage('Ready')
        else:
            self.label = QLabel('StatusBar Button')
            self.statusBar.addWidget(self.label)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Status Window')


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusbar = QStatusBar(self)
        # self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('this is a <b>QWidget</b> widget')

        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('Tooltips')
        self.setWindowIcon(QIcon('web.png'))
        self.setGeometry(300, 300, 500, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # ex = MyApp()
    sys.exit(app.exec_())