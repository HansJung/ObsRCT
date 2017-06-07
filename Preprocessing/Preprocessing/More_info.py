import csv
from datetime import datetime

def DateDiff(date1,date2):
    date_obj1 = date1.split(" ")[0]
    date_obj2 = date2.split(" ")[0]
    date_object = datetime.strptime(str(date_obj1), '%m/%d/%y')
    date_object2 = datetime.strptime(str(date_obj2), '%m/%d/%y')
    delta = date_object2 - date_object
    return str(delta).split(" ")[0]

def DateExt(date1):
    date1_obj = date1.split(" ")[0]
    date_obj = datetime.strptime(str(date1_obj), '%m/%d/%y')
    return date_obj


NMBA_list = ['rocuronium','cisatracurium','succinylcholine','atracurium','mivacurium','pancuronium','vecuronium']

with open('../Data/clean_ARDS_NMBA.csv') as csvfile:
    File = csv.DictReader(csvfile)
    idx = 0
    n_drug_NMBA = 165
    n_chart_NMBA = 17

    drug_list = []
    drug_date_list = []
    drug_dict = dict()
    chart_list = []

    for row in File:
        idx += 1
        for drug_idx in range(1,n_drug_NMBA+1):
            key_name = 'drug_' + str(drug_idx)
            if row[key_name] != '':
                key_start = key_name + '_start'
                key_end = key_name +'_end'
                drug_1 = row[key_name]
                drug_1_start = row[key_start]
                drug_1_end = row[key_end]
                if drug_1_start != '' and drug_1_end != '':
                    drug_1_date = DateDiff(drug_1_start,drug_1_end)

                if drug_1 not in drug_list:
                    drug_list.append(drug_1)
                    drug_dict[drug_1] = 1
                else:
                    drug_dict[drug_1] += 1
            else:
                break