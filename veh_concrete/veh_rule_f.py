import tool_f
import re

yaml_path_relation = "./yaml_files/relation.yaml"

class Rule():
    def __init__(self, case, arr_action, arr_odd, arr_geo_tag, arr_pre_tag):
        self.case = case
        self.arr_action = arr_action
        self.arr_odd = arr_odd
        self.arr_pre_tag = arr_pre_tag
        self.arr_geo_tag = arr_geo_tag
        self.temp = []
        #提取relations yaml中的行列对应关系
        t_obj = tool_f.Tool()
        self.colum_relation = (t_obj.yaml_manage(yaml_path_relation))['colum_relation']

    def func(self, title):
        return self.case[self.colum_relation[title]].value

    def geo_ex(self):
        """对道路几何展开。既有对summary_odd的追加，也有tag"""
        geos = ['default', 'curve', 'uphill', 'downhill']
        for geo in geos:
            if geo in self.arr_geo_tag['geo']:
                if geo in self.arr_odd.keys():
                    for i in self.arr_odd[geo]:
                        dic = {'summary' : self.func('summary') + ' (' + i + '_' + geo + ')', 'road_geo' : geo}
                        self.temp.append(dic)

    def summary_action_ex(self):
        if self.arr_action:
            for title, para_arr in self.arr_action.items():
                arr = []
                for para in para_arr:
                    for j in self.temp:
                        k = j.copy()
                        k['summary'] = k['summary'].replace(title, para)
                        arr.append(k)
                self.temp = arr

    def pre_ex(self):
        arr = []
        for i in self.temp:
            for key, value in self.arr_pre_tag.items():
                i[key] = value
            arr.append(i.copy())   #注意，一定要 .copy()
        self.temp = arr
    
    def excution_input(self):
        str01 = "initial status of hv"
        str02 = "initial status of tv"
        str03 = "action of hv"
        str04 = "action of tv"
        excution = {str01: self.func(str01), 
                    str02: self.func(str02), 
                    str03: self.func(str03), 
                    str04: self.func(str04)}
        for i in self.temp:
            for key, value in excution.items():
                i[key] = value

    def criteria_input(self):  #后面需要根据通过指标来展开
        str05 = 'subjective criteria'
        str06 = 'objective criteria'
        excution = {str05: self.func(str05), 
                    str06: self.func(str06)}
        for i in self.temp:
            for key, value in excution.items():
                i[key] = value

    def feature_input(self):
        for dic in self.temp:
            dic['feature'] = self.func('feature')

    def id_ex(self):
        i = 1
        for dic in self.temp:
            dic['id'] = self.func('id') + '-' + str(i)
            i += 1   #python没有++运算符