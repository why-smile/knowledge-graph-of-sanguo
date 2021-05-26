import re
import urllib
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
#将人物名称-人物网址-著作名称-著作网址.txt的所有元素按行存入列表final中
final = []
with open('./人物名称-人物网址-著作名称-著作网址.txt',encoding = 'utf-8') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
#通过之前提取到的著作网址对网址的格式以及作者的姓氏的限制对网址进行过滤、对某些特殊著作进行特殊处理以及将网址统一规范后加入人物网址-著作-著作网址.txt中
i = 0
print(len(final))
path_file_name = "人物网址-著作-著作网址.txt"
print(final[0])
while i < len(final):
    url = final[i+3]
    st =  '\t'.join([final[i],final[i+1],final[i+2],final[i+3]])
    print(st)
    str = url
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    str1 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//span//text()')
    if len(str1) == 0:
        str = str
    elif str1[0].find("三国时期") != -1 or str1[0].find("汉") != -1 or str1[0].find("曹")!=-1 or str1[0].find("杨")!=-1 or str1[0].find("诸") != -1:
        str = str
    else:
        print("继续找页面")
        str2 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//a[contains(@title,"三国时期") or contains(@title,"汉")]//@href')
        str2[0] = str2[0].strip('#viewPageContent')
        str = "https://baike.baidu.com" + str2[0]
    if str.count('/') == 4:
        print("改网址")
        str1 = html.xpath('//div//@data-lemmaid')
        str = str + '/' + str1[0][0]
    else:
        str = str
    list1 = str.split('/')
    name = html.xpath('//h1//text()')
    print(name)
    list1[4] = urllib.parse.quote(name[0], encoding='utf-8')
    str = "/".join(list1)
    response1 = requests.get(str, headers=header)
    html1 = etree.HTML(response1.text)
    # 过滤掉没有信息框的网址
    if len(html1.xpath('//div[contains(@class,"basic-info cmn-clearfix")]'))!=0:
        s = "\t".join([final[i+1], '著作', str])
        print(s)
        create_str_to_txt(s , path_file_name)
        create_str_to_txt("\n", path_file_name)
        if i+4<len(final):
            print(i)
            i += 4
        else:
            print(i)
            break
        sleep(1 + i * 0.0001)
    else:
        if i+4<len(final):
            print(i)
            i += 4
        else:
            print(i)
            break
        sleep(1 + i * 0.0001)



