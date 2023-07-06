import json

with open('data.json') as newfile:
    data = json.load(newfile)




def a_func():
    for names in data:
        if names["id"] == 1:
            return names['movies']


data2 = a_func()
print(data2)
for key in data2:
    print(key['name'])