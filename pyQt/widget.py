import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt

layoutOption = 'QLineEdit' # 'QPushButton', 'QLabel'. 'QCheckBox', 'QRadioButton', 'QComboBox'
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
            self.setWindowTitle('QPushButton')

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
            self.setWindowTitle('QLabel')

        # chpater 05.03
        elif(layoutOption == 'QCheckBox'):
            cb = QCheckBox('Show Title', self)
            cb.move(20, 20)
            cb.toggle()
            cb.stateChanged.connect(self.changeTitle)

            self.setWindowTitle('QCheckBox')

        # chpater 05.04
        elif(layoutOption == 'QRadioButton'):
            rbtn1 = QRadioButton('First Button', self)
            rbtn1.move(50, 50)
            rbtn1.setChecked(True)

            rbtn2 = QRadioButton(self)
            rbtn2.move(50, 70)
            rbtn2.setText('Second Button')

            self.setWindowTitle('QRadioButton')

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

            self.setWindowTitle('QComboBox')

        # chapter 05.06
        elif(layoutOption == 'QLineEdit'):
            self.lbl = QLabel(self)
            self.lbl.move(60, 40)

            qle = QLineEdit(self)
            qle.move(60, 100)
            qle.textChanged[str].connect(self.onChanged)

            self.setWindowTitle('QLineEdit')
    
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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())