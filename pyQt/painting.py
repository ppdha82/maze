import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, QPoint
import numpy as np

layoutOption = 'drawLine'   # 'drawPoint'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chapter 08.01
        if layoutOption == 'drawPoint':
            pass

        # chapter 08.02
        elif layoutOption == 'drawLine':
            pass
            
        self.setGeometry(300, 300, 800, 300)
        self.setWindowTitle(layoutOption)
        self.show()

    def paintEvent(self, e):
        # chapter 08.01
        qp = QPainter()
        qp.begin(self)
        if layoutOption == 'drawPoint':
            self.draw_point(qp)
        # chapter 08.02
        elif layoutOption == 'drawLine':
            self.draw_line(qp)
        qp.end()

    # chapter 08.01
    def draw_point(self, qp):
        pen = QPen()
        colors = [ '#D83C5F', '#3CD88F', '#AA5CE3', '#DF4A26', '#AE85F6', '#F7A82E', '#406CF3', '#E9F229', '#29ACF2' ]

        for i in range(1000):
            pen.setWidth(np.random.randint(1, 15))
            pen.setColor(QColor(np.random.choice(colors)))
            qp.setPen(pen)
            rand_x = 100 * np.random.randn()
            rand_y = 100 * np.random.randn()
            qp.drawPoint(QPointF(self.width() / 2 + rand_x, self.height() / 2 + rand_y))

        qp.setPen(QPen(Qt.blue, 8))
        qp.drawPoint(int(self.width() / 2), int(self.height() / 2))

        pass
    # chapter 08.02
    def draw_line(self, qp):
        qp.setPen(QPen(Qt.blue, 8))
        qp.drawLine(30, 230, 200, 50)
        qp.setPen(QPen(Qt.green, 12))
        qp.drawLine(140, 60, 320, 280)
        qp.setPen(QPen(Qt.red, 16))
        qp.drawLine(330, 250, 40, 190)

        self.draw_various_line(qp)

    def draw_various_line(self, qp):
        self.offset = QPoint(0, 50)
        self.center_x = int(self.width() / 2)
        self.linePos1 = QPoint(20 + self.center_x, 20)
        self.linePos2 = QPoint(380 + self.center_x, 20)
        self.textPos1 = QPoint(30 + self.center_x, 40)

        self.drawLineAndText(qp, Qt.SolidLine, 'Qt.SolidLine')

        self.applyOffset()
        self.drawLineAndText(qp, Qt.DashLine, 'Qt.DashLine')

        self.applyOffset()
        self.drawLineAndText(qp, Qt.DotLine, 'Qt.DotLine')

        self.applyOffset()
        self.drawLineAndText(qp, Qt.DashDotLine, 'Qt.DashDotLine')

        self.applyOffset()
        self.drawLineAndText(qp, Qt.DashDotDotLine, 'Qt.DashDotDotLine')

        self.applyOffset()
        self.drawLineAndText(qp, Qt.CustomDashLine, 'Qt.CustomDashLine')

        pass

    def drawLineAndText(self, qp, penStyle, text):
        qp.setPen(QPen(Qt.black, 3, penStyle))
        qp.drawLine(self.linePos1, self.linePos2)
        qp.drawText(self.textPos1, text)

    def applyOffset(self):
        self.linePos1 += self.offset
        self.linePos2 += self.offset
        self.textPos1 += self.offset
        pass
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())