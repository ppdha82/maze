import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QStatusBar, QMainWindow, QLabel, QAction, qApp, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, Qt

statusBarOption = 1 # != 1
window_option = 'QWidget' # 'QMainwindow'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # chap 5
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.initUI()

    def initUI(self):
        # chap 5
        if statusBarOption == 1:
            self.statusBar.showMessage('Ready')
        else:
            self.label = QLabel('StatusBar Button')
            self.statusBar.addWidget(self.label)

        # chap 6
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        # chap 7
        self.toolbar = self.addToolBar('Toolbar')

        saveAction = QAction(QIcon('save.png'), 'Save', self)
        saveAction.setStatusTip('Saving')
        self.toolbar.addAction(saveAction)

        editAction = QAction(QIcon('edit.png'), 'Edit', self)
        editAction.setStatusTip('Editing')
        self.toolbar.addAction(editAction)

        printAction = QAction(QIcon('print.png'), 'Print', self)
        printAction.setStatusTip('Printing')
        self.toolbar.addAction(printAction)

        self.toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Toolbar')


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chap 4
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('this is a <b>QWidget</b> widget')

        # chap 3
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        # chap 2
        self.setWindowTitle('Tooltips')
        self.setWindowIcon(QIcon('web.png'))

        # chap 8
        # self.setGeometry(300, 300, 500, 400)
        self.resize(500, 350)
        self.center()
        self.show()

    # chap 8
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if window_option == 'QMainwindow':
        mainWindow = MainWindow()
        mainWindow.show()
    else:
        ex = MyApp()

    sys.exit(app.exec_())