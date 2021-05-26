import json
import xlrd
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+",encoding = 'utf-8')
    f1.write(str_data)
    f1.close()
#预处理：将去重最终版网址信息_人物名称.txt的人物网址存入列表web中
web = []
with open('./去重最终版网址信息_人物名称.txt') as f:
    for line in f:
        line = line.strip('\n')
        line = line.split('\t')
        web.append(line[1])
#预处理：将去重最终版网址信息_人物名称.txt的人物名称存入列表name中
name = []
with open('./去重最终版网址信息_人物名称.txt') as f:
    for line in f:
        line = line.strip('\n')
        line = line.split('\t')
        name.append(line[0])
#预处理：导入xls表格，将人物属性名称和属性类型做成字典命名为person_attri_dict
data = xlrd.open_workbook('./表单.xls')
list1 = data.sheet_by_name('人物属性')
att_name = list1.col_values(0)
att_name.pop(0)
t_att_name = tuple(att_name)
att_type = list1.col_values(1)
att_type.pop(0)
person_mid = zip(att_name,att_type)
person_mid_1 = []
for item in person_mid:
    person_mid_1.append(item)
person_attri_dict = dict(person_mid_1)
print(person_attri_dict)
#预处理：将人物属性名称和属性类型做成字典命名为article_attri_dict
list1 = data.sheet_by_name('著作属性')
att_name = list1.col_values(0)
att_name.pop(0)
t_att_name = tuple(att_name)
att_type = list1.col_values(1)
att_type.pop(0)
article_mid = zip(att_name,att_type)
article_mid_1 = []
for item in article_mid:
    article_mid_1.append(item)
article_attri_dict = dict(article_mid_1)
print(article_attri_dict)
#将人物作为一个大字典big_dict导出
big_dict = dict.fromkeys(name)
print(big_dict)
#导入网址-名称-key-value.txt形成一个新字典
whole = []
whole = zip(web,name)
for object in whole:
    url = object[0]
    pname = object[1]
    #将人物属性形成字典加入pdict
    pdict = dict()
    list1 = data.sheet_by_name('网址-人物-key-value')
    l2 = list()
    for i in range(list1.nrows-1):
        row = list1.row_values(i)
        #print(row)
        if row[1] == url:
            tu = list()
            tu1 = list()
            l3 = list()
            d1 = dict()
            tu.append("@id:")
            tu.append(row[1])
            l2.append(tuple(tu))
            tu1.append("@type:")
            tu1.append("人物")
            l2.append(tuple(tu1))
            js = json.loads(row[3])
            if person_attri_dict[row[2]] == 'list':
                tu = list()
                tu.append(row[2])
                tu.append(js)
            else:
                tu = list()
                tu.append(row[2])
                tu.append(js[0])
            l2.append(tuple(tu))
    pdict.update(l2)
    print(pdict)
    #将人物名称形成字典加入pdict
    list2 = data.sheet_by_name('人物-关系-人物')
    #取出所有人物关系的名称
    relation = []
    for i in range(list2.nrows-1):
        row = list2.row_values(i)
        print(row)
        if row[0] == url:
            relation.append(row[1])
    s1 = []
    for item in relation:
        if not item in s1:
            s1.append(item)
    j = 0
    rela_val = []
    while j < len(s1):
        k = 1
        index = relation.index(s1[j])
        num = relation.count(s1[j])
        rela_val_mid = []
        while k <= num:
            row = list2.row_values(index+k-1)
            tu = list()
            tu1 = list()
            l3 = list()
            d1 = dict()
            tu.append("@id:")
            tu.append(row[2])
            l3.append(tuple(tu))
            tu1.append("@type:")
            tu1.append("人物")
            l3.append(tuple(tu1))
            d1.update(l3)
            rela_val_mid.append(d1)
            k += 1
        rela_val.append(tuple([row[1],rela_val_mid]))
        j += 1
    print(relation)
    print(rela_val)
    pdict.update(rela_val)
    print(pdict)
    #将作品名称形成字典加入pdict
    list2 = data.sheet_by_name('人物-著作-著作名称')
    #取出所有著作关系的名称
    relation = []
    for i in range(list2.nrows-1):
        row = list2.row_values(i)
        print(row)
        if row[0] == url:
            relation.append(row[1])
    s1 = []
    for item in relation:
        if not item in s1:
            s1.append(item)
    j = 0
    rela_val = []
    while j < len(s1):
        k = 1
        index = relation.index(s1[j])
        num = relation.count(s1[j])
        rela_val_mid = []
        while k <= num:
            row = list2.row_values(index+k-1)
            tu = list()
            tu1 = list()
            l3 = list()
            d1 = dict()
            tu.append("@id:")
            tu.append(row[2])
            l3.append(tuple(tu))
            tu1.append("@type:")
            tu1.append("著作")
            l3.append(tuple(tu1))
            d1.update(l3)
            rela_val_mid.append(d1)
            k += 1
        rela_val.append(tuple([row[1],rela_val_mid]))
        j += 1
    pdict.update(rela_val)
    print(pdict)
    print(pdict)
    big_dict[pname]=pdict
print(big_dict)
#循环外著作ar_big_dict字典
list2 = data.sheet_by_name('著作名称-著作网址-key-value')
web1 = []
name1 = []
for i in range(list2.nrows-1):
    row = list2.row_values(i)
    if not row[1] in web1:
        web1.append(row[1])
    if not row[0] in name1:
        name1.append(row[0])
ar_big_dict = dict.fromkeys(name1)
whole = []
whole = zip(web1,name1)
for object in whole:
    url = object[0]
    pname = object[1]
    pdict = dict()
    list1 = data.sheet_by_name('著作名称-著作网址-key-value')
    l2 = list()
    for i in range(list1.nrows-1):
        row = list1.row_values(i)
        print(row)
        if row[1] == url:
            tu = list()
            tu1 = list()
            l3 = list()
            d1 = dict()
            tu.append("@id:")
            tu.append(row[1])
            l2.append(tuple(tu))
            tu1.append("@type:")
            tu1.append("著作")
            l2.append(tuple(tu1))
            js = json.loads(row[3])
            if article_attri_dict[row[2]] == 'list':
                tu = list()
                tu.append(row[2])
                tu.append(js)
            else:
                tu = list()
                tu.append(row[2])
                tu.append(js[0])
            l2.append(tuple(tu))
    pdict.update(l2)
    ar_big_dict[pname] = pdict
    print(ar_big_dict)
#最后导出jsonld字典
jsonld = dict.fromkeys(['人物','著作'])
jsonld['人物']=big_dict
jsonld['著作'] = ar_big_dict
print(json.dumps(jsonld,ensure_ascii=False))
path_file_name = './jsonld.txt'
for item in name:
    create_str_to_txt(json.dumps(big_dict[item],ensure_ascii=False), path_file_name)
    create_str_to_txt('\n', path_file_name)
    print(json.dumps(big_dict[item],ensure_ascii=False))
for item in name1:
    create_str_to_txt(json.dumps(ar_big_dict[item], ensure_ascii=False), path_file_name)
    create_str_to_txt('\n', path_file_name)
    print(json.dumps(ar_big_dict[item], ensure_ascii=False))