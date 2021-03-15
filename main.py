import concrete_f
import tool_f
#git测试02

def input_file():
    """从yaml中提取场景库的输入路径"""
    yaml_path_file = "./yaml_files/file.yaml"
    t_obj = tool_f.Tool()    #tool_f 类中的有 Tool类 和 Yaml_manage 类，对其中 Yaml_manage 类做实例化
    file_dic = t_obj.yaml_manage(yaml_path_file)      #将文件路径的yaml文件处理为“字典”格式
    input_file = file_dic['lib_path']     #从字典中，提取场景库的文件路径
    return input_file

lib = concrete_f.Concrete(input_file())
#CC 实车
lib.cc_veh_test()
#ILC 实车
lib.ilc_veh_test()
#CC 仿真
lib.cc_hill_test()
#ILC 仿真
lib.ilc_hill_test()