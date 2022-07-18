import cv2
import datetime
import time
import numpy as np
import pandas as pd
from plus_dlib import find_face
from calc_coordinate import calc_user

d = datetime.datetime.now()
#user_box = [{'description': '20178888', 'coordinate': (63, 289, 96, 298), 'box_coordinate': (63, 121, 345, 289)}, {'description': '20200756', 'coordinate': (63, 457, 96, 465), 'box_coordinate': (63, 289, 345, 457)}, {'description': '20200998', 'coordinate': (51, 623, 85, 632), 'box_coordinate': (51, 455, 333, 623)}, {'description': '20181112', 'coordinate': (345, 290, 380, 298), 'box_coordinate': (345, 122, 627, 290)}, {'description': '20200759', 'coordinate': (357, 455, 391, 466), 'box_coordinate': (357, 287, 639, 455)}, {'description': '20210101', 'coordinate': (346, 623, 378, 634), 'box_coordinate': (346, 455, 628, 623)}, {'description': '20190201', 'coordinate': (651, 289, 684, 299), 'box_coordinate': (651, 121, 933, 289)}, {'description': '20200992', 'coordinate': (639, 457, 673, 465), 'box_coordinate': (639, 289, 921, 457)}, {'description': '20213523', 'coordinate': (639, 624, 672, 633), 'box_coordinate': (639, 456, 921, 624)}, {'description': '20190777', 'coordinate': (945, 289, 978, 298), 'box_coordinate': (945, 121, 1227, 289)}, {'description': '20200996', 'coordinate': (933, 457, 967, 465), 'box_coordinate': (933, 289, 1215, 457)}, {'description': '20200745', 'coordinate': (932, 622, 965, 632), 'box_coordinate': (932, 454, 1214, 622)}]
#user_total_check = []
#face_coordinate = []
check_total_radian = []
user_list = []
number = 1

