import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QFrame, QColorDialog, QFontDialog, QVBoxLayout, QSizePolicy, QLabel
from PyQt5.QtGui import QColor

layoutOption = 'QFontDialog'   # 'QInputDialog', 'QColorDialog'

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

        # chapter 06.02
        elif(layoutOption == 'QColorDialog'):
            col = QColor(0, 0, 0)

            self.btn = QPushButton('Dialog', self)
            self.btn.move(30, 30)
            self.btn.clicked.connect(self.showDialog)

            self.frm = QFrame(self)
            self.frm.setStyleSheet('QWidget { background-color: %s }' % col.name())
            self.frm.setGeometry(160, 35, 100, 100)

        # chapter 06.03
        elif(layoutOption == 'QFontDialog'):
            btn = QPushButton('Dialog', self)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.move(20, 20)
            btn.clicked.connect(self.showDialog)

            vbox = QVBoxLayout()
            vbox.addWidget(btn)

            self.lbl = QLabel('The quick brown fox jumps over the lazy dog', self)
            self.lbl.move(160, 20)
            self.font = self.lbl.font()

            vbox.addWidget(self.lbl)
            self.setLayout(vbox)
            pass

        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

    # chapter 06.01, 06.02, 06.03
    def showDialog(self):
        if(layoutOption == 'QInputDialog'):
            text, ok = QInputDialog.getText(self, layoutOption, 'Enter your name:')

            if ok:
                self.le.setText(str(text))
        elif(layoutOption == 'QColorDialog'):
            col = QColorDialog.getColor()

            if(col.isValid()):
                self.frm.setStyleSheet('QWidget { background-color: %s }' % col.name())
        elif(layoutOption == 'QFontDialog'):
            font, ok = QFontDialog.getFont(self.lbl.font())

            if ok:
                self.lbl.setFont(font)
                self.fontInfo = font
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())