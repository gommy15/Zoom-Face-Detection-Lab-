from plus_dlib import face_coordinate
from calc_coordinate import user_box

#user_box = [{'description': '20200756', 'coordinate': (280, 329, 329, 342), 'box_coordinate': (280, 115, 638, 329)}, {'description': '20190201', 'coordinate': (279, 543, 328, 557), 'box_coordinate': (279, 329, 637, 543)}, {'description': '20200998', 'coordinate': (262, 758, 312, 771), 'box_coordinate': (262, 544, 620, 758)}, {'description': '20200996', 'coordinate': (638, 330, 689, 341), 'box_coordinate': (638, 116, 996, 330)}, {'description': '20181112', 'coordinate': (639, 544, 689, 558), 'box_coordinate': (639, 330, 997, 544)}, {'description': '20178888', 'coordinate': (657, 758, 707, 771), 'box_coordinate': (657, 544, 1015, 758)}, {'description': '20200654', 'coordinate': (845, 973, 894, 985), 'box_coordinate': (845, 759, 1203, 973)}, {'description': '20190777', 'coordinate': (1033, 329, 1084, 342), 'box_coordinate': (1033, 115, 1391, 329)}, {'description': '20210101', 'coordinate': (1015, 544, 1064, 556), 'box_coordinate': (1015, 330, 1373, 544)}, {'description': '20200745', 'coordinate': (1016, 758, 1065, 770), 'box_coordinate': (1016, 544, 1374, 758)}, {'description': '20200992', 'coordinate': (1392, 329, 1443, 342), 'box_coordinate': (1392, 115, 1750, 329)}, {'description': '20200759', 'coordinate': (1410, 543, 1460, 559), 'box_coordinate': (1410, 329, 1768, 543)}, {'description': '20213523', 'coordinate': (1410, 758, 1459, 771), 'box_coordinate': (1410, 544, 1768, 758)}]
user_total_check = []

for i in range(len(user_box)):
    user_check = {'user' : i, "stay" : False, 'ssn' : user_box[i]['description']}
    for j in range(len(face_coordinate)):
        if (user_box[i]['box_coordinate'][0] <= face_coordinate[j][0] & face_coordinate[j][0] <= user_box[i]['box_coordinate'][2]) \
            & (user_box[i]['box_coordinate'][1] <= face_coordinate[j][1] & face_coordinate[j][1]<= user_box[i]['box_coordinate'][3]):
            user_check = {'user' : i, "stay" : True, 'ssn' : user_box[i]['description']}
            break

    user_total_check.append(user_check)

print(user_total_check)

