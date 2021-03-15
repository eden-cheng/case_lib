import tool_f

yaml_path_relation = "./yaml_files/relation.yaml"

class Rule_cc_veh():
    def __init__(self, case, arr_para, arr_tag):
        self.case = case
        self.arr_para = arr_para
        self.arr_tag = arr_tag
        self.temp = []
        #提取relations yaml中的行列对应关系
        t_obj = tool_f.Tool()
        self.colum_relation = (t_obj.yaml_manage(yaml_path_relation))['colum_relation']

    def func(self, title):
        return self.case[self.colum_relation[title]].value

    def road_geo_ex(self):
        """对坡度展开"""
        #默认平直路
        if '平直路' in self.arr_tag['geo']: 
            dic_default = {'summary' : self.func('summary') + ', 平直路', 'road_geo' : '平直路'}
            self.temp.append(dic_default)
        #对弯道和坡道展开
        geos = ['curve', 'uphill', 'downhill']
        for geo in geos:
            if geo in self.arr_tag['geo']:
                #self.func_01(self.arr_para[geo], self.case[3].value, geo)
                for i in self.arr_para[geo]:
                    dic = {'summary' : self.func('summary') + ', ' + i, 'road_geo' : geo}
                    self.temp.append(dic)

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

    def tv_ex(self):
        summary = ''
        if self.arr_para:      #因为yaml中para有的为空，此时.keys()会报错
            if 'tv_relate_hv_distance' in self.arr_para.keys():
                arr = []
                for dis in self.arr_para['tv_relate_hv_distance']:
                    for j in self.temp:
                        k = j.copy()
                        k['summary'] += '， tv相距hv' +  dis + '时'
                        arr.append(k)
                self.temp = arr
            if 'tv_speed' in self.arr_para.keys():
                arr = []
                for initial, target in self.arr_para['tv_speed'].items():   #tv_speed的子参数是字典
                    for j in self.temp:
                        k = j.copy()
                        k['summary'] += '， 初速度' + initial + ', 目标速度' + target
                        arr.append(k)
                self.temp = arr
            if 'tv_acc' in self.arr_para.keys():
                arr = []
                for acc in self.arr_para['tv_acc']:
                    for j in self.temp:
                        k = j.copy()
                        k['summary'] += '， 以' + acc + '加速度'
                        arr.append(k)
                self.temp = arr
    
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