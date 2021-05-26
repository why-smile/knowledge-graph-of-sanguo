#函数create_str_to_txt(str_data, path_file_name)调用时需传入两个参数，第一个参数str_data用于接受写入的字符串，第二个参数path_file_name用于接受字符串要写入的目标文件
def create_str_to_txt(str_data,path_file_name):
    f1 = open(path_file_name, "a+")
    f1.write(str_data)
    f1.close()
#将规范化关系人物网址.txt的所有元素按行存入列表final中
final1 = []
with open('规范化关系人物网址.txt') as f:
    for line in f:
        mid = line.split('\t')
        for item in mid:
            item = item.strip('\n')
            final1.append(item)
print(final1)
#提取列表final中关系人物规范后百度百科链接的部分
j1 = 1
linklist1 = []
while j1 < len(final1):
    linklist1.append((final1[j1]))
    j1 += 2
#提取列表final中关系人物规范后名字的部分
name1 = []
j2 = 0
while j2 < len(final1):
    name1.append(final1[j2])
    j2 += 2
#将得到的规范后的关系人物及其网址加入网址信息_人物名称.txt中
whole = []
whole = list(zip(name1, linklist1))
path_file_name = "./网址信息_人物名称.txt"
for item in whole:
        str = '\t'.join([item[0], item[1]])
        print(str)
        create_str_to_txt(str, path_file_name)
        create_str_to_txt('\n', path_file_name)
