from lxml import etree
import requests
#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+")
    f1.write(str_data)
    f1.close()
#设置请求头模拟浏览器对服务器发出请求
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
#将去重最终版网址信息_人物名称.txt的所有元素按行存入列表final中
final = []
with open('去重最终版网址信息_人物名称.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
print(final)
#提取列表final中所有人物去重后百度百科链接的部分
linklist = []
j = 1
while j < len(final):
    linklist.append(final[j])
    j += 2
#对于所有提取的三国人物进行关系的提取，限制与该人物有关系的人物必须在之前提取出的三国人物中
i = 0
while i<len(linklist):
    print(i)
    url = linklist[i]
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    relationship = html.xpath('//li[contains(@class,"lemma-relation-item")]//span[contains(@class,"name")]//text()')
    name = html.xpath('//li[contains(@class,"lemma-relation-item")]//a[contains(@class,"lemma-relation-link")]//@href')
    link = []
    for item in name:
        link.append("https://baike.baidu.com"+item)
    whole = []
    whole = zip(relationship, link)
    path_file_name = './网址-关系-网址.txt'
    for item in whole:
        if item[1] in linklist:
            str1 ='\t'.join([item[0],item[1]])
            str =  url +'\t'+ str1
            print(str)
            create_str_to_txt(str,path_file_name)
            create_str_to_txt('\n',path_file_name)

    i += 1