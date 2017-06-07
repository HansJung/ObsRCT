import pandas as pd
import csv

row_dict = dict()
row_list = list()

# Constructing drug and chart list
with open('../Data/clean_ARDS_NMBA.csv') as csvfile:
    File = csv.DictReader(csvfile)
    idx = 0
    n_drug_NMBA = 165
    n_chart_NMBA = 17

    drug_list = []
    drug_dict = dict()
    chart_list = []

    for row in File:
        idx += 1
        for drug_idx in range(1,n_drug_NMBA+1):
            key_name = 'drug_' + str(drug_idx)
            drug_1 = row[key_name]
            if drug_1 not in drug_list:
                drug_list.append(drug_1)
                drug_dict[drug_1] = 1
            else:
                drug_dict[drug_1] += 1


    # print len(drug_list)

with open('../Data/clean_ARDS_non-NMBA.csv') as csvfile:
    File = csv.DictReader(csvfile)
    idx = 0
    n_drug_non_NMBA = 194
    n_chart_non_NMBA = 18

    for row in File:
        idx += 1
        for drug_idx in range(1,n_drug_NMBA+1):
            key_name = 'drug_' + str(drug_idx)
            drug_1 = row[key_name]
            if drug_1 not in drug_list:
                drug_list.append(drug_1)
                drug_dict[drug_1] = 1
            else:
                drug_dict[drug_1] += 1


with open('../Data/clean_ARDS_NMBA.csv') as csvfile:
    File = csv.DictReader(csvfile)
    idx = 0
    n_drug_NMBA = 165
    n_chart_NMBA = 17

    drug_list = []
    drug_dict = dict()
    chart_list = []

    for row in File:
        idx += 1
        for drug_idx in range(1,n_drug_NMBA+1):
            key_name = 'drug_' + str(drug_idx)
            drug_1 = row[key_name]
            if drug_1 not in drug_list:
                drug_list.append(drug_1)
                drug_dict[drug_1] = 1
            else:
                drug_dict[drug_1] += 1


#




#
#
#     # print len(drug_list)
# for idx, key in enumerate(drug_dict):
#     print idx, "|", key, "|", drug_dict[key]