from datetime import datetime
obj1 = '10/23/08  00:00:00'
date_obj1 = obj1.split(" ")[0]

obj2 = '10/23/08  00:00:00'
date_obj2 = obj2.split(" ")[0]

date_object = datetime.strptime(date_obj1, '%m/%d/%y')
date_object2 = datetime.strptime(date_obj2, '%m/%d/%y')

# NMBA_list = ['rocuronium','cisatracurium','succinylcholine','atracurium','mivacurium','pancuronium','vecuronium']
# for elem in NMBA_list:
#     if elem in str.lower('Clonidine'):
#         print 'yes', elem
#         break


delta = date_object2 - date_object
print str(delta).split(" ")[0]