from veh_concrete import veh_feature_f
from hill_concrete import hill_feature_f
import tool_f

def input_file():
    """从yaml中提取场景库的输入路径"""
    yaml_path_file = "./yaml_files/file.yaml"
    t_obj = tool_f.Tool()    #tool_f 类中的有 Tool类 和 Yaml_manage 类，对其中 Yaml_manage 类做实例化
    file_dic = t_obj.yaml_manage(yaml_path_file)      #将文件路径的yaml文件处理为“字典”格式
    input_file = file_dic['lib_path']     #从字典中，提取场景库的文件路径
    return input_file

#实车测试
veh_ex = veh_feature_f.Feature_ex(input_file())
veh_ex.test()

#仿真测试
hill_ex = hill_feature_f.Feature_ex(input_file())
hill_ex.test()