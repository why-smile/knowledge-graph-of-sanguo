#打印网址信息-人名
import urllib
from time import sleep
import re
from lxml import etree
import requests
#设置请求头模拟浏览器对服务器发出请求
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
url = 'https://baike.baidu.com/item/%E4%B8%89%E5%9B%BD/5428?fr=aladdin#4_2'
response =requests.get(url, headers=header)
#response.encoding = 'utf-8'
#print(response.text)#打印网页源码的简便方法
html = etree.HTML(response.text)
#html_txt = etree.tostring(html, encoding='utf-8')
#print(html_txt.decode())#打印网页源码的复杂方法
#搜索三国百度百科网页中所有具有超链接的词语节点以及超链接节点并将它们分别存入content列表以及linklist列表中
linklist = html.xpath('//div[contains(@class,"para")]/a[contains(@target,"_blank")]/@href')
content = html.xpath('//div[contains(@class,"para")]/a[contains(@target,"_blank")]')
#将从外部搜索到的三国时期的人物存入列表a2中
f = open(r'三国人物.txt', encoding="utf-8")
a = list(f)
b = "".join(a)
c = b.split('、')
a2 = list(c)
#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data, path_file_name):
    f1 = open(path_file_name, "a+")
    f1.write(str_data)
    f1.close()
#设置与作为参考过滤的三国时期的人物长度相同的标记列表，初始化列表元素全为0
value = []
num = 0
for ai in a2:
    value.append(0)
    num += 1
#将从网页提取出的链接里过滤掉非三国时期人物的部分同时将提取出的网页规范化以及进行网址转换
i = 0
j = 0
count = 0
path_file_name = './网址信息_人物名称.txt'
while i < num:
    for item in content:
        if value[i] == 0 and item.text == a2[i]:   #判断该人物是否为三国时期的人物
            value[i] = 1                         #若已经比对过的人物将它在标记列表中数值标记为1
            str = "\t".join([item.text, "https://baike.baidu.com"+linklist[content.index(item)]]) #将名称和网址用'\t'连接成新的字符串后赋值给str
            url = "https://baike.baidu.com" + linklist[content.index(item)]  #将得到的三国时期人物的网址赋值给变量url
            print(url)
            #对提取的网址再进行一次判断，判断是否为三国时期人物的网址
            response = requests.get(url, headers=header)
            html = etree.HTML(response.text)
            str1 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//span//text()')
            key = html.xpath('//dt[contains(@class,"basicInfo-item name")]//text()')
            value1 = html.xpath('//dd[contains(@class,"basicInfo-item value")]')
            if len(str1) == 0:
                if len(key) != 0:
                    if ''.join(key).find("出生日期") != -1:
                        print('有出生日期')
                        std = value1[key.index("出生日期")].xpath('.//text()')
                        std1 = std[0].strip('\n')
                        if std1.find("年") != -1:
                            std1 = std1[0:std1.index("年")]
                            if std1 >= u'\u0030' and std1 <= u'u\u0039':
                                if int(std1) > 1000:
                                    print("不是三国人")
                                    i += 1
                                    continue
                                else:
                                    str = str
                                    print("是三国人")
                            else:
                                print("不是数字")
                                str = str
                        else:
                            print("没有年分")
                            str = str
                    else:
                        print("没有多义项 ")
                        str = str
                else:
                    str2 = html.xpath('//ul[contains(@class,"custom_dot  para-list list-paddingleft-1")]//a[contains(text(),"汉") or contains(text(),"三国") or contains(text(),"袁")]//@data-lemmaid')
                    str = str + '/' + str2[0]
                    print("纯跳转页")
            elif str1[0].find("汉") != -1 or str1[0].find("晋") != -1 or str1[0].find("吴") != -1 or str1[0].find("魏") != -1 or str1[0].find("蜀") != -1  or str1[0].find("三国时期") != -1 or str1[0].find("三国演义") != -1:
                print("保留页面2")
                str = str
            else:
                print("继续寻找页面")
                if len(str2) != 0:
                    str2 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//a[contains(@title,"汉") or contains(@title,"晋") or contains(@title,"吴")   or contains(@title,"蜀") or contains(@title,"三国时期") or contains(@title,"三国演义")]//@href')
                    str2[0] = str2[0].strip('#viewPageContent')
                    str = "\t".join([item.text, "https://baike.baidu.com" + str2[0]])
                else:
                    print("不用改，直接去除")
                    i += 1
                    continue
            # 将与三国时期人物同名人物网址替换为三国时期人物网址并对网址的格式进行规范化
            if str.count('/') == 4:
                str1 = html.xpath('//div//@data-lemmaid')
                print("换过网址")
                str = str + '/' + str1[0]
            else:
                str = str
            list1 = str.split('/')
            name = html.xpath('//h1//text()')
            list1[4] = urllib.parse.quote(name[0], encoding='utf-8')
            str = "/".join(list1)
            print(str)
            create_str_to_txt(str,path_file_name)
            create_str_to_txt("\n",path_file_name)
            count += 1
            sleep(1 + i * 0.001)
    i += 1
print(count)





