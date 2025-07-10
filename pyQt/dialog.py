import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog

layoutOption = 'QInputDialog'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chapter 06.01
        if(layoutOption == 'QInputDialog'):
            self.btn = QPushButton('Dialog', self)
            self.btn.move(30, 30)
            self.btn.clicked.connect(self.showDialog)

            self.le = QLineEdit(self)
            self.le.move(160, 35)

        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

    # chapter 06.01
    def showDialog(self):
        text, ok = QInputDialog.getText(self, layoutOption, 'Enter your name:')

        if ok:
            self.le.setText(str(text))
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())