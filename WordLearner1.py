from PyQt4 import QtCore, QtGui, uic
import sys

class MyMainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('/home/pushkaraj.thorat_fedora/workspace/python/GREPrep/WordLearner.ui', self)
        print self.pushButton_3

app = QtGui.QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()
sys.exit(app.exec_())