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
#将去重最终版网址信息_人物名称.txt的所有元素按行存入列表final中
final = []
with open('./去重最终版网址信息_人物名称.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
#提取列表final中所有人物去重后百度百科链接的部分
i = 1
link = []
while i < len(final):
    link.append(final[i])
    i += 2
#提取列表final中所有人物名字的部分
i1 = 0
name1 = []
while i1 < len(final):
    name1.append(final[i1])
    i1 += 2
#通过人物信息框中属性值中含有“作”字符的条件提取出每个人物的带有链接的作品名称以及对应的链接并将提取的链接加入人物名称-人物网址-著作名称-著作网址.txt中
name = []
j = 0
while j < len(link):
    url = link[j]
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    key = html.xpath('//dt[contains(@class,"basicInfo-item name")]//text()')
    #将信息框中key的名称提取至列表key中
    value1 = html.xpath('//dd[contains(@class,"basicInfo-item value")]')
    print(len(key),len(value1))
    if ''.join(key).find('作')!=-1:
        for object in key:
            if object.find('作')!=-1:
                index = key.index(object)
        linklist = value1[index].xpath('./a[contains(@target,"_blank")]//@href')
        name = value1[index].xpath('./a//text()')
        print(linklist)
        print(name)
        value = zip(name, linklist)
        for item in value:
                str = '\t'.join([name1[j],url,item[0],"https://baike.baidu.com"+item[1]])
                print(str)
                path_file_name = './人物名称-人物网址-著作名称-著作网址.txt'
                create_str_to_txt(str,path_file_name)
                create_str_to_txt('\n',path_file_name)
    sleep(1 + j * 0.0001)
    j += 1