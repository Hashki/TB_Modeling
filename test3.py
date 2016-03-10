import random
import time
import sys
import pandas as pd
from scipy.sparse import *
from scipy import *

import sqlite3 as lite
con = lite.connect('/Users/halehashki/Haleh/TB/limcat-master/database/limcat-zero-index.sqlite')
cur1 = con.cursor()
cur2 = con.cursor()
cur3 = con.cursor()
# >>> cur.execute('SELECT SQLITE_VERSION()')
# <sqlite3.Cursor object at 0x107d54c00>
# >>> data=cur.fetchone()
# >>> print data

# cursor.execute('''SELECT name, email, phone FROM users''')
# for row in cursor:
  
#     print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))

t = time.time()

from_to_state_dict={}
TP_dict=[[0 for x in range(200)] for x in range(200)]

cur1.execute('select from_state_id from transition_probabilities group by from_state_id')

for row in cur1:
    val=row[0]
    #print "from state" , val
    temp=[];
    cur2.execute('select to_state_id from transition_probabilities where from_state_id =' + str(val))
    for row2 in cur2:
        #print "to state" , row2[0]
        temp.append(row2[0])
        #print val, temp    
        
        stratdict={}
        cur3.execute('SELECT DISTINCT stratum_id, base from transition_probabilities_by_stratum where from_state_id =' +str(val) + ' and to_state_id= ' + str(row2[0]) )
        for row3 in cur3:
            #print row3, row3[0],row3[1]
            stratdict[row3[0]]=row3[1]

            
        TP_dict[val][row2[0]] = stratdict  
    from_to_state_dict[val]=temp


## 2d arraye to sparse dictionary format
#scipy.sparse.dok_matrix
M=dok_matrix(TP_dict)
print "size: ", sys.getsizeof(M)
t = time.time()
A=M[10,40][22016]
print  "time to get from dictionary: ", time.time() - t, A





