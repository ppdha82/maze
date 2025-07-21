import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QPoint, QRect, QSize
import numpy as np

layoutOption = 'drawRect'   # 'drawPoint', 'drawLine'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 300)
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
        # chapter 08.03
        elif layoutOption == 'drawRect':
            self.draw_rect(qp)
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

    def drawLineAndText(self, qp, penStyle, text):
        qp.setPen(QPen(Qt.black, 3, penStyle))
        qp.drawLine(self.linePos1, self.linePos2)
        qp.drawText(self.textPos1, text)

    def applyOffset(self):
        # chapter 08.02
        if layoutOption == 'drawLine':
            self.linePos1 += self.offset
            self.linePos2 += self.offset
            self.textPos1 += self.offset
            pass

        # chapter 08.03
        elif layoutOption == 'drawRect':
            self.count_x += 1
            if self.count_x == 3:
                self.leftTopPos = QPoint(20 + self.center_x, 10) + self.offsetY
                self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
                self.textPos.setX(20 + self.center_x)
                self.textPos += self.offsetY
                pass
            else:
                self.leftTopPos += self.offsetX
                self.rectInfo.moveTopLeft(self.leftTopPos)
                self.textPos.setX(self.textPos.x() + 160)

    # chapter 08.03
    def draw_rect(self, qp):
        qp.setBrush(QColor(180, 100, 160))
        qp.setPen(QPen(QColor(60, 60, 60), 3))
        qp.drawRect(20, 20, 100, 100)

        qp.setBrush(QColor(40, 150, 20))
        qp.setPen(QPen(Qt.blue, 2))
        qp.drawRect(180, 120, 50, 120)

        qp.setBrush(Qt.yellow)
        qp.setPen(QPen(Qt.red, 5))
        qp.drawRect(280, 30, 80, 40)

        self.draw_various_rect(qp)

    def draw_various_rect(self, qp):
        self.count_x = 0
        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.black, 1))

        self.offsetX = QPoint(160, 0)
        self.offsetY = QPoint(0, 100)
        self.center_x = int(self.width() / 2)
        self.leftTopPos = QPoint(20 + self.center_x, 10)
        self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
        self.textPos = QPoint(20 + self.center_x, 90)

        self.drawRectAndText(qp, Qt.SolidPattern, 'Qt.SolidPattern')

        self.applyOffset()
        self.drawRectAndText(qp, Qt.Dense1Pattern, 'Qt.Dense1Pattern')

        self.applyOffset()
        self.drawRectAndText(qp, Qt.Dense2Pattern, 'Qt.Dense2Pattern')

        self.applyOffset()
        self.drawRectAndText(qp, Qt.CrossPattern, 'Qt.CrossPattern')

        self.applyOffset()
        self.drawRectAndText(qp, Qt.BDiagPattern, 'Qt.BDialPattern')

        self.applyOffset()
        self.drawRectAndText(qp, Qt.FDiagPattern, 'Qt.FDialPattern')
        pass

    def drawRectAndText(self, qp, patternStyle, text):
        qp.setBrush(QBrush(patternStyle))
        qp.drawRect(self.rectInfo)
        qp.drawText(self.textPos, text)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())