import sys
from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.qbtn = QtGui.QPushButton('Quit', self)
        self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(50, 50)       
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')    
        self.show()
        
    def buttonPused(self):
        print "came here"
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

