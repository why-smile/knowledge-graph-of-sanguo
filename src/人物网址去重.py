#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+")
    f1.write(str_data)
    f1.close()
#将规范化关系人物网址.txt的所有元素按行存入列表list2中
list2 = []
with open('./网址信息_人物名称.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            list2.append(item)
path_file_name = './去重最终版网址信息_人物名称.txt'
#提取列表list2中关系人物百度百科链接的部分
linklist2 = []
name2 = []
j1 = 1
while j1 < len(list2):
    linklist2.append(list2[j1])
    j1 += 2
#提取列表list2中名字的部分
i1 = 0
while i1 < len(list2):
    name2.append(list2[i1])
    i1 += 2
#对于所有三国人物以链接是否相同为标准进行去重，去重后加入去重最终版网址信息_人物名称.txt中
whole = []
whole = list(zip(name2, linklist2))
all = []
name = []
for item in whole:
    if not item[1] in all:
        str = "\t".join([item[0], item[1]])
        print(str)
        all.append(item[1])
        name.append(item[0])
        create_str_to_txt(str,path_file_name)
    else:
        continue

