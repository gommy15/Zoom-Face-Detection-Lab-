import cv2
import datetime
import time
import pandas as pd
from plus_dlib import find_face
from calc_coordinate import calc_user

d = datetime.datetime.now()
#user_box = [{'description': '20178888', 'coordinate': (63, 289, 96, 298), 'box_coordinate': (63, 121, 345, 289)}, {'description': '20200756', 'coordinate': (63, 457, 96, 465), 'box_coordinate': (63, 289, 345, 457)}, {'description': '20200998', 'coordinate': (51, 623, 85, 632), 'box_coordinate': (51, 455, 333, 623)}, {'description': '20181112', 'coordinate': (345, 290, 380, 298), 'box_coordinate': (345, 122, 627, 290)}, {'description': '20200759', 'coordinate': (357, 455, 391, 466), 'box_coordinate': (357, 287, 639, 455)}, {'description': '20210101', 'coordinate': (346, 623, 378, 634), 'box_coordinate': (346, 455, 628, 623)}, {'description': '20190201', 'coordinate': (651, 289, 684, 299), 'box_coordinate': (651, 121, 933, 289)}, {'description': '20200992', 'coordinate': (639, 457, 673, 465), 'box_coordinate': (639, 289, 921, 457)}, {'description': '20213523', 'coordinate': (639, 624, 672, 633), 'box_coordinate': (639, 456, 921, 624)}, {'description': '20190777', 'coordinate': (945, 289, 978, 298), 'box_coordinate': (945, 121, 1227, 289)}, {'description': '20200996', 'coordinate': (933, 457, 967, 465), 'box_coordinate': (933, 289, 1215, 457)}, {'description': '20200745', 'coordinate': (932, 622, 965, 632), 'box_coordinate': (932, 454, 1214, 622)}]
user_total_check = []
face_coordinate = []
check_total_radian = []
number = 1

while(1):
    box_result, image, radianText_list, radianValue_list = find_face()
    user_box = calc_user()

    for i in range(len(box_result)):
        center_x = box_result[i][0] + (box_result[i][2] / 2)
        center_y = box_result[i][1] + (box_result[i][3] / 2)

        face_coordinate.append((int(center_x), int(center_y)))

        # 얼굴에 사각형 그리기
        cv2.rectangle(image, (box_result[i][0], box_result[i][1]), (box_result[i][0]+box_result[i][2], box_result[i][1] + box_result[i][3]), (0, 155, 255), 2)
        cv2.putText(image, radianText_list[i], (box_result[i][0], box_result[i][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)


    for i in range(len(user_box)):
        user_check = {'user' : i, "stay" : False, 'sNum' : user_box[i]['description']}
        check_radian = {'sNum' : user_box[i]['description']}
        for j in range(len(radianValue_list)):
            if (user_box[i]['box_coordinate'][0] <= face_coordinate[j][0] & face_coordinate[j][0] <= user_box[i]['box_coordinate'][2]) \
                & (user_box[i]['box_coordinate'][1] <= face_coordinate[j][1] & face_coordinate[j][1]<= user_box[i]['box_coordinate'][3]):
                user_check = {'user' : i, "stay" : True, 'sNum' : user_box[i]['description'], 'radian' : radianText_list[j]}
                if len(check_total_radian) < i+1:
                    check_radian = {'sNum': user_box[i]['description'], 'radian' : [radianValue_list[j]]}
                    #print(check_radian)
                else :
                    for z in range(len(check_total_radian)):
                        if check_total_radian[z]['sNum'] == user_box[i]['description']:
                            try:
                                check_total_radian[z]['radian'].append(radianValue_list[j])
                                #print(check_total_radian[z])
                            except:
                                check_total_radian[z]['radian'] = [radianValue_list[j]]

                break

        user_total_check.append(user_check)
        if len(check_total_radian) < i+1:
            check_total_radian.append(check_radian)

    print()
    print('========================================')
    print(f'{number}:', check_total_radian)
    print(len(check_total_radian))
    print('========================================')
    cv2.imwrite(f'./result{number}.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    number = number+1

    time.sleep(30)
    if len(check_total_radian[0]['sNum']) == 3:
        break



#cv2.imwrite('./result.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
print(datetime.datetime.now())
#print(user_total_check)
#print(check_total_radian)
#print(len(check_total_radian), len(user_total_check))

