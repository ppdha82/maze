import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QPoint, QRect, QSize
import numpy as np

layoutOption = 'drawRoundedRect'   # 'drawPoint', 'drawLine', 'drawRect'

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 660)
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
        # chapter 08.04
        elif layoutOption == 'drawRoundedRect':
            self.draw_rounded_rect(qp)
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
        self.setInitialData()
        self.draw_normal_rect(qp)
        self.draw_various_rect(qp)

    def setInitialData(self):
        if layoutOption == 'drawRect':
            self.count_x = 0
            self.offsetX = QPoint(160, 0)
            self.offsetY = QPoint(0, 100)
            self.center_x = int(self.width() / 2)
            self.leftTopPos = QPoint(20 + self.center_x, 10)
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.textPos = QPoint(20 + self.center_x, 90)
            self.patternList = [ Qt.SolidPattern, Qt.Dense1Pattern, Qt.Dense2Pattern, Qt.CrossPattern, Qt.BDiagPattern, Qt.FDiagPattern, ]
            self.patternStrList = [ 'Qt.SolidPattern', 'Qt.Dense1Pattern', 'Qt.Dense2Pattern', 'Qt.CrossPattern', 'Qt.BDiagPattern', 'Qt.FDiagPattern' ]
            self.colorData = [ [QColor(180, 100, 160), QPen(QColor(60, 60, 60), 3), QRect(20, 20, 100, 100)],
                        [QColor(40, 150, 20), QPen(Qt.blue, 2), QRect(180, 120, 50, 120)],
                        [Qt.yellow, QPen(Qt.red, 5), QRect(280, 30, 80, 120)] ]

        elif layoutOption == 'drawRoundedRect':
            self.radius = QPointF(20.0, 15.0)
            self.center_x = int(self.width() / 2)
            self.center_y = int(self.height() / 2)
            self.offsetX = QPoint(160, 0)
            self.offsetY = QPoint(0, 100)
            self.leftTopPos = QPoint(20 + self.center_x, 10)
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.textPos = QPoint(self.center_x, 90)
            self.startPos = QPoint(self.center_x, 0)
            self.patternList = [ Qt.SolidPattern, Qt.Dense1Pattern, Qt.Dense2Pattern, Qt.CrossPattern, Qt.BDiagPattern, Qt.FDiagPattern, ]
            self.patternStrList = [ 'Qt.SolidPattern', 'Qt.Dense1Pattern', 'Qt.Dense2Pattern', 'Qt.CrossPattern', 'Qt.BDiagPattern', 'Qt.FDiagPattern' ]
            self.colorData = [ [QColor(180, 100, 160), QPen(QColor(60, 60, 60), 3), QRect(20, 20, 100, 100)],
                        [QColor(40, 150, 20), QPen(Qt.blue, 2), QRect(180, 120, 50, 120)],
                        [Qt.yellow, QPen(Qt.red, 5), QRect(280, 30, 80, 120)] ]

    def run_draw_rect(self, qp, data):
        qp.setBrush(data[0])
        qp.setPen(data[1])
        qp.drawRect(data[2].topLeft().x(), data[2].topLeft().y(), data[2].size().width(), data[2].size().height())
        pass

    def draw_normal_rect(self, qp):
        for d in self.colorData:
            self.run_draw_rect(qp, d)

    def draw_various_rect(self, qp):
        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.black, 1))

        for p in range(len(self.patternList)):
            self.drawRectAndText(qp, self.patternList[p], self.patternStrList[p])
            self.applyOffset()

    def drawRectAndText(self, qp, patternStyle, text):
        qp.setBrush(QBrush(patternStyle))
        qp.drawRect(self.rectInfo)
        qp.drawText(self.textPos, text)

    # chapter 08.04
    def draw_rounded_rect(self, qp):
        self.setInitialData()

        self.draw_normal_rounded_rect(qp)
        self.draw_various_rounded_rect(qp)

    def draw_normal_rounded_rect(self, qp):
        for d in self.colorData:
            self.run_draw_rect_for_rounded(qp, d)

    def run_draw_rect_for_rounded(self, qp, data):
        qp.setBrush(data[0])
        qp.setPen(data[1])
        qp.drawRoundedRect(data[2].topLeft().x(), data[2].topLeft().y(), data[2].size().width(), data[2].size().height(), self.radius.x(), self.radius.y())
        pass

    def draw_various_rounded_rect(self, qp):
        self.count_x = 0
        self.count_stage = 1

        qp.setBrush(Qt.black)
        qp.setPen(QPen(Qt.black, 1))

        for i in range(3):
            self.draw_various_rounded_rect_with_pattern(qp)
            self.applyNextStageOffset()
            self.applyNewRadius()

    def updatePosition(self):
        self.leftTopPos = QPoint(20 + self.startPos.x(), 10 + self.startPos.y())
        self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
        self.textPos = QPoint(self.startPos.x(), self.leftTopPos.y() + 80)

    def applyNextStageOffset(self):
        if self.count_stage % 2 == 1:
            # 좌측 하단으로 이동
            self.startPos.setX(20)
            self.startPos += QPoint(0, self.center_y)
        else:
            # 우측 이동
            self.startPos.setX(20 + self.center_x)
        self.updatePosition()
        self.count_x = 0
        self.count_stage += 1

    def applyNewRadius(self):
        radiusOffset = QPointF(25.0, 25.0)
        self.radius += radiusOffset

    def applyOffsetInStage(self):
        self.count_x += 1
        if self.count_x % 3 == 0:
            # 촤측 하단 이동
            self.leftTopPos = QPoint(20 + self.startPos.x(), 10 + self.startPos.y()) + self.offsetY
                
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.textPos.setX(self.startPos.x())
            self.textPos += self.offsetY
        else:
            # 우측 이동
            self.leftTopPos += self.offsetX
            self.rectInfo.moveTopLeft(self.leftTopPos)
            self.textPos += self.offsetX

    def draw_various_rounded_rect_with_pattern(self, qp):
        for p in range(len(self.patternList)):
            self.drawRoundedRectAndText(qp, self.patternList[p], self.patternStrList[p] + str(self.count_stage))
            self.applyOffsetInStage()
        return

    def drawRoundedRectAndText(self, qp, patternStyle, text):
        qp.setBrush(QBrush(patternStyle))
        qp.drawRoundedRect(self.rectInfo, self.radius.x(), self.radius.y())
        qp.drawText(self.textPos, text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())