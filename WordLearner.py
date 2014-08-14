import sys
from PyQt4 import Qt, QtGui, QtCore
import pyaudio
import wave
import threading
import os
import time
import subprocess


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 4410
MEANINGFILE="meaning.mp3"
SENTENCES="sentences.mp3"

class WordLearner(QtGui.QWidget):

    def __init__(self):
        super(WordLearner, self).__init__()
        self.addWidgets()
        self.rootDir="/home/pushkaraj.thorat_fedora/Desktop/gre/stepLearning/"
        self.meaningR.pressed.connect(self.meaningPressed)
        self.meaningR.released.connect(self.meaningReleased)

        self.sentenceR.pressed.connect(self.sentencePressed)
        self.sentenceR.released.connect(self.sentenceReleased)
        self.leftButton.clicked.connect(self.previous)
        self.rightButton.clicked.connect(self.next)
        
        self.meaningP.clicked.connect(self.meaningPlay)
        self.sentenceP.clicked.connect(self.sentencesPlay)
        
        self.dirList=os.listdir(self.rootDir)
        self.wordIndex=0
        self.showWord()
    
    def previous(self):
        self.wordIndex = (self.wordIndex - 1 + len(self.dirList)) % len(self.dirList);
        self.showWord()
        
    def next(self):
        self.wordIndex=(self.wordIndex + 1) % len(self.dirList);
        self.showWord()
        
    def getCurrentWordPath(self):
        return str(self.rootDir + self.dirList[self.wordIndex] + "/")
        
    def showWord(self):
        self.wordLabel.setText("<b>"+self.dirList[self.wordIndex]+"</b>")
        self.meaningLabel.setText(open(self.getCurrentWordPath()+"meaning").read())
        self.sentenceLabel.setText(open(self.getCurrentWordPath()+"sentences").read())
        self.statusLabel.setText(str(self.wordIndex+1) + '/' + str(len(self.dirList)))
 
    def addWidgets(self):
        self.leftButton = Qt.QPushButton("<<",self)
        self.rightButton = Qt.QPushButton(">>", self)
         
        self.wordLabel = Qt.QLabel("word", self);#Qt.QLineEdit() #Qt.QLabel("word", self);
#         self.wordLabel.setStyleSheet("QLabel { background-color : yellow; color : blue; }")
        
        self.meaningLabel = Qt.QTextEdit("meaning and \n pronouncation", self);
        self.meaningLabel.setStyleSheet("QLabel { background-color : yellow; color : blue; }")
        
        self.sentenceLabel = Qt.QTextEdit("sentences", self);
        self.sentenceLabel.setStyleSheet("QLabel { background-color : yellow; color : blue; }")
        
        self.statusLabel = Qt.QLabel("sentences", self);
        
        self.meaningR = Qt.QPushButton("r", self);
        self.sentenceR = Qt.QPushButton("r", self);

        self.meaningP = Qt.QPushButton("p", self);
        self.sentenceP = Qt.QPushButton("p", self);
        
        
        grid = QtGui.QGridLayout()
        grid.addWidget(self.leftButton, 6,0,1,2)
        
        grid.addWidget(self.wordLabel, 0,3,1,6)
        
        grid.addWidget(self.meaningLabel, 4,3,4,6)
        grid.addWidget(self.meaningP, 5,10)
        grid.addWidget(self.meaningR, 6,10)
        
        grid.addWidget(self.sentenceLabel, 9,3,4,6)
        grid.addWidget(self.sentenceP, 10,10)
        grid.addWidget(self.sentenceR, 11,10)
        
        grid.addWidget(self.rightButton,6,13,1,2)
        
        grid.addWidget(self.statusLabel,14,0)
        
        self.setLayout(grid)

        self.setGeometry(300, 300, 1050, 550)
        self.setWindowTitle('Word Learner')
        
        
        self.meaningLabel.setReadOnly(True)
        self.sentenceLabel.setReadOnly(True)
        #self.wordLabel.setReadOnly(True)
        
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageDown:
            self.previous()
        if event.key() == QtCore.Qt.Key_Enter:
            self.next()


    def record(self, AUDIO_OUTPUT_FILENAME,arg1):
        #arecord -v -f cd -t raw | lame -r -h -V 0 -b 128 -B 224 - output.mp3
        
#         reccmd = ["arecord", "-B", "5000", "-f", "dat"]
#         mp3cmd = ["lame", "-m", "j", "-q", "5", "-V", "2", "-", AUDIO_OUTPUT_FILENAME]
        reccmd = ["arecord","-v","-f","cd","-t","raw"]
        mp3cmd = ["lame","-r","-h","-V","0","-b","128","-B","224","-",AUDIO_OUTPUT_FILENAME]
        p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(mp3cmd, stdin=p.stdout)
        while self.isRecording == True:
            time.sleep(.2)
        p.send_signal(subprocess.signal.SIGTERM)
        self.play(AUDIO_OUTPUT_FILENAME)

    def record_old(self, WAVE_OUTPUT_FILENAME,arg1):
        print WAVE_OUTPUT_FILENAME
        print "record"
        self.isRecording=True
        p = pyaudio.PyAudio()
    
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        while self.isRecording:
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print "record complete"
        
        self.play(WAVE_OUTPUT_FILENAME)
        

    def meaningPressed(self):
        print "meaning pressed"
        self.isRecording = True
        self.t = threading.Thread(target=self.record, args=(self.getCurrentWordPath()+MEANINGFILE,1))     #DONT KNOW WHY IT IS 1
        self.t.daemon = True
        self.t.start()
        
    def meaningReleased(self):
        time.sleep(1);  #need to capture the last 1 sec words
        self.isRecording=False;
        
    def sentencePressed(self):
        print "sentence pressed"
        self.isRecording = True
        self.t = threading.Thread(target=self.record, args=(self.getCurrentWordPath()+SENTENCES,1))
        self.t.daemon = True
        self.t.start()
        
    def sentenceReleased(self):
        time.sleep(1);  #need to capture the last 1 sec words
        self.isRecording=False;

    def meaningPlay(self):
        self.play(self.getCurrentWordPath()+MEANINGFILE)
        
    def sentencesPlay(self):
        self.play(self.getCurrentWordPath()+SENTENCES)
        
    def play(self, fileName):
        playmp3 = ["mpg123", fileName]
        subprocess.Popen(playmp3)

    def play_old(self, fileName):
        if os.path.isfile(fileName):
            wf = wave.open(fileName, 'rb')
            p = pyaudio.PyAudio()
    
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            data = wf.readframes(CHUNK)
            
            while data != '':
                stream.write(data)
                data = wf.readframes(CHUNK)
            
            stream.stop_stream()
            stream.close()
            
            p.terminate()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = WordLearner()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
