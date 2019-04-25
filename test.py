import copy

a = ['a', 'b', 'c', 'd']
b = [1, 3]

# temp =[]
# for i in b:
#     temp.append(a[i])
#
# for x in a:
#     if x not in temp:
#         temp.append(x)
#     else:
#         temp.remove(x)
#
# print(temp)
#
#
#
# for x in b:
#     del a[x]
#     a.insert(0,None)
#
# for x in a:
#     if x:
#         print(x)
c = []
for index, x in enumerate(b, 0):
    if index == 0:
        c.append(x)
    else:
        x = x - index
        c.append(x)
for x in c:
    del a[x]

print(a)
