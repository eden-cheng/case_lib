import openpyxl
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

    def cc(self):
        ws = self.wb['CC-lib']
        print('\033[0;34m' + 'CC HILL to do' +'\033[0m')

    # def ilc(self):
    #     ws = self.wb['ILC-lib']
    #     print('\033[0;34m' + 'ILC HILL to do' +'\033[0m')