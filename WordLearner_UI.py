#!/usr/bin/python
import sys
from PyQt4 import Qt, QtGui, QtCore, uic
import pyaudio
import wave
import threading
import os
import time
import subprocess
from random import shuffle


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
        
        self.pronounce.clicked.connect(self.doPronounce)
        self.meaningP.clicked.connect(self.meaningPlay)
        
        self.dirList = filter(self.isDir, os.listdir(self.rootDir))
        self.dirList = sorted(self.dirList, key=lambda s: s.lower())
        self.dirList = self.dirList[0:700]
        self.dirList = ["abase","abash","abate","abbreviate","abdicate","aberrant","aberration","abet","abeyance","abhor","abject","abjure","ablution","abnegation","abolish","abominate","abominable","aboriginal","abortive","abrasive","abridge","abrogate","abscission","abscond","absolute","absolve","abstain","abstemious","abstinence","abstract","representational","abstruse","abusive","abut","abysmal","abyss","academic","accede","accelerate","accessible","accessory","acclaim","acclimate","acclivity","accolade","merit","demerit","earn","accommodate","accomplice","accord","accost","accoutre","accretion","accrue","acerbity","bitter","biting","acetic","acidulous","acknowledge","acme","acoustics","acquiesce","acquittal","acrid","acrimonious","acrophobia","actuarial","actuary","actuate","acuity","acumen","acute","adage","proverb","adamant","adapt","addendum","addiction","addle","address","adept","adhere","adherent","adjacent","adjoin","adjourn","adjunct","adjuration","adjutant","admonish","adore","adorn","adroit","adulation","adulterate","advent","adventitious","adversary","adverse","adversity","advert","advocacy","advocate","aegis","aeriea","aesthetic","affable","affected","affidavit","affiliation","affinity","affirmation","affliction","affluence","affront","agape","agenda","agglomeration","aggrandize","aggregate","aghast","agility","agitate","agnostic","agog","agrarian","alacrity","alchemy","alcove","alias","alienate","alimentary","alimony","allay","allege","allegiance","allegory","alleviate","alliteration","allocate","earmark","alloy","allude","allure","siren","alluvial","aloof","aloft","altercation","altruistic","amalgamate","amalgam","amass","amazon","ambidextrous","ambience","ambiguous","ambivalence","amble","ambrosia","nectar","ambulatory","ameliorate","amenable","amend","amenities","amiable","amicable","amiss","amity","amnesia","amnesty","amoral","amorous","amorphous","amphibian","amphitheater","ample","amplify","amputate","amoka","amulet","anachronism","analgesic","analgesia","analogous","analogy","anarchist","anarchy","anathema","ancestry","anchor","ancillary","anecdote","anemia","anesthetic","anguish","angular","animadversion","animated","animosity","animus","annals","anneal","annex","annihilate","annotate","annuity","annul","elope","anodyne","anoint","anomalous","anomaly","anonymity","antagonism","protagonist","antecede","antecedents","antediluvian","anthem","anthology","anthropoid","anthropologist","anthropomorphic","anticlimax","antidote","antipathy","antiquated","antique","antiquity","antiseptic","antithesis","antler","anvil","apathy","ape","aperture","apex","aphasia","aphorism","apiary","hive","apiculture","apiarist","aplomb","poise","apocalyptic","apocryphal","apogee","apolitical","apologist","apoplexy","apostate","apothecary","apothegma","apotheosis","appall","apparition","appease","appellation","append","application","apposite","appraise","appreciate","apprehend","apprehensive","apprise","approbation","appropriate","appurtenances","apropos","aptitude","aquiline","arable","arbiter","arbitrary","arbitrate","arboretum","arboreal","arcade","arcane","archaeology","archaic","archetype","arch-","archipelago","archives","ardor","arduous","argot","aria","arid","aristocracy","armada","aromatic","arraign","array","arrears","arrhythmic","arrogance","arroyo","artery","articulate","arsenal","artifacts","artifice","artisan","artless","ascendancy","ascertain","ascetic","ascribe","aseptic","ashen","asinine","askance","askew","asperity","aspersion","aspirant","aspire","assail","assay","assent","assert","assiduous","assimilate","assuage","assumption","regent","assurance","asteroid","astigmatism","astral","astringent","astronomical","astute","asunder","asylum","asymmetric","atavism","atheistic","atone","atrocity","atrophy","attentive","attenuate","attest","attribute","attrition","atypical","audacious","audit","augment","augury","august","aureole","auroral","auspicious","austere","authenticate","authoritarian","authoritative","autocratic","automaton","autonomous","autopsy","auxiliary","avalanche","avarice","avenge","aver","averse","aversion","avert","aviary","avid","avocation","avow","avuncular","awe","awful","awl","awry","axiom","azure","babble","bacchanalian","bacchanal","Bacchanalia","badger","badinage","baffle","bait","baleful","balk","ballast","balm","pang","balmy","banal","bandy","bane","bantering","barb","bard","barefaced","unregenerate","baroque","barrage","barrister","solicitor","barterer","bask","luxuriate","bastion","bate","bauble","bawdy","beatific","bliss","beatitude","mystic","bedizen","finery","bedraggle","beeline","befuddle","fuddle","beget","begrudge","grudge","beguile","behemoth","beholden","behoovea","belabor","belated","beleaguer","belie","belittle","bellicose","belligerent","bemoan","bemused","benediction","benefactor","beneficent","beneficial","beneficiary","benefit","benevolent","benign","benison","bent","bequeath","berate","bereavement","bereaved","bereft","berserk","beseech","beset","hem","besiege","besmirch","bestial","bestow","betoken","token","betray","betroth","bevy","bicameral","bicker","biennial","bifurcated","bigotry","bigot","intolerant","bilious","bilk","billowing","billow","swell","surge","bivouac","bizarre","blanch","bland","blandishment","blare","screech","dazzle","blas\'e","blasphemy","blatant","bleak","blighted","blight","blithea","bloated","blowhard","bludgeon","bluff","blunder","blurt","bluster","bully","bode","bogus","bohemian","boisterous","bolster","bolt","dart","gobble","bombardment","bombastic","bombast","boon","boorish","boor","bouillon","bountiful","gracious","bourgeois","bovine","bowdlerize","brackish","braggadocio","brag","braggart","brandish","bravado","swagger","brawn","brawny","sturdy","brazen","brawl","breach","breadth","brevity","brindled","tawny","bristling","bristle","brittle","broach","brocade","brochure","brooch","clasp","brook","browbeat","browse","graze","skim","brunt","brusque","buccaneer","bucolic","buffet","slap","buffoonery","buffoon","clown","bugaboo","bullion","bulwark","bungle","botch","buoyant","bureaucracy","burgeon","burlesque","burnish","buttress","prop","buxom","plump","cabal","cache","cacophonous","cadaver","cadaverous","cadence","cajole","coax","calamity","calculated","caldrona","caliber","calligraphy","callous","callus","callow","calorific","calumny","camaraderie","cameo","canard","candor","canine","canker","ulcer","canny","cant","cantankerous","cantata","canter","canto","canvass","capacious","capacity","capillary","capitulate","caprice","capricious","caption","captious","carafe","carapace","carata","carcinogenic","cardinal","cardiologist","careen","career","sway","caricature","carillon","carnage","carnal","carnivorous","carousal","carping","carrion","cartographer","cascade","caste","castigation","casualty","casual","cataclysm","catalyst","catapult","hurl","cataract","catastrophe","catcall","catechism","categorical","qualify","catharsis","cathartic","catholic","caucus","caulka","causal","caustic","cauterize","cavalcade","cavalier","cavil","cede","celerity","celestial","hereafter","afterlife","celibate","censor","censorious","censure","centaur","centigrade","centrifugal","centrifuge","centripetal","centurion","cerebral","cerebration","ceremonious","unceremonious","certitude","cessation","cession","chafe","chaff","chaffing","chagrin","chalice","chameleon","champion","championship","chaotic","charisma","charlatan","chary","chase","chasm","chassis","chaste","chasten","chastise","chauvinist","check","checkereda","cherubic","chicanery","chide","chimerical","chisel","chip","chivalrous","choleric","choreography","chore","chortle","chuckle","chronic","chronicle","churlish","ciliated","cipher","circlet","circuitous","circuit","circumlocution","circumscribe","circumspect","circumvent","cistern","citadel","cite","civil","clairvoyant","hindsight","clamber","clamor","clandestine","chaperon","clangor","clapper","clap","clarion","claustrophobia","clavicle","scrimmage","cleave","cleft","clemency","clich\'e","bromide","clientele","climactic","clime","clique","cloister","clout","cloying","coagulate","clot","pudding","coalesce","coalition","coda","coddle","codicil","codify","coercion","coeval","cog","cogent","cogitate","cognate","cognitive","cognizance","cohabit","cohere","cohesion","cohorts","coiffure","coin","coincidence","colander","collaborate","collage","scrap","scraps","scrappy","collate","collateral","collation","colloquial","colloquy","collusion","colossal","colossus","comatose","coma","combustible","comely","homely","comestible","comeuppance","deserts","comity","commandeer","draft","draught","commemorative","commemorate","commensurate","commiserate","commodious","communal","commune","compact","compatible","compelling","compulsion","compulsory","compulsive","compendium","compensatory","compilation","compile","complacency","smug","complaisant","complement","complementary","compliance","compliant","complicity","component","comport","deport","bearing","composure","compound","comprehensive","comprehend","compress","comprise","compromise","compunction","compute","reckon","concatenate","concave","concede","conceit","vain","concentric","conception","concerted","concession","conciliatory","concise","conclave","conclusive","concoct","concomitant","concord","concordat","concur","concurrent","condescend","condign","condiments","condole","condone","conducive","conduit","confidanta","confide","confidence","confidential","confine","confiscate","conflagration","confluence","conformity","conformist","confound","congeal","congenial","congenital","conglomeration","conglomerate","congruence","congruent","conifer","conjecture","conjugal","conjure","connivance","connoisseur","connotation","connubial","matrimony","patrimony","consanguinity","consanguineousa","conscientious","conscript","consecrate","consensus","consequential","conservatorya","consign","consistency","console","consolidation","consonance","consonant","consort","conspiracy","conspire","consternation","constituent","constituency","constitution","constraint","construe","consummate","contagion","drastic","contaminate","contempt","contend","contention","thesis","boost","contentious","contest","context","contiguous","continence","contingent","contortions","contraband","contravene","contrite","contrived","contrive","contrivance","controvert","contumacious","contusion","bruise","conundrum","convene","convention","conventional","converge","conversant","converse","convert","convex","conveyance","conviction","convivial","convoke","convoluted","convulsion","copious","coquette","flirt","cordial","cordon","cornice","cornucopia","corollary","corporeal","corpulent","corpus","corpuscle","correlation","correlate","corroborate","corrode","corrosive","corrugated","wrinkle","crinkle","cosmic","coterie","countenance","countermand","counterpart","coup","couple","courier","covenant","bargain","covert","covetous","cow","cower","coy","cozen","crabbed","peevish","crass","craven","credence","credo","credulity","creed","crescendo","far-fetched","overture","crestfallen","crest","crevice","cringe","criteria","crone","crotchety","crux","crypt","cryptic","cubicle","compartment","cuisine","culinary","cull","culmination","culpable","culprit","culvert","cumbersome","cumulative","cupidity","curator","curmudgeon","cursive","cursory","curtail","cynical","cynosure","dabble","dais","dally","dank","dapper","dappled","daub","smear","smudge","daunt","dauntless","dawdle","deadlock","standstill","deadpan","dearth","d\'eb\^acle","debase","kneel","debauch","seduce","debilitate","bout","debonair","d\'ebris","debunk","debutante","debut","decadence","decant","decapitate","decelerate","deciduous","decimate","decipher","declivity","d\'ecollet\'e","decree","decomposition","decorum","decorous","decoy","decrepitude","decrepit","decry","deducible","deface","mar","defame","default","defeatist","defection","defect","defer","deference","defiance","defile","definitive","deflect","defoliate","defray","defrock","frock","deft","defunct","degenerate","degradation","dishonor","dehydrate","deify","deign","stoop","delete","deleterious","deliberate","delineate","delirium","delta","delude","deluge","delusion","delusive","delve","demagogue","demean","demeanor","demented","demise","demographic","demolition","demoniaca","fiend","demotic","demur","demure","denigrate","denizen","denotation","d\'enouement","denounce","depict","expos\'e","deplete","deplore","deploy","battalion","depose","deposition","depravity","deprecate","depreciate","depredation","deranged","institute","institution","institutionalize","derelict","dereliction","deride","derision","derivative","derivation","dermatologist","acne","derogatory","descry","desecrate","violate","desiccate","desolate","desperado","desperate","despise","despoil","despondent","despot","destitute","impoverish","desultory","detached","detain","determinate","determination","deterrent","detonation","detraction","detrimental","deviate","devious","devise","devoid","devolve","deputize","devotee","devout","religious","dexterous","diabolical","diadem","dialectical","diaphanous","diatribe","dichotomy","dictum","didactic","die","diffidence","diffuse","digression","dilapidated","dilate","dilatory","dilemma","dilettante","diligence","dilute","diminution","din","weary","dinghy","maroon","dingy","dull","dint","diorama","dire","dirge","disabuse","disaffected","disapprobation","disarray","disavowal","disband","disburse","discernible","discerning","disclaim","disclose","discombobulated","discompose","discomfit","disconcert","disconsolate","discord","discordant","discount","discourse","discredit","discrepancy","discrete","discretion","discriminating","discriminate","brisk","discursive","disdain","disembark","disenfranchise","disengage","disfigure","disgorge","disgruntle","dishearten","disheveled","disinclination","disingenuous","disinter","disinterested","disjointed","disjunction","dislodge","dismantle","mantle","crust","dismember","dismiss","disparage","maneuvera","disparate","disparity","dispassionate","dispatch","dispel","dispense","disperse","dispirited","disport","disputatious","disquietude","disquisition","dissection","dissemble","disseminate","dissent","dissertation","dissident","dissimulate","dissipate","dissolution","reduce","dissuade","dissonance","distant","distend","distill","distinction","distinct","distinctive","distort","distrait","distraught","distract","diurnal","diva","diverge","diverse","diversion","divest","divine","dowse","divulge","docile","ferocious","docket","doctrinaire","doctrine","indoctrinate","document","doddering","merit","doff","dogged","persevere","doggerel","dogmatic","doldrums","blues","dolorous","dolt","domicile","domineer","dominate","dominant","don","outfit","dormant","dormer","dorsal","dossier","dotage","dote","dour","sullen","brood","douse","dowdy","downcast","drab","draconian","dregs","drivel","nonsense","dribble","drip","trickle","droll","queer","drone","murmur","dross","drudgery","drudge","dubious","ductile","dulcet","dumbfounda","dupe","duplicity","duration","duress","dutifula","dwindle","dynamic","dynamo","dyspeptic","dys","dyslexia","dysentery"]
#         shuffle(self.dirList)
        
        i=1
        for text in self.dirList:
            item = QtGui.QListWidgetItem()
            item.setText(text+"  "+str(i))
            i=i+1
#             item.setBackground(QtGui.QColor('red'))
            self.wordList.addItem(item)
        
        self.wordList.currentItemChanged.connect(self.wordClicked)
            
        self.wordIndex = 0
        self.showWord()
    
    def doPronounce(self):
        self.play(self.getCurrentWordPath() + "/"+ self.getCurrentWord() + ".mp3")
        
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
        return str(self.rootDir + self.getCurrentWord() + "/")
        
    def getCurrentWord(self):
        return self.dirList[self.wordIndex]
        
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
            time.sleep(.1)
        p2.send_signal(subprocess.signal.SIGTERM)
        p.send_signal(subprocess.signal.SIGTERM)
#         self.play(AUDIO_OUTPUT_FILENAME)

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
    
