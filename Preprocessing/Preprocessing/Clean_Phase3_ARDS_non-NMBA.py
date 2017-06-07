import csv
import numpy as np

Tidal = ['Tidal Volume (Obser)','Tidal Volume (Set)','Tidal Volume (Spont)',
        'Sigh Tidal Volume', 'Tidal Volume (set)','Tidal Volume (observed)',
        'Tidal Volume (spontaneous)',]
Plateau = 'Plateau Pressure'


with open('../Data/clean2_ARDS_non-NMBA.csv') as csvfile:
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
        row_dict['NMBA'] = 0

        tidal_val_list = list()
        tidal_val = ''
        row_dict['Tidal'] = '-'
        for tidal in Tidal:
            if tidal == 'Tidal Volume (Obser)' or tidal == 'Tidal Volume (observed)':
                if row[tidal] != '':
                    tidal_val = float(row[tidal])
                    row_dict['Tidal'] = float(row[tidal])
                    break
                else:
                    continue
            else:
                if row[tidal] != '':
                    tidal_val = row[tidal]
                    if float(row[tidal]) > 0:
                        tidal_val_list.append(float(row[tidal]))
                    else:
                        continue
                else:
                    continue
        if len(tidal_val_list) > 0:
            row_dict['Tidal'] = np.median(tidal_val_list)

        if row['Plateau Pressure'] != '':
            row_dict['Plateau Pressure'] = row['Plateau Pressure']
        else:
            row_dict['Plateau Pressure'] = '-'

        if row['FiO2 Set'] != '':
            row_dict['FiO2'] = row['FiO2 Set']
        elif row['FiO2 Set'] == '' and row['FiO2 (Analyzed)'] != '':
            row_dict['FiO2'] = row['FiO2 (Analyzed)']
        elif row['FiO2 Set'] == '' and row['FiO2 (Analyzed)'] == '' and row['Vision FiO2'] != '':
            row_dict['FiO2'] = row['Vision FiO2']
        else:
            row_dict['FiO2'] = '-'

        row_dict['PaCO2'] = '-'
        if row['Arterial PaCO2'] != '':
            row_dict['PaCO2'] = row['Arterial PaCO2']

        row_dict['PaO2'] = '-'
        if row['Arterial PaO2'] != '':
            row_dict['PaO2'] = row['Arterial PaO2']

        row_dict['pH'] = '-'
        if row['Arterial pH'] != '':
            row_dict['pH'] = row['Arterial pH']
        elif row['Arterial pH'] == '' and row['Art.pH'] != '':
            row_dict['pH'] = row['Art.pH']
        elif row['Arterial pH'] == '' and row['Art.pH'] == '' and row['GI [pH]'] != '':
            row_dict['pH'] = row['GI [pH]']
        elif row['Arterial pH'] == '' and row['Art.pH'] == '' and row['GI [pH]'] == '' and row['Emesis [pH]'] != '':
            row_dict['pH'] = row['Emesis [pH]']
        elif row['Arterial pH'] == '' and row['Art.pH'] == '' and row['GI [pH]'] == '' and row['Emesis [pH]'] == '' and row['GI pH'] != '':
            row_dict['pH'] = row['GI pH']

        row_dict['PEEP'] = '-'
        if row['PEEP Set'] != '':
            row_dict['PEEP'] = row['PEEP Set']
        elif row['PEEP Set'] == '' and row['Total PEEP Level'] != '':
            row_dict['PEEP'] = row['Total PEEP Level']
        elif row['PEEP Set'] == '' and row['Total PEEP Level'] == '' and row['PEEP set'] != '':
            row_dict['PEEP'] = row['PEEP set']
        elif row['PEEP Set'] == '' and row['Total PEEP Level'] == '' and row['PEEP set'] == '' and row['Auto-PEEP Level'] != '':
            row_dict['PEEP'] = row['Auto-PEEP Level']

        if row_dict['Tidal'] == '-' or row_dict['Plateau Pressure'] == '-' or row_dict['FiO2'] == '-' or row_dict['PaCO2'] == '-' or row_dict['PaO2'] == '-' or row_dict['pH'] == '-' or row_dict['PEEP'] == '-':
            continue

        dict_list.append(row_dict)


head_list = ['subject_id','mortality','NMBA','age','gender',
             'Tidal','Plateau Pressure','FiO2','PaCO2',
             'PaO2','pH','PEEP']


with open('../Data/clean_final_ARDS_non-NMBA_v1.csv','wb') as f:
    w = csv.DictWriter(f,head_list )
    w.writeheader()
    w.writerows(dict_list)
