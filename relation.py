import yaml
import openpyxl
import openpyxl
from ruamel import yaml

file_name = 'para.yaml'
yaml_relation_file = "./yaml_files/relation.yaml"

def func_yaml():
    with open('./yaml_files/relation.yaml', encoding='utf-8') as obj:
        content = obj.read()
        dic = yaml.load(content, Loader=yaml.Loader)    #ruamel中的读取，不是FullLoader，而是Loader
        return dic

def func_para(ws, num):
    num_int = int(num)
    return ws[num_int]

#将 A：B 字符串转成字典结构
def func_dic(string):
    key = ''
    temp = ''
    dic = {} 
    for i in string:
        if i == ":":
            key = temp
            temp = ''
            continue
        temp += i
    dic[key] = temp
    return dic

# 将下面形式字符串转换成列表结构
# a;
# b;
# c;
def func_arr_01(string):
    arr = []
    str = ""
    k = 0
    for i in string:
        k += 1
        if i == "\n":
            arr.append(str)
            str = ""
            continue
        str += i
        if k == len(string):
            arr.append(str)
            break
    return arr

#将a;b;c;转换成列表结构
def func_arr_02(string):
    arr = []
    temp = ''
    for i in string:
        if i == ';':
            arr.append(temp)
            temp = ''
            continue
        temp += i
    return arr

#将下面形式转化成列表和字典嵌套格式
# A:1;2;3;#
# B:1;2;#
# C:0;1;2;3;4;#
def func(string):
    arr01 = func_arr_01(string)
    arr02 = []
    for i in arr01:
        dic = {}
        for key,value in func_dic(i).items():
            arr = func_arr_02(value)
            dic[key] = arr
            arr02.append(dic)
    return arr02

#写入yaml文件
def output_yaml(arr, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        yaml.dump(arr, f, Dumper=yaml.RoundTripDumper)

def relation(ws):
    with open (yaml_relation_file, encoding = 'utf-8') as file_obj:
        content = file_obj.read()
        yaml_dic = yaml.load(content, Loader=yaml.Loader)
        case_col = yaml_dic['output_titles']
        # case_row = list(yaml_dic['row_relation'].values())
    dic_col = {}
    for columns in ws[2]:
        for col_name in case_col:
            if col_name == columns.value:
                dic_col[col_name] = columns.column
    print(dic_col)
    dic_row = {}
    for rows in ws['A']:
        dic_row[rows.value] = rows.row
    print(dic_row)

wb_para = openpyxl.load_workbook("para.xlsx")
ws_para = wb_para['CC-para']
row_1 = func_para(ws_para, func_yaml()['CC_1_1'])
row_2 = func_para(ws_para, func_yaml()['CC_2_1'])
row_3 = func_para(ws_para, func_yaml()['CC_3_1'])

para_odd = row_1[3].value
para_action_01 = row_2[2].value
para_action_02 = row_3[2].value

print(func_arr_01(para_odd))

#将字符串转换成列表和字典的嵌套格式
arr = func(para_action_02)
print(arr)

#将字典和列表的嵌套格式转成yaml方式写入
output_yaml(arr, file_name)

wb_relation = openpyxl.load_workbook('TC_lib.xlsx')
ws_relation = wb_relation['CC-lib']
relation(ws_relation)