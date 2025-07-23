import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygon
from PyQt5.QtCore import Qt, QPointF, QPoint, QRect, QSize
import numpy as np
from enum import Enum

layoutOption = 'drawPolygon'   # 'drawPoint', 'drawLine', 'drawRect', 'drawRoundedRect'

class Mode(Enum):
    normal = 0
    various = 1

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 660)
        self.setWindowTitle(layoutOption)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        # chapter 08.01
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
        # chapter 08.05
        elif layoutOption == 'drawPolygon':
            self.draw_polygon(qp)
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

    # chapter 08.02
    def draw_line(self, qp):
        self.setInitialData()
        self.runDrawShape(qp, Mode.normal)
        self.runDrawShape(qp, Mode.various)

    def applyOffset(self):
        # chapter 08.02
        if layoutOption == 'drawLine':
            self.linePos1 += self.offset
            self.linePos2 += self.offset
            self.textPos1 += self.offset

    # chapter 08.02 & 08.03 & 08.04 & 08.05
    def setInitialData(self):
        # chapter 08.02
        if layoutOption == 'drawLine':
            self.lineData = [ [QPen(Qt.blue, 8), QPoint(30, 230), QPoint(200, 50)], [QPen(Qt.green, 12), QPoint(140, 60), QPoint(320, 280)], [QPen(Qt.red, 16), QPoint(330, 250), QPoint(40, 190)] ]
            self.linePatternList = [ [Qt.SolidLine, 'Qt.SolidLine'], [Qt.DashLine, 'Qt.DashLine'], [Qt.DotLine, 'Qt.DotLine'], [Qt.DashDotLine, 'Qt.DashDotLine'],
                                     [Qt.DashDotDotLine, 'Qt.DashDotDotLine'], [Qt.CustomDashLine, 'Qt.CustomDashLine'] ]
            self.offset = QPoint(0, 50)
            self.center_x = int(self.width() / 2)
            self.linePos1 = QPoint(20 + self.center_x, 20)
            self.linePos2 = QPoint(380 + self.center_x, 20)
            self.textPos1 = QPoint(30 + self.center_x, 40)

        # chapter 08.03
        elif layoutOption == 'drawRect':
            self.count_x = 0
            self.offsetX = QPoint(160, 0)
            self.offsetY = QPoint(0, 100)
            self.center_x = int(self.width() / 2)
            self.leftTopPos = QPoint(20 + self.center_x, 10)
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.textPos = QPoint(20 + self.center_x, 90)
            self.startPos = QPoint(self.center_x, 0)
            self.patternList = [ [Qt.SolidPattern, 'Qt.SolidPattern'], [Qt.Dense1Pattern, 'Qt.Dense1Pattern'], [Qt.Dense2Pattern, 'Qt.Dense2Pattern'],
                                 [Qt.CrossPattern, 'Qt.CrossPattern'], [Qt.BDiagPattern, 'Qt.BDiagPattern'], [Qt.FDiagPattern, 'Qt.FDiagPattern'] ]
            self.rectData = [ [QColor(180, 100, 160), QPen(QColor(60, 60, 60), 3), QRect(20, 20, 100, 100)],
                            [QColor(40, 150, 20), QPen(Qt.blue, 2), QRect(180, 120, 50, 120)],
                            [Qt.yellow, QPen(Qt.red, 5), QRect(280, 30, 80, 120)] ]

        # chapter 08.04
        elif layoutOption == 'drawRoundedRect':
            self.count_x = 0
            self.count_stage = 1
            self.radius = QPointF(20.0, 15.0)
            self.center_x = int(self.width() / 2)
            self.center_y = int(self.height() / 2)
            self.offsetX = QPoint(160, 0)
            self.offsetY = QPoint(0, 100)
            self.leftTopPos = QPoint(20 + self.center_x, 10)
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.textPos = QPoint(self.center_x, 90)
            self.startPos = QPoint(self.center_x, 0)
            self.patternList = [ [Qt.SolidPattern, 'Qt.SolidPattern'], [Qt.Dense1Pattern, 'Qt.Dense1Pattern'], [Qt.Dense2Pattern, 'Qt.Dense2Pattern'],
                                 [Qt.CrossPattern, 'Qt.CrossPattern'], [Qt.BDiagPattern, 'Qt.BDiagPattern'], [Qt.FDiagPattern, 'Qt.FDiagPattern'] ]
            self.rectData = [ [QColor(180, 100, 160), QPen(QColor(60, 60, 60), 3), QRect(20, 20, 100, 100)],
                            [QColor(40, 150, 20), QPen(Qt.blue, 2), QRect(180, 120, 50, 120)],
                            [Qt.yellow, QPen(Qt.red, 5), QRect(280, 30, 80, 120)] ]
            
        # chapter 08.05
        elif layoutOption == 'drawPolygon':
            self.count_x = 0
            self.count_stage = 1
            self.offsetX = QPoint(160, 0)
            self.offsetY = QPoint(0, 100)
            self.center_x = int(self.width() / 2)
            self.center_y = int(self.height() / 2)
            self.leftTopPos = QPoint(20 + self.center_x, 10)
            self.textPos = QPoint(self.center_x, 90)
            self.startPos = QPoint(self.center_x, 0)
            self.rectInfo = QRect(self.leftTopPos, QSize(100, 60))
            self.rectData = [ [QPoint(30, 30), QPoint(90, 10), QPoint(70, 50), QPoint(40, 80)], [QPoint(230, 50), QPoint(190, 110), QPoint(130, 70), QPoint(150, 50)],
                              [QPoint(50, 250), QPoint(230, 230), QPoint(200, 330), QPoint(280, 410), QPoint(90, 420), QPoint(90, 300)], [QPoint(300, 50), QPoint(350, 50), QPoint(350, 100), QPoint(300, 100)],
                              [QPoint(380, 100), QPoint(380, 180), QPoint(450, 180), QPoint(450, 100)], [QPoint(100, 500), QPoint(190, 500), QPoint(190, 600), QPoint(100, 500)] ]
            self.brushData = [ [QColor(180, 100, 160), QPen(QColor(60, 60, 60), 3)],
                            [QColor(40, 150, 20), QPen(Qt.blue, 2)],
                            [Qt.yellow, QPen(Qt.red, 3)],
                            [Qt.cyan, QPen(Qt.gray, 5)],
                            [Qt.green, QPen(Qt.red, 2)],
                            [Qt.blue, QPen(Qt.black, 6)] ]
            self.patternList = [ [Qt.SolidPattern, 'Qt.SolidPattern'], [Qt.Dense1Pattern, 'Qt.Dense1Pattern'], [Qt.Dense2Pattern, 'Qt.Dense2Pattern'],
                                 [Qt.CrossPattern, 'Qt.CrossPattern'], [Qt.BDiagPattern, 'Qt.BDiagPattern'], [Qt.FDiagPattern, 'Qt.FDiagPattern'] ]

    def runDrawShape(self, qp, mode):
        # chapter 08.02
        if layoutOption == 'drawLine':
            if mode == Mode.normal:
                for index in range(len(self.lineData)):
                    qp.setPen(self.lineData[index][0])
                    qp.drawLine(self.lineData[index][1], self.lineData[index][2])
            else:
                for index in range(len(self.linePatternList)):
                    qp.setPen(QPen(Qt.black, 3, self.linePatternList[index][0]))
                    qp.drawLine(self.linePos1, self.linePos2)
                    qp.drawText(self.textPos1, self.linePatternList[index][1])
                    self.applyOffset()

        # chapter 08.03
        elif layoutOption == 'drawRect':
            if mode == Mode.normal:
                for d in self.rectData:
                    qp.setBrush(d[0])
                    qp.setPen(d[1])
                    qp.drawRect(d[2].topLeft().x(), d[2].topLeft().y(), d[2].size().width(), d[2].size().height())
            else:
                qp.setBrush(Qt.black)
                qp.setPen(QPen(Qt.black, 1))

                for p in range(len(self.patternList)):
                    qp.setBrush(QBrush(self.patternList[p][0]))
                    qp.drawRect(self.rectInfo)
                    qp.drawText(self.textPos, self.patternList[p][1])
                    self.applyOffsetInStage()

        # chapter 08.04
        elif layoutOption == 'drawRoundedRect':
            if mode == Mode.normal:
                for d in self.rectData:
                    qp.setBrush(d[0])
                    qp.setPen(d[1])
                    qp.drawRoundedRect(d[2].topLeft().x(), d[2].topLeft().y(), d[2].size().width(), d[2].size().height(), self.radius.x(), self.radius.y())
            else:
                qp.setBrush(Qt.black)
                qp.setPen(QPen(Qt.black, 1))

                for i in range(3):
                    for p in range(len(self.patternList)):
                        qp.setBrush(QBrush(self.patternList[p][0]))
                        qp.drawRoundedRect(self.rectInfo, self.radius.x(), self.radius.y())
                        qp.drawText(self.textPos, self.patternList[p][1] + str(self.count_stage))
                        self.applyOffsetInStage()
                    self.applyNextStageOffset()
                    radiusOffset = QPointF(25.0, 25.0)
                    self.radius += radiusOffset

        # chapter 08.05
        elif layoutOption == 'drawPolygon':
            if mode == Mode.normal:
                self.polygon = QPolygon()
                count = 0
                for r in self.rectData:
                    for p in range(len(r)):
                        self.polygon << r[p]
                    qp.setBrush(self.brushData[count][0])
                    qp.setPen(self.brushData[count][1])
                    if count % 2 == 1:
                        qp.drawPolygon(self.polygon, Qt.WindingFill)
                    else:
                        qp.drawPolygon(self.polygon, Qt.OddEvenFill)
                    count += 1
                    self.polygon = QPolygon()
            else:
                count = 0
                self.polygon = QPolygon()
                qp.setPen(QPen(Qt.black, 1))
                for r in self.rectData:
                    for p in range(len(r)):
                        offset = QPoint(0, 0)
                        if self.count_stage == 0:
                            pass
                        elif self.count_stage == 1:
                            offset += QPoint(self.center_x, 0)
                        elif self.count_stage == 2:
                            offset += QPoint(0, self.center_y)
                        else:
                            offset += QPoint(self.center_x, self.center_y)
                        self.polygon << r[p] + offset
                    qp.setBrush(QBrush(self.patternList[count][0]))
                    qp.drawPolygon(self.polygon, Qt.OddEvenFill)
                    qp.drawText(self.polygon.boundingRect().bottomLeft() + QPoint(0, 20), self.patternList[count][1] + str(self.count_stage))
                    self.applyOffsetInStage()
                    count += 1
                    self.polygon = QPolygon()
                self.applyNextStageOffset()

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

    # chapter 08.03
    def draw_rect(self, qp):
        self.setInitialData()
        self.runDrawShape(qp, Mode.normal)
        self.runDrawShape(qp, Mode.various)

    # chapter 08.04
    def draw_rounded_rect(self, qp):
        self.setInitialData()
        self.runDrawShape(qp, Mode.normal)
        self.runDrawShape(qp, Mode.various)

    def draw_normal_rounded_rect(self, qp):
        for d in self.rectData:
            qp.setBrush(d[0])
            qp.setPen(d[1])
            qp.drawRoundedRect(d[2].topLeft().x(), d[2].topLeft().y(), d[2].size().width(), d[2].size().height(), self.radius.x(), self.radius.y())

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

    # chapter 08.05
    def draw_polygon(self, qp):
        self.setInitialData()
        self.runDrawShape(qp, Mode.normal)
        self.runDrawShape(qp, Mode.various)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())