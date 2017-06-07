import csv

PT_list = list()

with open('../Data/ARDS_NMBA_sorted.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    drug_list = []
    chart_list = []
    c_idx_list = []
    d_idx_list = []
    idx = 1
    prev_id = 0
    count_idx = 0

    for row in reader:
        current_id = row['subject_id']
        if (idx == 1) and (prev_id != current_id):
            print count_idx, 'start'
            prev_id = current_id
            PT_data = dict()
            PT_data['subject_id'] = row['subject_id']
            PT_data['gender'] = row['gender']
            PT_data['DOB'] = row['dob']
            PT_data['DOD'] = row['dod']
            # PT_data['Age'] = row['Age']
            PT_data['drug_1'] = row['drug']
            PT_data['drug_1_start'] = row['startdate']
            PT_data['drug_1_dosage'] = row['dose_val_rx']
            PT_data['chart_label_1'] = row['label']
            PT_data['drug_1_end'] = row['enddate']
            PT_data['chart_label_1_value'] = row['value']
            # PT_data['survival'] = row['Survival']

            drug_list = [row['drug']]
            chart_list = [row['label']]

            d_idx = 1
            c_idx = 1
            # print idx, PT_data
            idx += 1
            continue
        if (idx != 1) and (prev_id != current_id):
            count_idx += 1
            print idx, len(PT_list), count_idx, c_idx, d_idx
            prev_id = current_id
            PT_list.append(PT_data)
            c_idx_list.append(c_idx)
            d_idx_list.append(d_idx)

            PT_data = dict()
            PT_data['subject_id'] = row['subject_id']
            PT_data['gender'] = row['gender']
            PT_data['DOB'] = row['dob']
            PT_data['DOD'] = row['dod']
            # PT_data['Age'] = row['Age']
            PT_data['drug_1'] = row['drug']
            PT_data['drug_1_start'] = row['startdate']
            PT_data['drug_1_dosage'] = row['dose_val_rx']
            PT_data['chart_label_1'] = row['label']
            PT_data['drug_1_end'] = row['enddate']
            PT_data['chart_label_1_value'] = row['value']
            # PT_data['survival'] = row['Survival']

            drug_list = [row['drug']]
            chart_list = [row['label']]

            d_idx = 1
            c_idx = 1
            idx += 1
            continue
        elif prev_id == current_id:
            idx += 1
            prev_id = current_id
            if row['drug'] not in drug_list:
                d_idx += 1
                key_name = 'drug_'+str(d_idx)
                key_name_start = key_name + '_start'
                key_name_end = key_name + '_end'
                key_name_dosage = key_name + '_dosage'
                PT_data[key_name] = row['drug']
                PT_data[key_name_start] = row['startdate']
                PT_data[key_name_end] = row['enddate']
                PT_data[key_name_dosage] = row['dose_val_rx']
                drug_list.append(row['drug'])

            if row['label'] not in chart_list:
                c_idx += 1
                key_name = 'chart_label_'+str(c_idx)
                Key_name_value = key_name + '_value'
                PT_data[key_name] = row['label']
                PT_data[Key_name_value] = row['value']
                chart_list.append(row['label'])
                # print idx, PT_data

print len(PT_list), idx
print PT_data

n_cidx = max(c_idx_list)
n_didx = max(d_idx_list)
head_list = ['subject_id','gender','DOB','DOD']
for i in range(1,n_didx+1):
    drug = 'drug_' + str(i)
    drug_start = drug + '_start'
    drug_end = drug + '_end'
    drug_dosage = drug + '_dosage'
    head_list.append(drug)
    head_list.append(drug_dosage)
    head_list.append(drug_start)
    head_list.append(drug_end)
for i in range(1,n_cidx+1):
    chart = 'chart_label_' + str(i)
    chart_value = chart + '_value'
    head_list.append(chart)
    head_list.append(chart_value)

with open('../Data/clean_ARDS_NMBA.csv','wb') as f:
    w = csv.DictWriter(f,head_list )
    w.writeheader()
    w.writerows(PT_list)



print "-"*100


