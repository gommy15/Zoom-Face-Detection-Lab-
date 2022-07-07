from PIL import ImageGrab
from functools import partial
import pyautogui
import pygetwindow as gw
import pywinauto
import time
import ctypes
from screeninfo import get_monitors

win = gw.getWindowsWithTitle('Zoom 회의')[0]
win.activate()
#pyautogui.doubleClick(win.center)

#time.sleep(6)
# bbox=(win.left, win.top, win.right, win.bottom),
ImageGrab.grab = partial(ImageGrab.grab, bbox=(win.left, win.top+80, win.right, win.bottom-80), all_screens=True)
img = ImageGrab.grab()

img.save("image4.png")

'''

for m in get_monitors():
#monitor = get_monitors()
    i = i + 1
    ImageGrab.grab = partial(ImageGrab.grab, bbox=(m.x, m.y, m.x+m.width, m.y+m.height), all_screens=True)
    img = ImageGrab.grab()
    img.save(f"image{i}.png")
    print(str(m))
'''
#img = ImageGrab.grab()

#img.save("image1.png")  # 파일로 저장 image1.png