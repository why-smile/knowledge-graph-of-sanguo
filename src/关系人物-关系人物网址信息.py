from time import sleep
from lxml import etree
import requests
#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+")
    f1.write(str_data)
    f1.close()
#设置请求头模拟浏览器对服务器发出请求
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
final = []
#将网址信息_人物名称.txt的所有元素按行存入列表final中
with open('./网址信息_人物名称.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
print(final)
#提取列表final中三国人物百度百科链接的部分
j1 = 1
linklist = []
while j1 < len(final):
    linklist.append(final[j1])
    j1 += 2
#提取与三国时期人物所有有关系的人物并将其名字与网址加入关系人物名称-关系人物网址未去重.txt中
i = 0
path_file_name = "./关系人物名称-关系人物网址未去重.txt"
while i < len(linklist):
    url = linklist[i]
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    name = html.xpath('//li[contains(@class,"lemma-relation-item")]//span[contains(@class,"title")]//text()')
    linklist1 = html.xpath('//li[contains(@class,"lemma-relation-item")]//a[contains(@class,"lemma-relation-link")]//@href')
    whole = []
    whole = list(zip(name, linklist1))
    for item in whole:
        str = item[0] + "\t" + "https://baike.baidu.com" + item[1]
        print(str)
        create_str_to_txt(str, path_file_name)
        create_str_to_txt('\n', path_file_name)
    i += 1
    sleep(1 + i * 0.0001)



