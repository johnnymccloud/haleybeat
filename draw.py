# importing cv2 
import cv2 
import time   
import sys
from aubio import tempo, source
from playsound import playsound
from threading import Thread

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []
timestamps = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        timestamps.append(this_beat / float(samplerate))
        # print("%f" % (timepstamp))
        beats.append(this_beat)
    total_frames += read
    if read < hop_s: break
#print len(beats)






# path 
path = r'car.jpg'
   
# Reading an image in default mode
image = cv2.imread(path)
   
# Window name in which image is displayed
window_name = 'HaleyBeat'
cv2.imshow(window_name, image) 
cv2.waitKey(1000)

windshield = {"up" : ((100, 100), (300, 300)),
            "down" : ((580, 300), (300, 300))}

# Blue color in BGR
color = (0, 0, 255)
  
# Line thickness of 2 px
thickness = 10

def play_music(filename):
    playsound(filename)


start_time = time.time()

thread = Thread(target = play_music, args = [filename])
thread.start()


positions = ["up", "down"]
divider = 4
for i in range(len(timestamps)):
    if i % divider == 0:
        while time.time() < start_time + timestamps[i]:
            time.sleep(0.01)
        print("%f" % (timestamps[i]))
        pos = positions[(i % (divider * 2)) // divider] # 0 or 1
        start_point, end_point = windshield[pos]
        image = cv2.imread(path)
        image = cv2.line(image, start_point, end_point, color, thickness)
        cv2.imshow(window_name, image)
        k = cv2.waitKey(1)
        if k == 27:    # Esc key to stop
            break

thread.join()
