#!/usr/bin/python
import sys
from PyQt4 import Qt, QtGui, QtCore, uic
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
MEANINGFILE = "meaning.mp3"
SENTENCES = "sentences.mp3"

class WordLearnerUI(QtGui.QMainWindow):

    def __init__(self):
        super(WordLearnerUI, self).__init__()
        self.addWidgets()

        self.rootDir = "./oxford-dict/"
        self.meaningR.pressed.connect(self.meaningPressed)
        self.meaningR.released.connect(self.meaningReleased)

        self.leftButton.clicked.connect(self.previous)
        self.rightButton.clicked.connect(self.next)
        self.assesment.valueChanged.connect(self.updateAssesment)
        
        self.meaningP.clicked.connect(self.meaningPlay)
        
        self.dirList = filter(self.isDir, os.listdir(self.rootDir))
        self.dirList = sorted(self.dirList, key=lambda s: s.lower())
        
        for text in self.dirList:
            item = QtGui.QListWidgetItem()
            item.setText(text)
#             item.setBackground(QtGui.QColor('red'))
            self.wordList.addItem(item)
        
        self.wordList.currentItemChanged.connect(self.wordClicked)
            
        self.wordIndex = 0
        self.showWord()
    
    def wordClicked(self):
        if self.wordIndex != self.wordList.currentRow():
            self.wordIndex = self.wordList.currentRow()
            self.showWord()

    def isDir(self, s):
        return os.path.isdir(self.rootDir + s)

    def updateAssesment(self):
        open(self.getCurrentWordPath() + "assesment", "w+").write(str(self.assesment.value()))
        
    def previous(self):
#         self.wordIndex = (self.wordIndex - 1 + len(self.dirList)) % len(self.dirList);
        if self.wordIndex != 0:
            self.wordIndex = self.wordIndex - 1
        self.showWord()
        
    def next(self):
#        self.wordIndex=(self.wordIndex + 1) % len(self.dirList);
         if self.wordIndex != len(self.dirList):
            self.wordIndex = self.wordIndex + 1
         self.showWord()
        
    def getCurrentWordPath(self):
        return str(self.rootDir + self.dirList[self.wordIndex] + "/")
        
    def showWord(self):
        try:
            self.assesment.setValue(int(open(self.getCurrentWordPath() + "assesment").read()))
        except:
            self.assesment.setValue(0)
        
        self.wordLabel.setText("<b>" + self.dirList[self.wordIndex] + "</b>")
        self.meaningTextEdit.setText(open(self.getCurrentWordPath() + "meaning").read())
#         self.sentenceTextEdit.setText(open(self.getCurrentWordPath()+"sentences").read())
        self.wordList.setCurrentRow(self.wordIndex)
#         self.statusLabel.setText(str(self.wordIndex+1) + '/' + str(len(self.dirList)))
 
    def addWidgets(self):
#         self.ui = uic.loadUi('WordLearner.ui', self)
        self.ui = uic.loadUi('mainwindow.ui', self)
        self.show()

    def record(self, AUDIO_OUTPUT_FILENAME, arg1):
        # arecord -v -f cd -t raw | lame -r -h -V 0 -b 128 -B 224 - output.mp3
        
#         reccmd = ["arecord", "-B", "5000", "-f", "dat"]
#         mp3cmd = ["lame", "-m", "j", "-q", "5", "-V", "2", "-", AUDIO_OUTPUT_FILENAME]
        reccmd = ["arecord", "-v", "-f", "cd", "-t", "raw"]
        mp3cmd = ["lame", "-r", "-h", "-V", "0", "-b", "128", "-B", "224", "-", AUDIO_OUTPUT_FILENAME]
        p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(mp3cmd, stdin=p.stdout)
        while self.isRecording == True:
            time.sleep(.2)
        p.send_signal(subprocess.signal.SIGTERM)
        self.play(AUDIO_OUTPUT_FILENAME)

    def record_old(self, WAVE_OUTPUT_FILENAME, arg1):
        print WAVE_OUTPUT_FILENAME
        print "record"
        self.isRecording = True
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
        self.t = threading.Thread(target=self.record, args=(self.getCurrentWordPath() + MEANINGFILE, 1))  # DONT KNOW WHY IT IS 1
        self.t.daemon = True
        self.t.start()
        
    def meaningReleased(self):
        time.sleep(1);  # need to capture the last 1 sec words
        self.isRecording = False;
        
    def sentencePressed(self):
        print "sentence pressed"
        self.isRecording = True
        self.t = threading.Thread(target=self.record, args=(self.getCurrentWordPath() + SENTENCES, 1))
        self.t.daemon = True
        self.t.start()
        
    def sentenceReleased(self):
        time.sleep(1);  # need to capture the last 1 sec words
        self.isRecording = False;

    def meaningPlay(self):
        self.play(self.getCurrentWordPath() + MEANINGFILE)
        
    def sentencesPlay(self):
        self.play(self.getCurrentWordPath() + SENTENCES)
        
    def play(self, fileName):
        playmp3 = ["mpg123", fileName]
        subprocess.Popen(playmp3)
        print "another"

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
    ex = WordLearnerUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
