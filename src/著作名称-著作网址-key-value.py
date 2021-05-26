import json
import re
from time import sleep
from lxml import etree
import requests
#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+", encoding='utf-8')
    f1.write(str_data)
    f1.close()
#设置请求头模拟浏览器对服务器发出请求
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
#将人物网址-著作-著作网址.txt的所有元素按行存入列表final中
final = []
with open('./人物网址-著作-著作网址.txt',encoding = 'utf-8') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
#提取列表final中所有著作去重后百度百科链接的部分
j1 = 2
linklist = []
while j1 < len(final):
    linklist.append(final[j1])
    j1 += 2
#提取去重后的著作的属性值并将著作名称-著作网址-key-value四元组加入著作名称-著作网址-key-value.txt中
num = 2
path_file_name = "著作名称-著作网址-key-value.txt"
while num < len(final):
    value2 = []
    value1 = []
    url = final[num]
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    key = html.xpath('//dt[contains(@class,"basicInfo-item name")]')
    value = html.xpath('//dd[contains(@class,"basicInfo-item value")]')
    name = html.xpath('//h1//text()')
    for item in value:
        value1.append(item.xpath('.//text()'))
    #print(value1)
    for object in key:
        akey = object.text.split("\xa0")
        bkey = "".join(akey)
        ckey = "".join(list(bkey))
        value2.append(ckey)    #用value2列表存储key值
    whole = []
    whole = list(zip(value2, value1))
    print(whole)
    for object in whole:
        str = '\t'.join([name[0], final[num], object[0]])
        print(str)
        create_str_to_txt(str,path_file_name)
        print(object[1])
        i = 0
        while i < len(object[1]):
            item1 = object[1][i]
            # 去掉注释序列号以及除'\n外的非中文字符'
            print("字符在列表中的位置：", i)
            if object[1][i] != '\n':
                if object[1][i].find("[") != -1 or object[1][i] == '\xa0':
                   # print("注释")
                    object[1].remove(object[1][i])
                    i = i
                    continue
            # 把列表中第一个字符串的最开始的'\n'转换为'\t'
            if i == 0:
                #print("第一个", repr('\n'))
                list_str = list(object[1][i])
                list_str[0] = '\t'
                object[1][i] = ''.join(list_str)
            # 长度大于2的列表判断非最后一个元素"\n"的位置是否有不在最开始的，若有将该'\n'转化为'\t'
            if len(object[1]) > 1 and i != len(object[1]) - 1 and object[1][i].find('\n') != 0 and object[1][i].find('\n') != -1:
                print("中间位置", repr("\n"), "转换")
                list_str = list(object[1][i])
                list_str[len(list_str) - 1] = '\t'
                object[1][i] = ''.join(list_str)
                # 删除书名号里面的顿号和逗号
            if object[1][i].find("》") != -1 or object[1][i].find("《")!=-1:
                print(1)
                object[1][i] = object[1][i].replace("、", "")
                object[1][i] = object[1][i].replace("，", "")
                print("去掉顿号后：",object[1][i])
            # 在遇到后书名号且不在列表最后位置，在后书名号后面加"\t"
            if object[1][i].find("》") != -1:
                # print("书名号后",repr('\t'))
                list_str = list(object[1][i])
                if i != len(object[1]) - 1:
                    tar = list_str.index("》")
                    list_str.insert(tar + 1, '\t')
                    object[1][i] = ''.join(list_str)
                else:
                    symbol = 0
                    for j in [l1 for l1, x in enumerate(object[1][i]) if x == "》"]:
                        # 判断后书引号后面是不是前书引号，若是才进行加入"\t"的操作
                        print(j, symbol)
                        tar = j + symbol
                        print(list_str[tar + 1])
                        if list_str[tar + 1] == "《":
                            list_str.insert(tar + 1, '\t')
                            object[1][i] = ''.join(list_str)
                            print(list(object[1][i]))
                            symbol += 1
                        else:
                            symbol = 0
            print(list(object[1][i]))

            i += 1
        print(object[1])
        str = "".join(object[1])
        str = re.sub('\n', '\t', str)
        str = str.lstrip("\t")
        str = str.rstrip("\t")
        l1 = str.split('\t')
        create_str_to_txt("\t",path_file_name)
        create_str_to_txt(json.dumps(l1, ensure_ascii=False),path_file_name)
        create_str_to_txt("\n",path_file_name)
    print(num)
    if num + 3 < len(final):
        num += 3
    else:
        break
    sleep(1 + num * 0.01)

