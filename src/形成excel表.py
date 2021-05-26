#encoding = utf-8
import xlwt
import json
final1 = []
with open(r'./网址-名称-key-value.txt',encoding = 'utf-8') as f:
    for line in f:
        line = line.strip('\n')
        final1.extend(line.split('\t'))
wb = xlwt.Workbook(encoding = 'ascii')
ws = wb.add_sheet('人物属性')
ws.write(0, 0, label='属性名称')
ws.write(0, 1, label='属性类型')
ws.write(0, 2, label='范例')
ws.write(0, 3, label='属性频次')
i = 2
key = []
while i < len(final1):
    if not final1[i] in key:
        key.append(final1[i])
    i += 4
i = 0
for item in key:
    ws.write(i+1, 0, label=item)
    label = "str"
    for j in [j for j,x in enumerate(final1) if x == item]:
        if len(json.loads(final1[j + 1])) > 1:
            label = "list"
    ws.write(i + 1, 1, label=label)
    ws.write(i+1, 2, label=json.loads(final1[final1.index(item)+1]))
    ws.write(i+1, 3, label=final1.count(item))
    i += 1
final1 = []
with open(r'./著作名称-著作网址-key-value.txt',encoding = 'utf-8') as f:
    for line in f:
        line = line.strip('\n')
        final1.extend(line.split('\t'))
ws1 = wb.add_sheet('著作属性')
ws1.write(0, 0, label='属性名称')
ws1.write(0, 1, label='属性类型')
ws1.write(0, 2, label='范例')
ws1.write(0, 3, label='属性频次')
i = 2
key = []
while i < len(final1):
    if not final1[i] in key:
        key.append(final1[i])
    i += 4
i = 0
for item in key:
    ws1.write(i+1, 0, label=item)
    label = "str"
    for j in [j for j,x in enumerate(final1) if x == item]:
        if len(json.loads(final1[j + 1])) > 1:
            label = "list"
    ws1.write(i + 1, 1, label=label)
    ws1.write(i+1, 2, label=json.loads(final1[final1.index(item)+1]))
    ws1.write(i+1, 3, label=final1.count(item))
    i += 1
wb.save('./表单.xls')

