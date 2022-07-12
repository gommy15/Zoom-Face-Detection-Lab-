x = [{'a': 10, 'b': 20, 'c': 30, 'd': [40]}, {'a': 20, 'b': 30, 'c': 40, 'd': [50]}]
print(len((x['d'] == 20)))
x['d'].append(50)
x['e'] = [60]
print(len((x['d'] == 20)))
print((x['d'] == 20))
print(x)