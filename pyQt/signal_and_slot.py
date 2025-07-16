import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QDial, QVBoxLayout

layoutOption = 'Signal_and_Slot'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        if layoutOption == 'Signal_and_Slot':
            lcd = QLCDNumber(self)
            dial = QDial(self)

            vbox = QVBoxLayout()
            vbox.addWidget(lcd)
            vbox.addWidget(dial)
            self.setLayout(vbox)

            dial.valueChanged.connect(lcd.display)

        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())