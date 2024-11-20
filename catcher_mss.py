
#  Before running this script, you have to install all included libraries using "pip3 install <lib-name>".
import cv2
import numpy as np
import mss # with mss we can recoring near to 20fps
import pygetwindow as gw 
import time

window_name = "chrome"

fourcc = cv2.VideoWriter_fourcc(*"XVID")
# init fps
fps =20.0

w = gw.getWindowsWithTitle(window_name)[0]
w.activate()
    # define recording area size and position
monitor = {
    "top": w.top,
    "left": w.left,
    "width": w.width,
    "height": w.height
}

out = cv2.VideoWriter('output.avi', fourcc, fps, tuple(w.size))

# init app title
appTitle = "BlackSpot" 

sct = mss.mss()

# init start time
startTime = time.time()
paused = False
#init max recording time
maxRecordTime = 60 * 60
counter = 0
maxIteration = maxRecordTime * fps

while counter < maxIteration :


    if not paused:
        counter += 1
        loop_start = time.time()

        # made screen with mss
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)

        # mutate the color scema 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        out.write(frame)
        cv2.imshow(appTitle, frame)

        # time correction
        elapsed = time.time() - loop_start
        delay = max(1 / fps - elapsed, 0) 
        time.sleep(delay)

    # define control settings
    key = cv2.waitKey(1)
    if key == ord("q") or cv2.getWindowProperty(appTitle, cv2.WND_PROP_VISIBLE) < 1 :
        break
    elif key == ord(' '):
        paused = not paused


cv2.destroyAllWindows()
out.release()

