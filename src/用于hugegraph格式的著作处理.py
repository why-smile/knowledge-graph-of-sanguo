import xlwt
import xlrd
workbook = xlrd.open_workbook(r'./表单.xls')
sheet1 = workbook.sheet_by_name('著作属性')
cols = sheet1.col_values(0)#获取人物所有属性名称
final = []
wb = xlwt.Workbook(encoding='ascii')
ws = wb.add_sheet('sheet1')
ws.write(0, 0, label='著作姓名')
ws.write(0, 1, label='著作网址')
i = 1
while i < len(cols):
    ws.write(0, i+1, label=cols[i])
    i += 1
final= []
name = []
web = []
with open('./著作名称-著作网址-key-value.txt',encoding = 'utf-8') as f:
    for line in f:
        mid = line.split('\t')
        mid[3] = mid[3].strip('\n')
        final.append(mid)
        if mid[0] not in name:
            name.append(mid[0])
        if mid[1] not in web:
            web.append(mid[1])
i = 1
while i < len(name):
    ws.write(i,0,label=name[i-1])
    i += 1
i = 1
while i<len(web):
    ws.write(i,1,label=web[i-1])
    i += 1
for object in web:
    for item in final:
        print(item)
        if item[1] != object:
            continue
        else:
            for item1 in cols:
                if item[2] == item1:
                    ws.write(web.index(object)+1, cols.index(item1)+1, label=item[3])
wb.save('./著作名称-著作网址-key-value(csv).xls')
