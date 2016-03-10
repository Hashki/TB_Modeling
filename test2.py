import sys
# term_dict={}
# term_dict[0,0,0] = 11
# term_dict[1,0,0] = 21
# term_dict[0,1,1] = 11


# #baraye 3 dimention kar nakard

# from scipy.sparse import csr_matrix
# def _dict_to_csr(term_dict):
#     term_dict_v = list(term_dict.itervalues())
#     term_dict_k = list(term_dict.iterkeys())
#     shape = list(np.repeat(np.asarray(term_dict_k).max() + 1,2))  #2,3 to be 3 dimention
#     csr = csr_matrix((term_dict_v, zip(*term_dict_k)), shape = shape)
#     return csr

# print csr   





Matrix = [[[0 for x in range(5)] for x in range(5)] for x in range(5)]
Matrix[1][1][1]=1
Matrix[2][2][2]=1
Matrix[3][3][3]=1
Matrix[4][4][4]=1
Matrix[0][0][0]=1
print sys.getsizeof(Matrix)



term_dict={}
term_dict[1,1,1] = 1
term_dict[2,2,2] = 1
term_dict[3,3,3] = 1
term_dict[4,4,4] = 1
term_dict[5,5,5] = 1
print sys.getsizeof(term_dict)





# Sdict={}  ### for stratum ['1':.1,'2':.2,'3':.3]
# FTdic={}
# FTdic['175,176']=Sdict

Sdict['1']=.1
Sdict['2']=.2
FTdic={}
FTdic[1,2]=Sdict
FTdic[2,3]=Sdict
print FTdic[1,2]
{'1': 0.1, '2': 0.2}
print FTdic[1,2]['1']
0.1