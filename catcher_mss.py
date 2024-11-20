
import cv2
import numpy as np
import mss # with mss we can recoring near to 20fps
import pygetwindow as gw 
import time

window_name = "chrome"

fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 20.0
record_seconds = 60 * 60

w = gw.getWindowsWithTitle(window_name)[0]
w.activate()

out = cv2.VideoWriter('output.avi', fourcc, fps, tuple(w.size))

appTitle = "BlackSpot"

# set the window title
# cv2.namedWindow(appTitle)

# Создаем экземпляр mss
sct = mss.mss()


# Начало записи
start_time = time.time()

paused = False

for i in range(int(record_seconds * fps)):

    # Определяем область захвата
    monitor = {
        "top": w.top,
        "left": w.left,
        "width": w.width,
        "height": w.height
    }

    if not paused:
        loop_start = time.time()  # Отслеживаем начало цикла

        # Захват кадра через mss
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)

        # Преобразуем цветовую схему
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        out.write(frame)
        cv2.imshow(appTitle, frame)

        # Расчет времени выполнения и корректировка задержки
        elapsed = time.time() - loop_start
        delay = max(1 / fps - elapsed, 0)  # Учитываем прошедшее время
        time.sleep(delay)

    key = cv2.waitKey(1)
    if key == ord("q") or cv2.getWindowProperty(appTitle, cv2.WND_PROP_VISIBLE) < 1 :
        break
    elif key == ord(' '):
        paused = not paused


cv2.destroyAllWindows()
out.release()

