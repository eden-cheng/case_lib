import openpyxl
import rule_cc_veh_f
import yaml
import os

yaml_path_file = "./yaml_files/file.yaml"
yaml_path_relation = "./yaml_files/relation.yaml"

class Expand():
    def __init__(self, ws, yaml_content):
        self.ws = ws
        self.yaml_content = yaml_content
        #之所以放在此处，而不是放在下面函数中，
        #一方面，因为当cc-1,cc-8,cc-11轮流调用下面的expand函数时，可以在全局变量上追加。如果做成局部变量，会被覆盖
        #另一方面，当多种特征值yaml文件调用时，self.arr会被初始化清空
        self.arr = []  

    def expand_group(self, relation):
        for id, row_num in relation.items():
            #获取case行
            case = self.ws[row_num]
            #如果特征值yaml中的键与relation中的id不对应会报错，所以需要先做判断
            if id in self.yaml_content.keys():
                #step1: 从yaml文件中导入实车测试的特征值
                para = (self.yaml_content[id])['para']
                tag = (self.yaml_content[id])['tag']
                #step2: 将规则实例化，借助Rule_cc_veh类
                rule_obj = rule_cc_veh_f.Rule_cc_veh(case, para, tag)
                #step3: 展开成具体case，以字典的格式
                self.expand(rule_obj)    #rule_obj的传入参数是一个实例化类的对象
    
    def expand(self, rule_obj):   
        rule_obj.road_geo_ex()       #将道路曲率或坡道等几何因素展开，一方面展开tag，一方面展开参数
        rule_obj.tag_ex()            #将光照，天气，目标类型等tag展开
        rule_obj.tv_ex()             #将目标车的可设参数展开
        rule_obj.excution_input()    #将执行部分的内容填到展开的case中
        rule_obj.criteria_input()    #将通过条件部分的内容填到展开的case中
        rule_obj.other_ex()          #将id，feature名填到case中
        #每次被调用时，将当前obj.temp的内容“追加”到arr中
        for dic in rule_obj.temp: 
            self.arr.append(dic)

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