import pandas as pd

df = pd.read_csv('../Data/ARDS_non-NMBA_yh.csv')
df = df.sort('subject_id')

print df.head(n=5)

df.to_csv('../Data/ARDS_non-NMBA_sorted.csv',sep=',')

# print df.head(n=100)
#
# prev_id = 0
# count_idx = 0
# for idx, row in df.iterrows():
#     current_id = row['subject_id']
#     if prev_id != current_id:
#         count_idx += 1
#         print count_idx, current_id
#     prev_id = current_id





