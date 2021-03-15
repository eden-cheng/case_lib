import openpyxl
import concrete_cc_f
import tool_f

yaml_path_file = "./yaml_files/file.yaml"

class Concrete():
    def __init__(self, lib):
        self.lib = lib
        self.wb = openpyxl.load_workbook(self.lib)
        self.t_obj = tool_f.Tool()

    def cc_veh_test(self):
        print('\033[0;31m'+'CC VEH doing'+ '\033[0m')
        ws = self.wb['CC-lib']
        #将cc的实车测试特征值存储为字典
        cc_veh_value = self.t_obj.charact_value(yaml_path_file, 'cc_charact_values')
        #外层循环是空载，满载，卡车目标
        for key,value in cc_veh_value.items():
            obj = concrete_cc_f.Concrete_cc(ws, value)
            obj.cc_ex()
            arr = obj.ex_obj.arr
            self.t_obj.import_data(arr, key)    #前面通过cc_ex后，具体化的case全部添加到字典中，现在写入excel中

    def ilc_veh_test(self):
        ws = self.wb['ILC-lib']
        #ilc_veh_value = self.yaml_obj.charact_value(yaml_path_file, 'ilc_charact_values')
        print('\033[0;34m' + 'ILC VEH doing' +'\033[0m')

    def cc_hill_test(self):
        ws = self.wb['CC-lib']
        print('\033[0;34m' + 'CC HILL doing' +'\033[0m')

    def ilc_hill_test(self):
        ws = self.wb['ILC-lib']
        print('\033[0;34m' + 'ILC HILL doing' +'\033[0m')
