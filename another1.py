# import subprocess
# import time
# 
# reccmd = ["arecord", "-B", "5000", "-f", "dat"]
# mp3cmd = ["lame", "-m", "j", "-q", "5", "-V", "2", "-", "test.mp3"]
# p = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
# p2 = subprocess.Popen(mp3cmd, stdin=p.stdout)
# print "started"
# time.sleep(5)
# print "stopped"
# p.send_signal(subprocess.signal.SIGTERM)



from pygame import mixer # Load the required library

mixer.init()
mixer.music.load('/home/pushkaraj.thorat_fedora/workspace/python/GREPrep/test.mp3')
mixer.music.play()


