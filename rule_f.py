import tool_f
import re

yaml_path_relation = "./yaml_files/relation.yaml"

class Rule_cc_veh():
    def __init__(self, case, arr_action, arr_odd, arr_tag):
        self.case = case
        self.arr_action = arr_action
        self.arr_odd = arr_odd
        self.arr_tag = arr_tag
        self.temp = []
        #提取relations yaml中的行列对应关系
        t_obj = tool_f.Tool()
        self.colum_relation = (t_obj.yaml_manage(yaml_path_relation))['colum_relation']

    def func(self, title):
        return self.case[self.colum_relation[title]].value

    def summary_odd_ex(self):
        """对坡度展开"""
        #默认平直路
        if '平直路' in self.arr_tag['geo']: 
            dic_default = {'summary' : self.func('summary') + ' (平直路)', 'road_geo' : '平直路'}
            self.temp.append(dic_default)
        #对弯道和坡道展开
        geos = ['curve', 'uphill', 'downhill']
        for geo in geos:
            if geo in self.arr_tag['geo']:
                #self.func_01(self.arr_odd[geo], self.case[3].value, geo)
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

    def tag_ex(self):
        tags = ['weather', 'illumination', 'load', 'tv', 'speed_limit']
        for tag in tags:
            #if tag in self.arr_tag.keys():
            arr = []
            for i in self.temp:
                for j in self.arr_tag[tag]:
                    i[tag] = j
                    arr.append(i.copy())   #注意，一定要 .copy()
            self.temp = arr
            arr = []
    
    def excution_input(self):
        excution = {'initial status of hv': self.func('initial status of hv'), 
                    'initial status of tv': self.func('initial status of tv'), 
                    'action of hv': self.func('action of hv'), 'action of tv': self.func('action of tv')}
        for i in self.temp:
            for key, value in excution.items():
                i[key] = value

    def criteria_input(self):  #后面需要根据通过指标来展开
        excution = {'subjective criteria': self.func('subjective criteria'), 
                    'objective criteria': self.func('objective criteria')}
        for i in self.temp:
            for key, value in excution.items():
                i[key] = value

    def other_ex(self):
        i = 1
        for dic in self.temp:
            dic['id'] = self.func('id') + '-' + str(i)
            dic['feature'] = self.func('feature')
            i += 1   #python没有++运算符