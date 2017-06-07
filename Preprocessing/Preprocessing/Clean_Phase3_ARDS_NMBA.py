import csv
import numpy as np

Tidal = ['Tidal Volume (Obser)','Tidal Volume (Set)','Tidal Volume (Spont)',
        'Sigh Tidal Volume', 'Tidal Volume (set)','Tidal Volume (observed)',
        'Tidal Volume (spontaneous)',]
Plateau = 'Plateau Pressure'


with open('../Data/clean2_ARDS_NMBA.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    row_idx = 0
    dict_list = list()
    for row in reader:
        row_idx += 1
        row_dict = dict()
        row_dict['subject_id'] = row['subject_id']
        row_dict['age'] = row['age']
        if row['gender'] == 'F':
            row_dict['gender'] = 0
        else:
            row_dict['gender'] = 1
        row_dict['mortality'] = row['mortality']
        row_dict['NMBA'] = 1

        # tidal_val = list()
        # for tidal in Tidal:
        #     if tidal == 'Tidal Volume (Obser)' or tidal == 'Tidal Volume (observed)':
        #         if row[tidal] != '':
        #             row_dict['Tidal'] = float(row[tidal])
        #         else:
        #             continue
        #     else:
        #         if row[tidal] != '':
        #             if float(row[tidal]) > 0:
        #                 tidal_val.append(float(row[tidal]))
        #             else:
        #                 continue
        #         else:
        #             continue
        row_dict['Tidal'] = row['Tidal Volume (Obser)']
        row_dict['Plateau Pressure'] = row['Plateau Pressure']
        row_dict['FiO2'] = row['FiO2 Set']
        row_dict['PaCO2'] = row['Arterial PaCO2']
        row_dict['PaO2'] = row['Arterial PaO2']
        row_dict['pH'] = row['Arterial pH']
        row_dict['PEEP'] = row['PEEP Set']
        dict_list.append(row_dict)


head_list = ['subject_id','mortality','NMBA','age','gender',
             'Tidal','Plateau Pressure','FiO2','PaCO2',
             'PaO2','pH','PEEP']



with open('../Data/clean_final_ARDS_NMBA_v1.csv','wb') as f:
    w = csv.DictWriter(f,head_list )
    w.writeheader()
    w.writerows(dict_list)
