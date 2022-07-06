from google_api import user
#user = [{'description': '20200756', 'coordinate': (211, 424, 288, 446)}, {'description': '20190201', 'coordinate': (210, 757, 287, 778)}, {'description': '20200998', 'coordinate': (184, 1090, 262, 1112)}, {'description': '20200996', 'coordinate': (768, 424, 846, 445)}, {'description': '20181112', 'coordinate': (769, 758, 846, 779)}, {'description': '20178888', 'coordinate': (796, 1090, 874, 1111)}, {'description': '20200654', 'coordinate': (1088, 1422, 1167, 1444)}, {'description': '20190777', 'coordinate': (1381, 424, 1459, 446)}, {'description': '20210101', 'coordinate': (1354, 757, 1429, 777)}, {'description': '20200745', 'coordinate': (1354, 1090, 1430, 1112)}, {'description': '20200992', 'coordinate': (1938, 423, 2016, 445)}, {'description': '20200759', 'coordinate': (1966, 756, 2044, 779)}, {'description': '20213523', 'coordinate': (1966, 1089, 2043, 1111)}]

#사용자간 사이 높이, 너비 구하기
for j in range(len(user)):
    if abs(user[0]['coordinate'][0]- user[j]['coordinate'][0]) >= 100:
        width = user[j]['coordinate'][0] - user[0]['coordinate'][0]
        break

height = user[1]['coordinate'][1] - user[0]['coordinate'][1]

print("width : ",width, "height : ", height)

user_box = user
#각 사용자의 박스 좌표 구하기
for i in range(len(user)):
    user_box[i]['box_coordinate'] = (int(user[i]['coordinate'][0]), int(user[i]['coordinate'][1]), int(width), int(height))

print(user_box)