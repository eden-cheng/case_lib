import openpyxl
from veh_concrete import veh_case_f
import tool_f

yaml_path_file = "./yaml_files/file.yaml"

class Feature_ex():
    def __init__(self, lib):
        self.lib = lib
        self.wb = openpyxl.load_workbook(self.lib)
        self.t_obj = tool_f.Tool()

    def test(self):
        self.cc()
        # self.ilc()

    def func(self, values_name):
        #将cc的实车测试特征值存储为字典
        veh_value = self.t_obj.charact_value(yaml_path_file, values_name)
        return veh_value

    def cc(self):
        print('\033[0;31m'+'CC VEH doing'+ '\033[0m')
        ws = self.wb['CC-lib']
        #外层循环是空载，满载，卡车目标
        for key,value in self.func('cc_charact_values').items():
            obj = veh_case_f.Case_ex(ws, key, value)
            obj.cc_ex()
            arr = obj.ex_obj.arr
            self.t_obj.import_data(arr, key)    #前面通过cc_ex后，具体化的case全部添加到字典中，现在写入excel中

    # def ilc(self):
    #     ws = self.wb['ILC-lib']
    #     print('\033[0;34m' + 'ILC VEH to do' +'\033[0m')
