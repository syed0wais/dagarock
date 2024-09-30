# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PythonFinance import Finance  # Ensure that this import points to your updated Finance class
import sys


class Worker(QtCore.QThread):
    # Signal to send data back to the main thread
    finished = QtCore.pyqtSignal()

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker

    def run(self):
        finance = Finance()
        finance.get_moving_avg(self.ticker)
        self.finished.emit()  # Emit signal when done


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Stock Genie")
        MainWindow.resize(803, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: rgb(35, 3, 36);")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(190, 50, 441, 461))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color: rgb(27, 56, 49);")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(90, 50, 281, 71))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setStyleSheet("color:yellow;")
        self.lineEdit.setGeometry(QtCore.QRect(80, 200, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(160, 290, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color:white;")
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.pressed)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stock Genie"))
        self.label.setText(_translate("MainWindow", "STOCK GENIE"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "TICKER SYMBOL"))
        self.pushButton.setText(_translate("MainWindow", "PREDICT"))

    def pressed(self):
        ticker = self.lineEdit.text()
        if ticker:
            self.start_worker(ticker)
        else:
            print("Please enter a ticker symbol.")

    def start_worker(self, ticker):
        self.worker = Worker(ticker)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self):
        print("Processing finished!")  # You can add more functionality here if needed


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
