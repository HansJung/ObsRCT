import csv
import pandas as pd

dict_list = []
NMBA_list = ['rocuronium','cisatracurium','succinylcholine','atracurium','mivacurium','pancuronium','vecuronium']

Chart_name_list = ['Tidal Volume (Obser)','Tidal Volume (Set)','Tidal Volume (Spont)',
                   'Sigh Tidal Volume', 'Tidal Volume (set)','Tidal Volume (observed)',
                   'Tidal Volume (spontaneous)',
                   'Plateau Pressure',
                   'FiO2 Set', 'FiO2 (Analyzed)', 'Vision FiO2',
                   'Arterial PaCO2', 'Arterial PaO2',
                   'Arterial pH','Art.pH', 'Venous pH', 'GI [pH]','Emesis [pH]','GI pH',
                   'Total PEEP Level','PEEP set', 'Auto-PEEP Level' ,'PEEP Set']


with open('../Data/clean_ARDS_NMBA.csv') as csvfile:
    row_idx = -1
    n_drug_NMBA = 165
    n_chart_NMBA = 17
    reader = csv.DictReader(csvfile)
    chart_list = []
    drug_list = []
    drug_duration_list = []


    for row in reader:
        row_idx += 1
        drug_start_list = []
        drug_end_list = []
        row_dict = dict()
        row_dict['subject_id'] = row['subject_id']
        row_dict['gender'] = row['gender']
        for idx in range(1,n_drug_NMBA+1):
            drug_idx = 'drug_' + str(idx)
            if row[drug_idx] != '':
                drug_name = row[drug_idx]
                drug_dosage = drug_name + '_dosage'
                drug_start = drug_name + '_start'
                drug_end = drug_name + '_end'
                drug_duration = drug_name + '_duration'
                for NMBA_elem in NMBA_list:
                    if NMBA_elem in str.lower(drug_name):
                        # row_dict[drug_name] = row[drug_idx]
                        # row_dict[drug_dosage] = row[drug_idx + '_dosage']
                        row_dict[drug_name] = row[drug_idx + '_dosage']
                        # row_dict[drug_start] = row[drug_idx+'_start']
                        # row_dict[drug_end] = row[drug_idx+'_end']
                        row_dict[drug_duration] = float(row[drug_idx+'_end']) - float(row[drug_idx+'_start'])
                        if drug_duration not in drug_duration_list:
                            drug_duration_list.append(drug_duration)
                        drug_start_list.append(float(row[drug_idx+'_start']))
                        drug_end_list.append(float(row[drug_idx+'_end']))
                        if drug_name not in drug_list:
                            drug_list.append(drug_name)


        for idx in range(1,n_chart_NMBA+1):
            chart_idx= 'chart_label_' + str(idx)
            chart_val = chart_idx + '_value'
            if row[chart_idx] != '':
                chart_name = row[chart_idx]
                for chart_elem in Chart_name_list:
                    if chart_elem == chart_name:
                        row_dict[chart_elem] = row[chart_val]
        Age = round(( (min(drug_start_list) - float(row['DOB'])) /365.25),0)
        if Age < 0:
            Age = -1 * Age
        elif Age > 100:
            Age = 90
        row_dict['age'] = Age
        if row['DOD'] == '' or (float(row['DOD']) - max(drug_end_list) > 90):
            row_dict['mortality'] = 1
        else:
            row_dict['mortality'] = 0
        dict_list.append(row_dict)

head_list = ['subject_id','age','gender','mortality']
head_list += drug_list
head_list += drug_duration_list
head_list += Chart_name_list

print head_list


with open('../Data/clean2_ARDS_NMBA.csv','wb') as f:
    w = csv.DictWriter(f,head_list )
    w.writeheader()
    w.writerows(dict_list)
