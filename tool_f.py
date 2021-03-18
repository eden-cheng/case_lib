import openpyxl
import rule_f
import yaml
import os

yaml_path_file = "./yaml_files/file.yaml"
yaml_path_relation = "./yaml_files/relation.yaml"
yaml_path_pre = "./yaml_cc/cc_prerequsite.yaml"

class Expand():
    def __init__(self, ws, yaml_title, yaml_content):
        self.ws = ws
        self.yaml_title = yaml_title
        self.yaml_content = yaml_content
        #之所以放在此处，而不是放在下面函数中，
        #一方面，因为当cc-1,cc-8,cc-11轮流调用下面的expand函数时，可以在全局变量上追加。如果做成局部变量，会被覆盖
        #另一方面，当多种特征值yaml文件调用时，self.arr会被初始化清空
        self.arr = []

    def func(self, name):
        return (self.yaml_content[name])['para_group']

    def expand_group(self, relation):
        #循环case二级目录，cc_3_1,cc_3_2,cc_3_3
        for id, row_num in relation.items():
            arr_para_group = []
            case = self.ws[row_num]
            if id in self.yaml_content.keys():
                #循环case的参数组
                for key, value in self.func(id).items():
                    #step1: 从yaml文件获取不同odd的实车测试的特征值
                    para_action = value['para_action']
                    para_odd = value['para_odd']
                    geo_tag = (self.yaml_content[id])['geo_tag']
                    #step2：从yaml文件获取不同odd的默认tag
                    dic_pre = Tool().yaml_manage(yaml_path_pre)
                    if self.yaml_title in dic_pre.keys():
                        pre_tag = dic_pre[self.yaml_title]
                    #step3: 将规则实例化，借助Rule_cc_veh类
                    rule_obj = rule_f.Rule(case, para_action, para_odd, geo_tag, pre_tag)
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
        rule_obj.excution_input()    #将执行部分的内容填到展开的case中
        rule_obj.criteria_input()    #将通过条件部分的内容填到展开的case中
        rule_obj.feature_input()

class Tool():
    def yaml_manage(self, file_path):
        """载入yaml配置文件，并存为字典格式"""
        with open (file_path, encoding = 'utf-8') as file_obj:
            content = file_obj.read()
            yaml_dic = yaml.load(content, Loader=yaml.FullLoader)
            return yaml_dic

    def charact_value(self, file_path, test_name):
        """将yaml中的多组特征值文件路径，提取出成参数字典"""
        #实例化 Yaml_manage 类，并从yaml中提取出实车测试特征值文件的路径构成字典
        #键是实车测试对象，比如noload, payload
        #值是特征值文件的路径
        yaml_s = (self.yaml_manage(file_path))[test_name]
        #分别将实车测试特征值文件中的内容提取出来，形成一个庞大的特征值字典。
        #键是实车测试的对象， 比如noload, payload
        #值是特征值
        cc_veh_value = {}
        for key, value in yaml_s.items():
            cc_veh_value[key] = self.yaml_manage(value)
        return cc_veh_value

    def import_data(self, arr, yaml_title):
        """将output整理的列表，写入表格，仅做写入，不做列表的追加等操作"""
        out_path = (self.yaml_manage(yaml_path_file))['case_path_cc_veh']
        wb = openpyxl.Workbook()
        ws = wb.active
        titles = ['id', 'feature', 'summary', 'weather', 'illumination', 'load', 'speed_limit', 
                'tv', 'road_geo', 'initial status of hv', 'initial status of tv', 'action of hv', 
                'action of tv', 'subjective criteria', 'objective criteria']
        #将标题填入excel 
        for i in range(len(titles)):
            ws.cell(row = 1, column = i + 1).value = titles[i]
        #将expand整理出的case，从字典形式填入Excel中
        j = 2
        for dic in arr:
            k = 1
            for title, content in dic.items():
                ws.cell(row = j, column = k).value = dic[titles[k-1]]
                k += 1
            j = j + 1
        #python生成文件路径
        isExists = os.path.exists(out_path)
        if not isExists:
            os.makedirs(file_path)
        wb.save(out_path + yaml_title + '.xlsx')