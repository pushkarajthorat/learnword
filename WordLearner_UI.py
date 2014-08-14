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
MEANINGFILE="meaning.mp3"
SENTENCES="sentences.mp3"

#   python /home/pushkaraj.thorat_fedora/workspace/python/GREPrep/another2.py amazon
# python /home/pushkaraj.thorat_fedora/workspace/python/GREPrep/another2.py $folder/$folder | html2text -width 1000 | grep -Ev "Get_more_examples|View_synonyms|More example sentences" > $folder/meaning
# grep "    * " $folder/meaning > $folder/sentences

#version 3
# python /home/pushkaraj.thorat_fedora/workspace/python/GREPrep/another3.py amazon | tr '\n' ' ' | sed -e 's/<header class/\n<header class/g' -e 's/<\/header>/<\/header>\n/g' -e 's/<\/h2>/<\/h2>\n/g' -e 's/<h2/\n<h2/g'  | grep -v '</div>/</div></header>$' | grep -v '^<header class="entryHeader">' | tr '\n' ' ' | sed -e 's/<h2> Definition of <strong>/\n<h2> Definition of <strong>/g' -e 's/<\/ul>/<\/ul>\n/g'  | grep -v "^<h2> Definition of <strong>"

class WordLearnerUI(QtGui.QMainWindow):

    def __init__(self):
        super(WordLearnerUI, self).__init__()
        self.addWidgets()

#         self.rootDir="/home/pushkaraj.thorat_fedora/Desktop/gre/downloads/"
        self.rootDir="/home/pushkaraj.thorat_fedora/Desktop/gre/oxford-dict/"
        self.meaningR.pressed.connect(self.meaningPressed)
        self.meaningR.released.connect(self.meaningReleased)

        self.sentenceR.pressed.connect(self.sentencePressed)
        self.sentenceR.released.connect(self.sentenceReleased)
        self.leftButton.clicked.connect(self.previous)
        self.rightButton.clicked.connect(self.next)
        self.assesment.valueChanged.connect(self.updateAssesment)
        
        self.meaningP.clicked.connect(self.meaningPlay)
        self.sentenceP.clicked.connect(self.sentencesPlay)
        
        motherList = os.listdir(self.rootDir)
        
#         interestedList = [line.strip() for line in open('/home/pushkaraj.thorat_fedora/Desktop/gre/first500/1.txt')]
        interestedList = [line.strip() for line in open('/home/pushkaraj.thorat_fedora/Desktop/gre/frequent500words.txt')]
        
        interestedList = motherList
        
        missing = [item for item in interestedList if item not in motherList]
        difference = [item for item in interestedList if item not in missing]
        self.dirList=filter(self.isDir, difference)
        self.dirList=sorted(self.dirList,key=lambda s: s.lower())
        
        for text in self.dirList:
            item = QtGui.QListWidgetItem()
            item.setText(text)
#             item.setBackground(QtGui.QColor('red'))
            self.wordList.addItem(item)
        
        self.wordList.currentItemChanged.connect(self.wordClicked)
            
        self.wordIndex=0
        self.showWord()
    
    def wordClicked(self):
        if self.wordIndex != self.wordList.currentRow():
            self.wordIndex=self.wordList.currentRow()
            self.showWord()

    def isDir(self,s):
        return os.path.isdir(self.rootDir+s)

    def updateAssesment(self):
        open(self.getCurrentWordPath()+"assesment","w+").write(str(self.assesment.value()))
        
    def previous(self):
#         self.wordIndex = (self.wordIndex - 1 + len(self.dirList)) % len(self.dirList);
        if self.wordIndex!=0:
            self.wordIndex=self.wordIndex-1
        self.showWord()
        
    def next(self):
#        self.wordIndex=(self.wordIndex + 1) % len(self.dirList);
         if self.wordIndex!=len(self.dirList):
            self.wordIndex=self.wordIndex+1
         self.showWord()
        
    def getCurrentWordPath(self):
        return str(self.rootDir + self.dirList[self.wordIndex] + "/")
        
    def showWord(self):
        try:
            self.assesment.setValue(int(open(self.getCurrentWordPath()+"assesment").read()))
        except:
            self.assesment.setValue(0)
        
        self.wordLabel.setText("<b>"+self.dirList[self.wordIndex]+"</b>")
        self.meaningTextEdit.setText(open(self.getCurrentWordPath()+"meaning").read())
        self.sentenceTextEdit.setText(open(self.getCurrentWordPath()+"sentences").read())
        self.wordList.setCurrentRow(self.wordIndex)
#         self.statusLabel.setText(str(self.wordIndex+1) + '/' + str(len(self.dirList)))
 
    def addWidgets(self):
        self.ui = uic.loadUi('/home/pushkaraj.thorat_fedora/workspace/python/GREPrep/WordLearner.ui', self)
        self.show()

#     def keyPressEvent(self, event):
#         if event.key() == QtCore.Qt.Key_PageUp:
#             self.previous()
#         if event.key() == QtCore.Qt.Key_PageDown:
#             self.next()
#         if event.key() == QtCore.Qt.Key_Home:
#             self.wordIndex=0
#             self.showWord()
#         if event.key() == QtCore.Qt.Key_End:
#             self.wordIndex=len(self.dirList)-1
#             self.showWord()

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
    
