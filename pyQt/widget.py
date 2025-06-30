import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QComboBox, QLineEdit, QProgressBar, QDial, QSlider, QSplitter, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QBasicTimer

layoutOption = 'QSplitter' # 'QPushButton', 'QLabel'. 'QCheckBox', 'QRadioButton', 'QComboBox', 'QLineEdit', 'QProgressBar', 'QSlider_QDial'
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # chapter 05.01
        if(layoutOption == 'QPushButton'):
            btn1 = QPushButton('&Button1', self)
            btn1.setCheckable(True)
            btn1.toggle()

            btn2 = QPushButton(self)
            btn2.setText('Button&2')

            btn3 = QPushButton(self)
            btn3.setEnabled(False)

            vbox = QVBoxLayout()
            vbox.addWidget(btn1)
            vbox.addWidget(btn2)
            vbox.addWidget(btn3)

            self.setLayout(vbox)

        # chapter 05.02
        elif(layoutOption == 'QLabel'):
            label1 = QLabel('First Label', self)
            label1.setAlignment(Qt.AlignCenter)

            label2 = QLabel('Second Label', self)
            label2.setAlignment(Qt.AlignVCenter)

            font1 = label1.font()
            font1.setPointSize(20)

            font2 = label2.font()
            font2.setFamily('Times New Roman')
            font2.setBold(True)

            label1.setFont(font1)
            label2.setFont(font2)

            layout = QVBoxLayout()
            layout.addWidget(label1)
            layout.addWidget(label2)

            self.setLayout(layout)

        # chpater 05.03
        elif(layoutOption == 'QCheckBox'):
            cb = QCheckBox('Show Title', self)
            cb.move(20, 20)
            cb.toggle()
            cb.stateChanged.connect(self.changeTitle)

        # chpater 05.04
        elif(layoutOption == 'QRadioButton'):
            rbtn1 = QRadioButton('First Button', self)
            rbtn1.move(50, 50)
            rbtn1.setChecked(True)

            rbtn2 = QRadioButton(self)
            rbtn2.move(50, 70)
            rbtn2.setText('Second Button')

        # chapter 05.05
        elif(layoutOption == 'QComboBox'):
            self.lbl = QLabel('Option1', self)
            self.lbl.move(50, 150)

            cb = QComboBox(self)
            cb.addItem('Option1')
            cb.addItem('Option2')
            cb.addItem('Option3')
            cb.addItem('Option4')
            cb.move(50, 50)

            cb.activated[str].connect(self.onActivated)

        # chapter 05.06
        elif(layoutOption == 'QLineEdit'):
            self.lbl = QLabel(self)
            self.lbl.move(60, 40)

            qle = QLineEdit(self)
            qle.move(60, 100)
            qle.textChanged[str].connect(self.onChanged)

        # chapter 05.07
        elif(layoutOption == 'QProgressBar'):
            self.pbar = QProgressBar(self)
            self.pbar.setGeometry(30, 40, 200, 25)

            self.btn = QPushButton('Start', self)
            self.btn.move(40, 80)
            self.btn.clicked.connect(self.doAction)

            self.timer = QBasicTimer()
            self.step = 0

        # chapter 05.08
        elif(layoutOption == 'QSlider_QDial'):
            self.slider = QSlider(Qt.Horizontal, self)
            self.slider.move(30, 30)
            self.slider.setRange(0, 50)
            self.slider.setSingleStep(2)

            self.dial = QDial(self)
            self.dial.move(30, 50)
            self.dial.setRange(0, 50)
            self.dial.setNotchesVisible(True)

            btn = QPushButton('Default',self)
            btn.move(35, 160)

            self.slider.valueChanged.connect(self.dial.setValue)
            self.dial.valueChanged.connect(self.slider.setValue)
            btn.clicked.connect(self.button_clicked)

        # chapter 05.09
        elif(layoutOption == 'QSplitter'):
            hbox = QHBoxLayout()

            top = QFrame()
            top.setFrameShape(QFrame.Box)

            midLeft = QFrame()
            midLeft.setFrameShape(QFrame.StyledPanel)

            midRight = QFrame()
            midRight.setFrameShape(QFrame.Panel)

            bottom = QFrame()
            bottom.setFrameShape(QFrame.WinPanel)
            bottom.setFrameShadow(QFrame.Sunken)

            splitter1 = QSplitter(Qt.Horizontal)
            splitter1.addWidget(midLeft)
            splitter1.addWidget(midRight)

            splitter2 = QSplitter(Qt.Vertical)
            splitter2.addWidget(top)
            splitter2.addWidget(splitter1)
            splitter2.addWidget(bottom)

            hbox.addWidget(splitter2)
            self.setLayout(hbox)
    
        self.setWindowTitle(layoutOption)
        self.setGeometry(300, 300, 500, 200)
        self.show()

    # chapter 05.03
    def changeTitle(self, state):
        if(state == Qt.Checked):
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')
    
    # chpater 05.04
    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    # chapter 05.06
    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    # chapter 05.07
    def timerEvent(self, e):
        if(self.step >= 100):
            self.timer.stop()
            self.btn.setText('Finished')
            return
        
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if(self.timer.isActive()):
            self.timer.stop()
            self.btn.setText('Start')
        else:
            if(self.btn.text() == 'Finished'):
                self.step = 0
                self.btn.setText('Start')
                self.pbar.setValue(self.step)
            else:
                self.timer.start(100, self)
                self.btn.setText('Stop')

    # chapter 05.08
    def button_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())