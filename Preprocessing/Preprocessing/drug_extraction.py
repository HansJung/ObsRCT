import csv

PT_list = list()

with open('../Data/testdata.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    drug_list = []
    chart_list = []
    idx = 0
    prev_id = 0
    count_idx = 0

    for row in reader:
        idx += 1
        if idx == 1:
            drug_list.append(row['drug'])
            chart_list.append(row['label'])
        else:
            if row['drug'] not in drug_list:
                drug_list.append(row['drug'])
            if row['label'] not in chart_list:
                chart_list.append(row['label'])

    for drug_elem in drug_list:
        print drug_elem
    print " "
    for chart_elem in chart_list:
        print chart_elem

