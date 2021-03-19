import tool_f
from veh_concrete import veh_expand_f

yaml_path_relation = "./yaml_files/relation.yaml"

class Case_ex():
    def __init__(self, ws, yaml_title, yaml_content):
        #提取relations yaml中的行列对应关系
        self.t_obj = tool_f.Tool()
        self.row_relation = (self.t_obj.yaml_manage(yaml_path_relation))['row_relation']
        #实例化tool_f文件中的Tool类，方便后面调用case的展开方法
        self.ex_obj = veh_expand_f.Expand(ws, yaml_title, yaml_content)
    
    def func(self, name):
        if name in self.row_relation.keys():
            relation = self.row_relation[name]
            self.ex_obj.expand_group(relation)

    def cc_ex(self):
        self.func('cc_1')
        self.func('cc_2')
        self.func('cc_3')
        self.func('cc_4')
        self.func('cc_5')
        self.func('cc_6')
        self.func('cc_7')
        self.func('cc_8')
        self.func('cc_9')
        self.func('cc_10')
        self.func('cc_11')
        self.func('cc_12')
        self.func('cc_13')
        self.func('cc_14')

    def ilc_ex(self):
        print("hello ilc")