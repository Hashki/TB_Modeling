#!/usr/bin/env python
import random
import time
import sys

class person():
    def __init__(self):
        self.state = 0
        self.age   = 1
        self.sex   = 0
        self.race  = 0
        self.birthplace = 1
        self.hiv   = 0



def randstate(prob):
    p = [pi[1] for pi in prob]
    s = [pi[0] for pi in prob]
    print p,s
    sum = 0
    for pi,si in zip(p,s):
        sum += pi
        r = random.uniform(0.0,1.0)
        if r < sum:
            return si
    return p[-1]   
    



prob1 = [[0,0.5],[1,0.2],[2,0.3]]
prob2=[[1,0.9],[3,0.1]] 

print randstate(prob1)


a = [person() for i in range(5)]
print a[1].state

 # a1 = [ai.state for ai in a]
 #    b = set(a1)


#  elements = ['one', 'two', 'three'] 
# >>> weights = [0.2, 0.3, 0.5]
# >>> from numpy.random import choice
# >>> print choice(elements, p=weights)

# [ (i,mylist.count(i)) for i in set(mylist) ]




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
TP_dict={}

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

            
        TP_dict[val,row2[0]] = stratdict  
    from_to_state_dict[val]=temp


# print "dictionary making time: ",   time.time() - t
# print "size of : ", sys.getsizeof(TP_dict)

# print TP_dict[10,40]
# print "----------------------------------"


# t = time.time()
# A=TP_dict[10,40][22016]
# print  "time to get from dictionary: ", time.time() - t, A



# t = time.time()
# cur3.execute('SELECT DISTINCT  base from transition_probabilities_by_stratum where from_state_id =' + str(10) + ' and to_state_id = ' + str(40) + ' and stratum_id = ' + str(22016))
# for row3 in cur3:
#     B=row3[0]
# print "time to get from database: ", time.time() - t, B







#print from_to_state_dict   

# cur.execute('select to_state_id from transition_probabilities where from_state_id =5')
# print cur.fetchone()
# for row in cur:
#     print row[0]

# http://zetcode.com/db/sqlitepythontutorial/

# http://pythoncentral.io/introduction-to-sqlite-in-python/


# python multidimentional array

#Matrix = [[[0 for x in range(5)] for x in range(5)] for x in range(5)]

# Matrix = [[[0 for x in range(5)] for x in range(5)] for x in range(5)]
# >>> Matrix[1][1][1]=1
# >>> import pandas as pd
# >>> df=pd.DataFrame(Matrix)
# >>> df



# df=pd.DataFrame(H)
# sdf = df.to_sparse()
# sdf=df.to_sparse(fill_value=0)
# df.fillna(0).to_sparse(fill_value=0)
# sparse_matrix = scipy.sparse.csr_matrix(Matrix)
# sparse_matrix = scipy.sparse.csr_matrix(df)


# term_dict={}
# term_dict[0][0][0]=1
# term_dict[1][0][0]=1
# term_dict[1][1][0]=1
# term_dict[2][2][2]=1




# from scipy.sparse import csr_matrix
# def _dict_to_csr(term_dict):
#     term_dict_v = list(term_dict.itervalues())
#     term_dict_k = list(term_dict.iterkeys())
#     shape = list(repeat(np.asarray(term_dict_k).max() + 1,2))
#     csr = csr_matrix((term_dict_v, zip(*term_dict_k)), shape = shape)
#     return csr