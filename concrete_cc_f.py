import tool_f

yaml_path_relation = "./yaml_files/relation.yaml"

class Concrete_cc():
    def __init__(self, ws, yaml_content):
        #提取relations yaml中的行列对应关系
        self.t_obj = tool_f.Tool()
        self.row_relation = (self.t_obj.yaml_manage(yaml_path_relation))['row_relation']
        #实例化tool_f文件中的Tool类，方便后面调用case的展开方法
        self.ex_obj = tool_f.Expand(ws, yaml_content)
    
    def func(self, name):
        relation = self.row_relation[name]
        self.ex_obj.expand_group(relation)

    def cc_ex(self):
        self.func('cc_1')   #主车以限速巡航，无目标
        self.func('cc_2')   #运动中进AD，无目标加速至限速
        self.func('cc_8')   #approach, 接近静止目标车辆
        self.func('cc_11')  #cutin, 切入后目标车减速