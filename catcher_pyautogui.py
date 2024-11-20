import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

window_name = "chrome"

fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 10.0
record_seconds = 60 * 30

w = gw.getWindowsWithTitle(window_name)[0]
w.activate()

out = cv2.VideoWriter('output.avi', fourcc, fps, tuple(w.size))

start_time = time.time()

for i in range(int(record_seconds * fps)):
    if cv2.waitKey(1) == ord("q"):
        break
    loop_start = time.time()  # Отслеживаем начало цикла

    # Захват кадра
    img = pyautogui.screenshot(region=(w.left, w.top, w.width, w.height))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)
    cv2.imshow('screenshot', frame)

    # Расчет времени выполнения и корректировка задержки
    elapsed = time.time() - loop_start
    delay = max(1 / fps - elapsed, 0)  # Учитываем прошедшее время

    time.sleep(delay)


cv2.destroyAllWindows()
out.release()

