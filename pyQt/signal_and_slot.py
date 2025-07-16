import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QDial, QVBoxLayout, QHBoxLayout, QPushButton

layoutOption = 'Event_Handler'  # 'Signal_and_Slot'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chapter 07.01
        if layoutOption == 'Signal_and_Slot':
            lcd = QLCDNumber(self)
            dial = QDial(self)
            dial.setMaximum(100)

            vbox = QVBoxLayout()
            vbox.addWidget(lcd)
            vbox.addWidget(dial)
            self.setLayout(vbox)

            dial.valueChanged.connect(lcd.display)

        # chapter 07.02
        elif layoutOption == 'Event_Handler':
            lcd = QLCDNumber(self)
            dial = QDial(self)
            dial.setMaximum(100)
            btn1 = QPushButton('Big', self)
            btn2 = QPushButton('Small', self)

            hbox = QHBoxLayout()
            hbox.addWidget(btn1)
            hbox.addWidget(btn2)

            vbox = QVBoxLayout()
            vbox.addWidget(lcd)
            vbox.addWidget(dial)
            vbox.addLayout(hbox)
            self.setLayout(vbox)

            dial.valueChanged.connect(lcd.display)
            btn1.clicked.connect(self.resizeBig)
            btn2.clicked.connect(self.resizeSmall)

        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

    # chapter 07.02
    def resizeBig(self):
        self.resize(400, 500)

    def resizeSmall(self):
        self.resize(200, 250)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())