import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLCDNumber, QDial, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QObject, pyqtSignal

layoutOption = 'Emitting_Signal'  # 'Signal_and_Slot', 'Event_Handler', 'Rebuilding_Event_Handler', 'Rebuilding_Event_Handler2'

# chapter 07.05
class Communicate(QObject):
    closeApp = pyqtSignal()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.color_index = 0
        self.colors = ["background-color: red", "background-color: green", "background-color: blue", "background-color: white"]
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

        # chapter 07.03
        elif layoutOption == 'Rebuilding_Event_Handler':
            pass

        # chapter 07.04
        elif layoutOption == 'Rebuilding_Event_Handler2':
            x = 0
            y = 0

            self.text = 'x: {0}, y: {1}'.format(x, y)
            self.label = QLabel(self.text, self)
            self.label.move(20, 20)

            self.setMouseTracking(True)

        # chapter 07.05
        elif layoutOption == 'Emitting_Signal':
            self.c = Communicate()
            self.c.closeApp.connect(self.close)
            pass

        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

    # chapter 07.02
    def resizeBig(self):
        self.resize(400, 500)

    def resizeSmall(self):
        self.resize(200, 250)

    # chapter 07.03
    def keyPressEvent(self, e):
        if layoutOption == 'Rebuilding_Event_Handler2':
            if e.key() == Qt.Key_Escape:
                reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.close()
            elif e.key() == Qt.Key_F:
                self.showFullScreen()
            elif e.key() == Qt.Key_N:
                self.showNormal()

    # chapter 07.04
    def mouseMoveEvent(self, e):
        if layoutOption == 'Rebuilding_Event_Handler2':
            x = e.x()
            y = e.y()

            text = 'x: {0}, y: {1}'.format(x, y)
            self.label.setText(text)
            self.label.adjustSize()
    
    def mouseReleaseEvent(self, e):
        if layoutOption == 'Rebuilding_Event_Handler2':
            if e.button() == Qt.LeftButton:
                self.color_index = (self.color_index + 1) % len(self.colors)
                self.setStyleSheet(self.colors[self.color_index])
                if self.color_index == (len(self.colors) - 1):
                    self.label.setStyleSheet("color: black")
                else:
                    self.label.setStyleSheet("color: white")
        pass

    # chpater 07.05
    def mousePressEvent(self, e):
        if layoutOption == 'Emitting_Signal':
            self.c.closeApp.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())