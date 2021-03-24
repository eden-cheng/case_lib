import openpyxl
from veh_concrete import veh_rule_f
import yaml
import os
import tool_f

yaml_path_file = "./yaml_files/file.yaml"

class Expand():
    def __init__(self, ws, yaml_title, yaml_content):
        self.ws = ws
        self.yaml_title = yaml_title
        self.yaml_content = yaml_content
        #之所以放在此处，而不是放在下面函数中，
        #一方面，因为当cc-1,cc-8,cc-11轮流调用下面的expand函数时，可以在全局变量上追加。如果做成局部变量，会被覆盖
        #另一方面，当多种特征值yaml文件调用时，self.arr会被初始化清空
        self.arr = []

    def func_para(self, name):
        return (self.yaml_content[name])['para_group']

    def func_tool(self, yaml_path):
        return tool_f.Tool().yaml_manage(yaml_path)

    def expand_group(self, relation):
        #循环case二级目录，cc_3_1,cc_3_2,cc_3_3
        for id, row_num in relation.items():
            arr_para_group = []
            case = self.ws[row_num]
            if id in self.yaml_content.keys():
                #循环case的参数组
                for key, value in self.func_para(id).items():
                    #step1: 从yaml文件获取不同odd的实车测试的特征值
                    para_action = value['para_action']
                    para_odd = value['para_odd']
                    geo_tag = value['para_odd'].keys()
                    #step2：从yaml文件获取不同odd的默认tag
                    yaml_path_pre = self.func_tool(yaml_path_file)['cc_pre']
                    dic_pre = self.func_tool(yaml_path_pre)
                    if self.yaml_title in dic_pre.keys():
                        pre_tag = dic_pre[self.yaml_title]
                    #step3: 将规则实例化，借助Rule_cc_veh类
                    rule_obj = veh_rule_f.Rule(case, para_action, para_odd, geo_tag, pre_tag)
                    #step4: 展开成具体case，以字典的格式
                    self.expand(rule_obj)    #rule_obj的传入参数是一个实例化类的对象
                    for dic in rule_obj.temp: 
                        arr_para_group.append(dic)
                    # print("@@@@@@@@@@@@@@@@@@   " + key)
                i = 1
                for dic in arr_para_group:
                    dic['id'] = id + "_" + str(i)
                    i += 1
                    # print(dic)
                    self.arr.append(dic)
                # print("@@@@@@@@@@@@@@@@@@   " + id)
                
    def expand(self, rule_obj):   
        rule_obj.geo_ex()       #将道路曲率或坡道等几何因素展开，一方面展开tag，一方面展开参数
        rule_obj.summary_action_ex()             #将目标车的可设参数展开
        rule_obj.pre_ex()            #将光照，天气，目标类型等tag展开
        rule_obj.execution_input()    #将执行部分的内容填到展开的case中
        rule_obj.criteria_input()    #将通过条件部分的内容填到展开的case中
        rule_obj.feature_input()
        rule_obj.keywords_ex()
        rule_obj.rm_execution_input()
        rule_obj.rm_criteria_input()