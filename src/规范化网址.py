import re
import urllib
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
#将关系人物名称-关系人物网址未去重.txt的所有元素按行存入列表final中
final = []
with open('./关系人物名称-关系人物网址未去重.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final.append(item)
#提取列表final中关系人物百度百科链接的部分
j1 = 1
linklist = []
while j1 < len(final):
    linklist.append(final[j1])
    j1 += 2
#提取列表final中名字的部分
i1 = 0
name1 = []
while i1 < len(final):
    name1.append(final[i1])
    i1 += 2
#将关系人物通过限制出生日期的年份的条件以及所在朝代或者与主体人物关系的条件进行过滤后加上数字形成规范网址
i = 0
path_file_name = "./规范化关系人物网址.txt"
while i < len(linklist):
    url = linklist[i]
    str = name1[i] +'\t' +linklist[i]
    print(str)
    response = requests.get(url, headers=header)
    html = etree.HTML(response.text)
    str1 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//span//text()')
    key = html.xpath('//dt[contains(@class,"basicInfo-item name")]//text()')
    value = html.xpath('//dd[contains(@class,"basicInfo-item value")]')
    if len(str1) == 0 :
        #有信息框
        if len(key)!=0:
            if ''.join(key).find("出生日期") != -1:
                print('有出生日期')
                std = value[key.index("出生日期")].xpath('.//text()')
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
                        str =str
                        print("不是数字")
                else:
                    str =str
                    print("没有年分")
            else:
                print("没有多义项 ")
                str = str
        #没有信息框
        else:
            str2 = html.xpath('//ul[contains(@class,"custom_dot  para-list list-paddingleft-1")]//a[contains(text(),"汉") or contains(text(),"三国") or contains(text(),"袁")]//@data-lemmaid')
            print("纯跳转页")
            str = str + '/' + str2[0]
    elif str1[0].find("汉") != -1 or str1[0].find("晋") != -1 or str1[0].find("吴") != -1 or str1[0].find("魏") != -1 or str1[0].find("蜀") != -1 or str1[0].find("三国时期") != -1 or str1[0].find("三国历史人物") != -1 or str1[0].find("三国演义") != -1 or str1[0].find("三国时人物") != -1 or str1[0].find("妻")!=-1 or str1[0].find("父")!=-1 or str1[0].find("子")!=-1 or str1[0].find("三国人物")!=-1 or str1[0].find("孙")!=-1 or str1[0].find("女")!=-1 or str1[0].find("妾")!=-1:
        print("保留页面2")
        str = str
    else:
        print("继续寻找页面")
        str2 = html.xpath('//ul[contains(@class,"polysemantList-wrapper cmn-clearfix")]//a[contains(@title,"汉") or contains(@title,"晋") or contains(@title,"吴")   or contains(@title,"蜀") or contains(@title,"三国时期") or contains(@title,"三国演义")]//@href')
        if len(str2)!=0:
            print("改网址")
            str2[0] = str2[0].strip('#viewPageContent')
            str = "\t".join([name1[i], "https://baike.baidu.com" + str2[0]])
        else:
            print("不用改，直接去除")
            i += 1
            continue
    # 将与三国时期人物同名人物网址替换为三国时期人物网址
    if str.count('/') == 4:
        print("网址格式不对")
        str1 = html.xpath('//div//@data-lemmaid')
        str = str + '/' + str1[0][0]
    else:
        str =str
    list1 = str.split('/')
    name = html.xpath('//h1//text()')
    list1[4] = urllib.parse.quote(name[0], encoding='utf-8')
    str = "/".join(list1)
    print(str)
    create_str_to_txt(str, path_file_name)
    create_str_to_txt("\n ", path_file_name)
    print(i)
    i += 1
    sleep(1 + i * 0.000001)


