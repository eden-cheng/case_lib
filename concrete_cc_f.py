import tool_f

yaml_path_relation = "./yaml_files/relation.yaml"

class Concrete_cc():
    def __init__(self, ws, yaml_title, yaml_content):
        #提取relations yaml中的行列对应关系
        self.t_obj = tool_f.Tool()
        self.row_relation = (self.t_obj.yaml_manage(yaml_path_relation))['row_relation']
        #实例化tool_f文件中的Tool类，方便后面调用case的展开方法
        self.ex_obj = tool_f.Expand(ws, yaml_title, yaml_content)
    
    def func(self, name):
        if name in self.row_relation.keys():
            relation = self.row_relation[name]
            self.ex_obj.expand_group(relation)

    def cc_ex(self):
        for i in range(1, 30):
            self.func('cc_' + str(i))