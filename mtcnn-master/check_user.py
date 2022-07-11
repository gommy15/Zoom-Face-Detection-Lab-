import os.path

import cv2
import datetime
import pandas as pd
from plus_dlib import box_result, image, radianText_list, radianValue_list
#from calc_coordinate import user_box

d = datetime.datetime.now()
user_box = [{'description': '20200998', 'coordinate': (184, 1090, 262, 1112), 'box_coordinate': (184, 757, 741, 1090)}, {'description': '20200996', 'coordinate': (768, 424, 846, 445), 'box_coordinate': (768, 91, 1325, 424)}, {'description': '20181112', 'coordinate': (769, 758, 846, 779), 'box_coordinate': (769, 425, 1326, 758)}, {'description': '20178888', 'coordinate': (796, 1090, 874, 1111), 'box_coordinate': (796, 757, 1353, 1090)}, {'description': '20200756', 'coordinate': (211, 424, 288, 446), 'box_coordinate': (211, 91, 768, 424)}, {'description': '20200654', 'coordinate': (1088, 1422, 1167, 1444), 'box_coordinate': (1088, 1089, 1645, 1422)}, {'description': '20190777', 'coordinate': (1381, 424, 1459, 446), 'box_coordinate': (1381, 91, 1938, 424)}, {'description': '20210101', 'coordinate': (1354, 757, 1429, 777), 'box_coordinate': (1354, 424, 1911, 757)}, {'description': '20200745', 'coordinate': (1354, 1090, 1430, 1112), 'box_coordinate': (1354, 757, 1911, 1090)}, {'description': '20200992', 'coordinate': (1938, 423, 2016, 445), 'box_coordinate': (1938, 90, 2495, 423)}, {'description': '20200759', 'coordinate': (1966, 756, 2044, 779), 'box_coordinate': (1966, 423, 2523, 756)}, {'description': '20190201', 'coordinate': (210, 757, 287, 778), 'box_coordinate': (210, 424, 767, 757)}, {'description': '20213523', 'coordinate': (1966, 1089, 2043, 1111), 'box_coordinate': (1966, 756, 2523, 1089)}]
user_total_check = []
face_coordinate = []
save_total_csv = []

time = f'{d.hour}:{d.minute}'

if os.path.isfile(f'./{d.year}-{d.month}-{d.day}.csv'):
    radian_df = pd.read_csv(f'./{d.year}-{d.month}-{d.day}.csv', index_col='sNum')

for i in range(len(box_result)):
    center_x = box_result[i][0] + (box_result[i][2] / 2)
    center_y = box_result[i][1] + (box_result[i][3] / 2)

    face_coordinate.append((int(center_x), int(center_y)))

    # 얼굴에 사각형 그리기
    cv2.rectangle(image, (box_result[i][0], box_result[i][1]), (box_result[i][0]+box_result[i][2], box_result[i][1] + box_result[i][3]), (0, 155, 255), 2)
    cv2.putText(image, radianText_list[i], (box_result[i][0], box_result[i][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)


for i in range(len(user_box)):
    user_check = {'user' : i, "stay" : False, 'sNum' : user_box[i]['description']}
    save_csv = {'sNum' : user_box[i]['description']}
    for j in range(len(face_coordinate)):
        if (user_box[i]['box_coordinate'][0] <= face_coordinate[j][0] & face_coordinate[j][0] <= user_box[i]['box_coordinate'][2]) \
            & (user_box[i]['box_coordinate'][1] <= face_coordinate[j][1] & face_coordinate[j][1]<= user_box[i]['box_coordinate'][3]):
            user_check = {'user' : i, "stay" : True, 'sNum' : user_box[i]['description'], 'radian' : radianText_list[j]}
            if os.path.isfile(f'./{d.year}-{d.month}-{d.day}.csv') == False:
                save_csv = {'sNum': user_box[i]['description'], time : radianValue_list[j]}
            else :
                #save_csv = {f'{d.hour}:{d.minute}': radianValue_list[j]}
                save_csv = radianValue_list[j]
                #add_df = pd.DataFrame({time : radianValue_list[j]}, index=[f"{user_box[i]['description']}"])
                #radian_df = pd.concat([radian_df, add_df], axis=1)

            break

    user_total_check.append(user_check)
    save_total_csv.append(save_csv)


if os.path.isfile(f'./{d.year}-{d.month}-{d.day}.csv') == False:
    radian_df = pd.DataFrame(save_total_csv)
    #radian_df = radian_df.sort_values('sNum')
    print(radian_df)

if os.path.isfile(f'./{d.year}-{d.month}-{d.day}.csv') == False:
    radian_df.to_csv(f'./{d.year}-{d.month}-{d.day}.csv', index = None)
else:
    radian_df.to_csv(f'./{d.year}-{d.month}-{d.day}.csv')
print(radian_df)

cv2.imwrite('./result.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
print(datetime.datetime.now())
print(user_total_check)

