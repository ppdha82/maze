import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit

layoutOption = 'QGridLayout' # BoxQLayout
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chap 04.01
        label1 = QLabel('Label1', self)
        label1.move(20, 20)
        label2 = QLabel('Label2', self)
        label2.move(20, 60)

        btn1 = QPushButton('Button1', self)
        btn1.move(80, 13)
        btn2 = QPushButton('Button2', self)
        btn2.move(80, 53)

        # chap 04.02
        if(layoutOption == 'BoxLayout'):
            okButton = QPushButton('OK')
            cancelButton = QPushButton('Cancel')

            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(okButton)
            hbox.addWidget(cancelButton)
            hbox.addStretch(1)

            vbox = QVBoxLayout()
            vbox.addStretch(1)
            vbox.addLayout(hbox)
            vbox.addStretch(1)

            self.setLayout(vbox)

        # chap 04.03
        elif(layoutOption == 'QGridLayout'):
            grid = QGridLayout()
            self.setLayout(grid)

            grid.addWidget(QLabel('Title:'), 0, 0)
            grid.addWidget(QLabel('Author:'), 1, 0)
            grid.addWidget(QLabel('Review:'), 2, 0)

            grid.addWidget(QLineEdit(), 0, 1)
            grid.addWidget(QLineEdit(), 1, 1)
            grid.addWidget(QLineEdit(), 2, 1)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 500, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
