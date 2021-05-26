import xlwt
import json
wb = xlwt.Workbook(encoding = 'ascii')
final = []
all = []
with open('./著作名称-著作网址-key-value.txt',encoding = 'utf-8') as f:
    for line in f:
        mid = line.split('\t')
        mid[3] = mid[3].strip('\n')
        mid[3] = json.loads(mid[3])
        l1 = mid[3]
        mid.pop(3)
        for item in l1:
            mid.append(item)
        final.append(mid)
        for item in mid:
            all.append(item)
print(final)
key = []
for item in final:
    key.append(item[2])
    key.append(len(item))
#将属性及整个列表长度放入列表key中
akey = []
count = []
i= 0
while i < len(key):
    akey.append(key[i])
    count.append(key[i+1])
    i += 2
#将属性名称放入列表akey中,将列表长度放入列表count中
bkey = []
btype   = []
for item in akey:
    if item not in bkey:
        bkey.append(item)
        btype.append("str")
for item in bkey:
    l1 = [i for i,x in enumerate(akey) if x == item]
    for object in l1:
        if count[object]>4:
            btype[bkey.index(item)]='list'
k = 0
whole = []
while k<len(bkey):
        whole.append(bkey[k])
        whole.append(btype[k])
        k += 1
#去重后的属性名称和列表长度放入whole列表中
ws = wb.add_sheet('作品属性')
i = 0
ws.write(0, 0, label='属性名称')
ws.write(0, 1, label='属性类型')
ws.write(0, 2, label='范例')
ws.write(0, 3, label='属性频次')
j = 1
while i < len(whole):
    ws.write(j, 0, label=whole[i])
    ws.write(j, 1, label=whole[i+1])
    ws.write(j, 2, label=all[all.index(whole[i])+1])
    ws.write(j, 3, label=key.count(whole[i]))
    if i+2<len(whole):
        i += 2
        j += 1
    else:
        break
final1 = []
all1 = []
with open('./网址-名称-key-value.txt',encoding = 'utf-8') as f:
    for line in f:
        mid = line.split('\t')
        mid[3] = mid[3].strip('\n')
        mid[3] = json.loads(mid[3])
        l1 = mid[3]
        mid.pop(3)
        for item in l1:
            mid.append(item)
        final1.append(mid)
        for item in mid:
            all1.append(item)

print(all1)
key1 = []
for item in final1:
    key1.append(item[2])
    key1.append(len(item))
#将属性及整个列表长度放入列表key中
akey1 = []
count1 = []
i= 0
while i < len(key1):
    akey1.append(key1[i])
    count1.append(key1[i+1])
    i += 2
bkey1 = []
btype1   = []
for item in akey1:
    if item not in bkey1:
        bkey1.append(item)
        btype1.append("str")
for item in bkey1:
    l1 = [i for i,x in enumerate(akey1) if x == item]
    for object in l1:
        if count1[object]>4:
            btype1[bkey1.index(item)]='list'
k = 0
whole1 = []
while k<len(bkey1):
        whole1.append(bkey1[k])
        whole1.append(btype1[k])
        k += 1
#去重后的属性名称和列表长度放入whole列表中
ws = wb.add_sheet('人物属性')
i = 0
ws.write(0, 0, label='属性名称')
ws.write(0, 1, label='属性类型')
ws.write(0, 2, label='范例')
ws.write(0, 3, label='属性频次')
j = 1
while i < len(whole1):
    ws.write(j, 0, label=whole1[i])
    ws.write(j, 1, label=whole1[i+1])
    ws.write(j, 2, label=all1[all1.index(whole1[i])+1])
    ws.write(j, 3, label=key1.count(whole1[i]))
    if i+2<len(whole1):
        i += 2
        j += 1
    else:
        break
wb.save('./表单.xls')