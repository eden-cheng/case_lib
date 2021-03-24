import yaml
import openpyxl

yaml_relation_file = "./yaml_files/relation.yaml"

with open (yaml_relation_file, encoding = 'utf-8') as file_obj:
    content = file_obj.read()
    yaml_dic = yaml.load(content, Loader=yaml.FullLoader)
    case_col = yaml_dic['output_titles']
    # case_row = list(yaml_dic['row_relation'].values())
    # print(case_row)

def relation(ws):
    dic_col = {}
    for columns in ws[2]:
        for col_name in case_col:
            if col_name == columns.value:
                dic_col[col_name] = columns.column
    print(dic_col)
    dic_row = {}
    for rows in ws['A']:
        dic_row[rows.value] = rows.row
    print(dic_row)

wb = openpyxl.load_workbook('TC_lib.xlsx')
ws = wb['CC-lib']
relation(ws)