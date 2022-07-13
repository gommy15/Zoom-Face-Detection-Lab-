import pandas
import pandas as pd

x = [{'sNum': '20200998', 'radian': [-6.08, -6.08], 'score': 0}, {'sNum': '20200759', 'radian': [1.12, 1.12], 'score': 0}, {'sNum': '20190777', 'radian': [-9.4, -9.4], 'score': 0}]
'''
for i in range(len(x[0]['box_coordinate'])):
    print(x[0]['box_coordinate'][i])
'''

df = pd.DataFrame(x)
df_2 = df.drop(['radian'], axis = 1)
df_2.insert(2,"만점", 2,True)
df_2.to_csv(f'./test.csv', index = None)
print(df_2)