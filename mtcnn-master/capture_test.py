from PIL import ImageGrab
from functools import partial
import pyautogui
import pygetwindow as gw
import pywinauto
import time

win = gw.getWindowsWithTitle('real_test')[0]
win.activate()
win.maximize()

ImageGrab.grab = partial(ImageGrab.grab, bbox=(win.left, win.top, win.right, win.bottom), all_screens=True)


img = ImageGrab.grab()

img.save("image1.png")  # 파일로 저장 image1.png