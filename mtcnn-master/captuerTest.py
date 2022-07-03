import pyautogui
import pygetwindow as gw
import pywinauto
import time

win = gw.getWindowsWithTitle('Zoom')[0]

win.activate() # 해당 윈도우를 활성화
#print(win.size)
#print(win.left, win.top)
# 만약 에러가 자주 발생하면 아래 코드로 실행한다.
if win.isActive == False:
    pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()

left_top_x = win.topleft[0]
right_bottom_y = win.bottomright[1]

pyautogui.screenshot('test.png', region=(win.left, win.top, win.right, win.bottom))
#pyautogui.doubleClick(win.center) # 해당 윈도우창의 정가운데 더블 클릭

#time.sleep(6)

#pyautogui.screenshot('test.png')