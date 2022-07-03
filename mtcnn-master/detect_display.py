#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2019 Iván de Paz Centeno
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
from mtcnn import MTCNN
from PIL import Image
import pyautogui
import pygetwindow as gw
import pywinauto
import time

detector = MTCNN()
image_name = "./image/screenshot.jpg"
resultImg_name = "./result/screenshot_drawn.jpg"

#win = gw.getWindowsWithTitle('Zoom')[0]
win = gw.getWindowsWithTitle('사진')[0]
win.activate()

if win.isActive == False:
    pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()

#pyautogui.doubleClick(win.center)
#time.sleep(6)
pyautogui.click(win.right, win.bottom)

pyautogui.screenshot(image_name)

image = cv2.cvtColor(cv2.imread(image_name), cv2.COLOR_BGR2RGB)
result = detector.detect_faces(image)

# 모든 얼굴을 탐지하기 위해 for문 사용
for i in range(len(result)):
    bounding_box = result[i]['box']
    keypoints = result[i]['keypoints']
    confidence = result[i]['confidence']

    start_point = (bounding_box[0], bounding_box[1])
    end_point = (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3])

    cv2.rectangle(image, start_point, end_point, (0,155,255), 2)
    cv2.putText(image, f'{confidence}', (bounding_box[0], bounding_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
    
# 랜드마크(눈,코,입) 찍는 코드
    for key in keypoints:
        cv2.circle(image,(keypoints[key]), 2, (0,155,255), 2)

    print(confidence)

cv2.imwrite(resultImg_name, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))


