import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
from mtcnn import MTCNN
from PIL import Image
import dlib
import math
import datetime
import pyautogui
import pygetwindow as gw
import pywinauto
import time

print(datetime.datetime.now())
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
detector = MTCNN()
print(datetime.datetime.now())
'''
#저장되어있는 이미지를 사용할 때
image_name = "./image/real_test.png"
resultImg_name = "./result/real_test_drawn.png"
'''

#캡쳐 이미지를 사용할 때
image_name = "./image/screenshot.jpg"
resultImg_name = "./result/screenshot_drawn.jpg"

#win = gw.getWindowsWithTitle('Zoom 회의')
win = gw.getWindowsWithTitle('사진')[0]
win.activate()
win.maximize()

if win.isActive == False:
    pywinauto.application.Application().connect(handle=win._hWnd).top_window().set_focus()
    win.activate()

time.sleep(1)           #maximize 되는 시간 기다리기
pyautogui.screenshot(image_name, region=(win.left, win.top, win.right, win.bottom))


image = cv2.cvtColor(cv2.imread(image_name), cv2.COLOR_BGR2RGB)
result = detector.detect_faces(image)

# 모든 얼굴을 탐지하기 위해 for문 사용
for i in range(len(result)):
    bounding_box = result[i]['box']
    #keypoints = result[i]['keypoints']
    #confidence = result[i]['confidence']

    #좌표값을 dlib 사각형 값으로 변환
    dlib_rect = dlib.rectangle(bounding_box[0], bounding_box[1], bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3])
    shape = predictor(image, dlib_rect)

    #얼굴에 사각형 그리기
    cv2.rectangle(image, (dlib_rect.left(), dlib_rect.top()), (dlib_rect.right(), dlib_rect.bottom()), (0,155,255), 2)

    ## 표시할 선, 도형
    line_width = 3
    circle_r = 3
    ## 글씨
    fontType = cv2.FONT_HERSHEY_SIMPLEX
    fontSize = 0.6
    font_width = 2

    # 이제 랜드마크에 점을 찍어보자.
    num_of_points_out = 4
    num_of_points_in = shape.num_parts - num_of_points_out
    gx_out = 0
    gy_out = 0
    gx_in = 0
    gy_in = 0

    # 점을 찍으려면 필요한 건 좌표!  -> 이는 shape.part(번호) 에 (x,y로) 들어있다.
    # 번호값을 하나씩 바꿔가며 좌표를 찍자.
    for i in range(shape.num_parts):  # 총 5개
        shape_point = shape.part(i)
        #print('얼굴 랜드마크 No.{} 좌표위치: ({}, {})'.format(i, shape_point.x, shape_point.y))

        # 얼굴 랜드마크마다 그리기
        ## i(랜드마크 번호)가 17보다 작으면 out(바깥쪽)을 그린다 - 파란색 점
        if i < num_of_points_out:
            cv2.circle(image, (shape_point.x, shape_point.y), circle_r, (0, 0, 255), line_width)
            gx_out = gx_out + shape_point.x / num_of_points_out
            gy_out = gy_out + shape_point.y / num_of_points_out

        ##반면 i가 17이상이면 in(안쪽)을 그린다 - 초록색 점
        else:
            cv2.circle(image, (shape_point.x, shape_point.y), circle_r, (0, 255, 0), line_width)
            gx_in = gx_in + shape_point.x / num_of_points_in
            gy_in = gy_in + shape_point.y / num_of_points_in

    # 랜드마크에 톡톡톡 찍힌 점들 중에서도, 가장 중심위치를 표시해보자.
    # 먼저 out(바깥쪽)은 빨강색
    cv2.circle(image, (int(gx_out), int(gy_out)), circle_r, (255, 0, 0), line_width)
    # 그리고 in(안쪽)은 검은색
    cv2.circle(image, (int(gx_in), int(gy_in)), circle_r, (0, 0, 0), line_width)

    # 얼굴 방향 표시하기(정면인지? 측면인지? -> 앞서 만든 out, in 좌표로 계산!)
    # math.asin(x) : x의 아크 사인을 라디안 값으로 반환
    theta = math.asin(2 * (gx_in - gx_out) / (dlib_rect.right() - dlib_rect.left()))
    radian = theta * 180 / math.pi
    #print(' ')
    #print('얼굴방향: {0:.3f} (각도: {1:.3f}도)'.format(theta, radian))

    # 이 얼굴방향과 각도를 face('d') 사각형 위에 출력
    if radian < 0:
        textPrefix = 'left'
    else:
        textPrefix = 'right'

    textShow = textPrefix + str(round(abs(radian), 1))
    cv2.putText(image, textShow, (dlib_rect.left(), dlib_rect.top() - 10), fontType, fontSize, (255, 0, 0), font_width, cv2.LINE_AA)
    
#cv2.imshow('img', image)
cv2.imwrite(resultImg_name, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
#cv2.waitKey(0)  # 아무키나 누르면
#cv2.destroyAllWindows() # 모든 창 닫기

print(datetime.datetime.now())
