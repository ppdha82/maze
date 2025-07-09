import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QComboBox, QLineEdit, QProgressBar, QDial, QSlider, QSplitter, QFrame, QHBoxLayout, QGroupBox, QGridLayout, QMenu, QTabWidget, QCalendarWidget, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit, QTextBrowser, QTextEdit
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import Qt, QBasicTimer, QDate, QTime, QDateTime

layoutOption = 'QTextEdit' # 'QPushButton', 'QLabel'. 'QCheckBox', 'QRadioButton', 'QComboBox', 'QLineEdit', 'QProgressBar', 'QSlider_QDial', 'QSplitter', 'QGroupBox', 'QTabWidget', 'QPixmap', 'QCalendarWidget', 'QSpinBox', 'QDoubleSpinBox', 'QDateEdit', 'QTimeEdit', 'QDateTimeEdit', 'QTextBrowser'

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

        # chapter 05.10
        elif(layoutOption == 'QGroupBox'):
            grid = QGridLayout()
            grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
            grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
            grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
            grid.addWidget(self.createPushButtonGroup(), 1, 1)

            self.setLayout(grid)

        # chapter 05.11
        elif(layoutOption == 'QTabWidget'):
            grid = QGridLayout()
            grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
            grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
            grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
            grid.addWidget(self.createPushButtonGroup(), 1, 1)

            tab1 = QWidget()
            tab2 = QWidget()

            tab1.setLayout(grid)

            tabs = QTabWidget()
            tabs.addTab(tab1, 'Tab1')
            tabs.addTab(tab2, 'Tab2')

            vbox = QVBoxLayout()
            vbox.addWidget(tabs)

            self.setLayout(vbox)

        # chapter 05.12
        elif(layoutOption == 'QPixmap'):
            pixmap = QPixmap('landscape.jpg')
            
            lbl_img = QLabel()
            lbl_img.setPixmap(pixmap)
            lbl_size = QLabel('Width: ' + str(pixmap.width()) + ', Height: ' + str(pixmap.height()))
            lbl_size.setAlignment(Qt.AlignCenter)

            vbox = QVBoxLayout()
            vbox.addWidget(lbl_img)
            vbox.addWidget(lbl_size)
            self.setLayout(vbox)
        
        # chapter 05.13
        elif(layoutOption == 'QCalendarWidget'):
            cal = QCalendarWidget(self)
            cal.setGridVisible(True)
            cal.clicked[QDate].connect(self.showDate)

            self.lbl = QLabel(self)
            date = cal.selectedDate()
            self.lbl.setText(date.toString())

            vbox = QVBoxLayout()
            vbox.addWidget(cal)
            vbox.addWidget(self.lbl)

            self.setLayout(vbox)

        # chapter 05.14
        elif(layoutOption == 'QSpinBox'):
            self.lbl1 = QLabel('QSpinBox')
            self.spinbox = QSpinBox()
            self.spinbox.setMinimum(-10)
            self.spinbox.setMaximum(30)
            self.spinbox.setSingleStep(2)
            self.lbl2 = QLabel('0')

            self.spinbox.valueChanged.connect(self.value_changed)

            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl1)
            vbox.addWidget(self.spinbox)
            vbox.addWidget(self.lbl2)
            vbox.addStretch()

            self.setLayout(vbox)

        # chapter 05.15
        elif(layoutOption == 'QDoubleSpinBox'):
            self.lbl1 = QLabel('QDoubleSpinBox')
            self.dspinbox = QDoubleSpinBox()
            self.dspinbox.setRange(0, 100)
            self.dspinbox.setSingleStep(0.5)
            self.dspinbox.setPrefix('$ ')
            self.dspinbox.setDecimals(1)
            self.lbl2 = QLabel('$ 0.0')

            self.dspinbox.valueChanged.connect(self.value_changed_1)

            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl1)
            vbox.addWidget(self.dspinbox)
            vbox.addWidget(self.lbl2)
            vbox.addStretch()

            self.setLayout(vbox)

        # chapter 05.16
        elif(layoutOption == 'QDateEdit'):
            lbl = QLabel(layoutOption)

            dateedit = QDateEdit(self)
            dateedit.setDate(QDate.currentDate())
            dateedit.setMinimumDate(QDate(1900, 1, 1))
            dateedit.setMaximumDate(QDate(2100, 12, 31))
            # dateedit.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))

            vbox = QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(dateedit)
            vbox.addStretch()

            self.setLayout(vbox)

        # chapter 05.17
        elif(layoutOption == 'QTimeEdit'):
            lbl = QLabel(layoutOption)

            self.timeedit = QTimeEdit(self)
            self.timeedit.setTime(QTime.currentTime())
            self.timeedit.setTimeRange(QTime(3, 00, 00), QTime(23, 30, 00))
            self.timeedit.setDisplayFormat('hh:mm:ss')
            self.timer = QBasicTimer()
            self.timer.start(1000, self)

            vbox = QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(self.timeedit)
            vbox.addStretch()

            self.setLayout(vbox)

        # chapter 05.18
        elif(layoutOption == 'QDateTimeEdit'):
            lbl = QLabel(layoutOption)

            self.datetimeedit = QDateTimeEdit(self)
            self.datetimeedit.setDateTime(QDateTime.currentDateTime())
            self.datetimeedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00), QDateTime(2100, 1, 1, 00, 00, 00))
            self.datetimeedit.setDisplayFormat('yyyy.MM.dd hh:mm:ss')
            self.timer = QBasicTimer()
            self.timer.start(1000, self)

            vbox = QVBoxLayout()
            vbox.addWidget(lbl)
            vbox.addWidget(self.datetimeedit)
            vbox.addStretch()

            self.setLayout(vbox)
            
        # chapter 05.19
        elif(layoutOption == 'QTextBrowser'):
            self.le = QLineEdit()
            self.le.returnPressed.connect(self.append_text)

            self.tb = QTextBrowser()
            self.tb.setAcceptRichText(True)
            self.tb.setOpenExternalLinks(True)

            self.clear_btn = QPushButton('Clear')
            self.clear_btn.pressed.connect(self.clear_text)

            vbox = QVBoxLayout()
            vbox.addWidget(self.le, 0)
            vbox.addWidget(self.tb, 1)
            vbox.addWidget(self.clear_btn, 2)

            self.setLayout(vbox)

        # chapter 05.20
        elif(layoutOption == 'QTextEdit'):
            self.lbl1 = QLabel('Enter your sentence:')
            self.te = QTextEdit()
            self.te.setAcceptRichText(False)
            self.lbl2 = QLabel('The number of words is 0. Total letter is 0.')

            self.te.textChanged.connect(self.text_changed)

            vbox = QVBoxLayout()
            vbox.addWidget(self.lbl1)
            vbox.addWidget(self.te)
            vbox.addWidget(self.lbl2)
            vbox.addStretch()

            self.setLayout(vbox)
            pass
    
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

    # chapter 05.10
    def createFirstExclusiveGroup(self):
        groupbox = QGroupBox('Exclusive Radio Buttons')

        radio1 = QRadioButton('Radio1')
        radio2 = QRadioButton('Radio2')
        radio3 = QRadioButton('Radio3')
        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        groupbox.setLayout(vbox)

        return groupbox
    
    def createSecondExclusiveGroup(self):
        groupbox = QGroupBox('Exclusive Radio Buttons')
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        radio1 = QRadioButton('Radio1')
        radio2 = QRadioButton('Radio2')
        radio3 = QRadioButton('Radio3')
        radio1.setChecked(True)
        checkbox = QCheckBox('Independent Checkbox')
        checkbox.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addWidget(checkbox)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox
    
    def createNonExclusiveGroup(self):
        groupbox = QGroupBox('Non-Exclusive Checkboxes')
        groupbox.setFlat(True)

        checkbox1 = QCheckBox('Checkbox1')
        checkbox2 = QCheckBox('Checkbox2')
        checkbox2.setChecked(True)
        tristatebox = QCheckBox('Tri-state Button')
        tristatebox.setTristate(True)

        vbox = QVBoxLayout()
        vbox.addWidget(checkbox1)
        vbox.addWidget(checkbox2)
        vbox.addWidget(tristatebox)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox
    
    def createPushButtonGroup(self):
        groupbox = QGroupBox('Push Buttons')
        groupbox.setCheckable(True)
        groupbox.setChecked(True)

        pushbutton = QPushButton('Normal Button')
        togglebutton = QPushButton('Toggle Button')
        togglebutton.setCheckable(True)
        togglebutton.setChecked(True)
        flatbutton = QPushButton('Flat Button')
        flatbutton.setFlat(True)
        popupbutton = QPushButton('Popup Button')
        menu = QMenu(self)
        menu.addAction('First Item')
        menu.addAction('Second Item')
        menu.addAction('Third Item')
        menu.addAction('Fourth Item')
        popupbutton.setMenu(menu)

        vbox = QVBoxLayout()
        vbox.addWidget(pushbutton)
        vbox.addWidget(togglebutton)
        vbox.addWidget(flatbutton)
        vbox.addWidget(popupbutton)
        groupbox.setLayout(vbox)

        return groupbox
    
    # chapter 05.13
    def showDate(self, date):
        self.lbl.setText(date.toString())

    # chapter 05.14
    def value_changed(self):
        self.lbl2.setText(str(self.spinbox.value()))

    # chapter 05.15
    def value_changed_1(self):
        self.lbl2.setText('$ ' + str(self.dspinbox.value()))

    # chapter 05.17, 05.18
    def timerEvent(self, e):
        if(layoutOption == 'QTimeEdit'):
            self.timeedit.setTime(QTime.currentTime())
        elif(layoutOption == 'QDateTimeEdit'):
            self.datetimeedit.setDateTime(QDateTime.currentDateTime())

    # chapter 05.19
    def append_text(self):
        text = self.le.text()
        self.tb.setPlainText(text + "\n" + self.tb.toPlainText())
        # self.tb.append(text)
        self.le.clear()

    def clear_text(self):
        self.tb.clear()

    # chapter 05.20
    def text_changed(self):
        text = self.te.toPlainText()
        self.lbl2.setText('The number of words is ' + str(len(text.split())) + '. Total letter is ' + str(len(text)) + '.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())