def notice_user_check():
    user_image = np.full((550, 300*(len(user_total_check)//10 + 1), 3), (255,255,255), np.uint8)

    for i in range(len(user_total_check)):
        if user_total_check[i]['stay'] == True:
            cv2.putText(user_image, user_total_check[i]['sNum']+" concentrate", (10+(i//10)*300, ((i%10)+1)*50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        else :
            cv2.putText(user_image, user_total_check[i]['sNum'] + " no concentrate", (10+(i//10)*300, ((i%10)+1)* 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imwrite(f'./user_check{number}.png', cv2.cvtColor(user_image, cv2.COLOR_RGB2BGR))
    user_img_check = cv2.imread(f'./user_check{number}.png')
    #image = cv2.cvtColor(cv2.imread(image_name), cv2.COLOR_BGR2RGB)
    cv2.imshow('user check', user_img_check)
    time.sleep(5)
    cv2.destroyAllWindows()

def find_key(dict, val):
    for i in range(len(dict)):
        print("dict[i][description] : ", dict[i]['description'], "val", val)
        if dict[i]['description'] == val:
            return i

while(1):
    user_total_check = []
    try:
        detect_result, image = find_face()
        user_box = calc_user()
    except:
        break

    for i in range(len(detect_result)):
        center_x = detect_result[i]['box'][0] + (detect_result[i]['box'][2] / 2)
        center_y = detect_result[i]['box'][1] + (detect_result[i]['box'][3] / 2)

        detect_result[i]['face_center'] = (int(center_x), int(center_y))

        # 얼굴에 사각형 그리기
        cv2.rectangle(image, (detect_result[i]['box'][0], detect_result[i]['box'][1]), (detect_result[i]['box'][0]+detect_result[i]['box'][2], detect_result[i]['box'][1] + detect_result[i]['box'][3]), (0, 155, 255), 2)
        cv2.putText(image, f"{i} : {detect_result[i]['radianText']}", (detect_result[i]['box'][0], detect_result[i]['box'][1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    for i in range(len(user_box)):
        user_check = {'user' : i, "stay" : False, 'sNum' : user_box[i]['description'], 'box_coordinate' : None}
        check_radian = {'sNum' : user_box[i]['description']}
        overLap = 0
        for j in range(len(detect_result)):
            if ((user_box[i]['box_coordinate'][0] <= detect_result[j]['face_center'][0]) and (detect_result[j]['face_center'][0] <= user_box[i]['box_coordinate'][2])) \
                and ((user_box[i]['box_coordinate'][1] <= detect_result[j]['face_center'][1]) and (detect_result[j]['face_center'][1]<= user_box[i]['box_coordinate'][3])):

                if overLap == 0:
                    user_check = {'user': i, "stay": True, 'sNum': user_box[i]['description'], 'exist': True,
                                  'box_coordinate': detect_result[j]['box']}
                    overLap += 1
                else:
                    key = find_key(user_box, user_box[i]['description'])
                    if (detect_result[key]['face_size'] >= detect_result[i]['face_size']):
                        print("pass")
                    else:
                        user_check = {'user': key, "stay": True, 'sNum': user_box[key]['description'], 'exist': True,
                                      'box_coordinate': detect_result[key]['box']}
                #user_check = {'user' : i, "stay" : True, 'sNum' : user_box[i]['description'], 'radian' : detect_result[j]['radianValue']}

                if user_box[i]['description'] in user_list:
                    for z in range(len(check_total_radian)):
                        if user_box[i]['description'] == check_total_radian[z]['sNum']:
                            print(check_total_radian[z]['sNum'], user_box[i]['description'])
                            try:
                                check_total_radian[z]['radian'].append(detect_result[j]['radianValue'])
                                #print(check_total_radian[z])
                                # score : 1분에 한번씩 각도를 측정하면서 +- 5도 안이면 1점 아니면 0점이라고 가정 누적해서 스코어링
                                if (check_total_radian[z]['radian'][0] - 5 < detect_result[j]['radianValue']) and (check_total_radian[z]['radian'][0]+5 > detect_result[j]['radianValue']):
                                    check_total_radian[z]['score'] = check_total_radian[z]['score'] + 1
                                else:
                                    check_total_radian[z]['score'] = check_total_radian[z]['score'] + 0

                            except:
                                check_total_radian[z]['radian'] = [detect_result[j]['radianValue']]
                                check_total_radian[z]['score'] = 0
                else:
                    check_radian = {'sNum': user_box[i]['description'], 'radian': [detect_result[j]['radianValue']], 'score': 0}

                break

        #print(user_box[i]['box_coordinate'][0])
        cv2.rectangle(image, (user_box[i]['box_coordinate'][0], user_box[i]['box_coordinate'][1]), (user_box[i]['box_coordinate'][2], user_box[i]['box_coordinate'][3]), (0, 155, 255), 2)
        user_total_check.append(user_check)
        if user_box[i]['description'] not in user_list:
            check_total_radian.append(check_radian)
            user_list.append(user_box[i]['description'])

    print('========================================')
    print(user_total_check)
    print('========================================')
    print()
    for i in range(len(user_total_check)):
        if user_total_check[i]['box_coordinate'] != None:
            cv2.rectangle(image, (user_total_check[i]['box_coordinate'][0], user_total_check[i]['box_coordinate'][1]), \
                          (user_total_check[i]['box_coordinate'][0] + user_total_check[i]['box_coordinate'][2],
                           user_total_check[i]['box_coordinate'][1] + user_total_check[i]['box_coordinate'][3]),
                          (0, 155, 255), 2)
            cv2.putText(image, f"user : {user_total_check[i]['sNum']}",
                        (user_total_check[i]['box_coordinate'][0], user_total_check[i]['box_coordinate'][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    print()
    print('========================================')
    print(f'user_box{number} : ', user_box)
    print(len(user_box))
    print(f'user_result{number} : ', user_total_check)
    print(len(user_total_check))
    print(f'derect_result{number} : ', detect_result)
    print(len(detect_result))
    print(f'{number}:', check_total_radian)
    print(len(check_total_radian))
    print('========================================')
    cv2.imwrite(f'./result{number}.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    notice_user_check()
    number = number+1

    time.sleep(10)
    '''
    if len(check_total_radian[0]['sNum']) == 3:
        break
    '''


#cv2.imwrite('./result.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
print('만점 : ', number-2)
#=====================================
# 회의를 끝내고 엑셀로 저장되는 학번과 점수
# 엑셀의 저장 명은 년도 - 월 - 일
#=====================================
df = pd.DataFrame(check_total_radian)
df = df.drop(['radian'], axis = 1)
#df.insert(2,"만점", number-2,True)
df.to_csv(f'./{d.year}-{d.month}-{d.day}.csv', index = None)

print(datetime.datetime.now())
#print(user_total_check)
#print(check_total_radian)
#print(len(check_total_radian), len(user_total_check))

