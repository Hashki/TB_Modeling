#!/usr/bin/env python
import numpy as np
import sqlite3 as lite
import time



class person():
    def __init__(self):
        self.sex   = ''
        self.race  = ''
        self.age_group  = ''
        self.citizen=''
        self.years_in_us=''
        self.birthplace=''
        self.state=[]
        self.Stratum_id=0
        self.age=0
        self.cycle=0
        self.MonthSinceTBInfection=0
        self.intervention_id=0




### return the index and weight for each index of the base_init_lines
### this index values are used to assign the race, sex, ... for initial people
#### New means its been called for newcomers and in then the year is the year that new comers are coming
def Population_Sample(PopulationNumber,New,year):

	global con
	cur1 = con.cursor()
	cur2=con.cursor()


	


	if New :  ### it means new commers and New is True
		print "true"
		column='weight_new_people' + str(year)
		cur1.execute('select `index`, ' + column + ' from base_init_lines')
		cur2.execute('select sum(' + column + ') from base_init_lines')
		total=cur2.fetchone()   ## sum of all weights 
		total=total[0]
	else:
		cur1.execute('select `index`, weight  from base_init_lines')
		cur2.execute('select sum(weight)  from base_init_lines')  
		total=cur2.fetchone()   ## sum of all weights 
		total=total[0]



	
	elements = [] ### [0] * 11794  #initializing doesnt change the speed
	weights = []

	for row in cur1:
		
	   	elements.append(row[0])
	   	
	   	if row[1] != None:  ### There is no weight for some records
	   		weights.append(row[1] / float(total))    ## to get the percentage of weight for each index 
		else:
			weights.append(0)

	A=np.random.choice(elements, PopulationNumber, p=weights)
	### A contains the index of the base_init_line table that we have to choose people from based on the weight and population size
	return   A




def Initial_Person(Pop_Sample):
	global con
	global P

	cur1 = con.cursor()
	cur2 = con.cursor()

	counter=0
	for pi in P:
		cur1.execute('select sex,race,age_group,citizen,years_in_us,birthplace from base_init_lines  where `index`= ' + str(Pop_Sample[counter]))
		row=cur1.fetchone() 

		pi.sex=row[0]
		pi.race=row[1]
		pi.age_group=row[2]
		pi.citizen=row[3]
		pi.years_in_us=[4]
		pi.birthplace=[5]


		#### Age is low value in age range
		B=row[2].split(' ')
		a=int(B[1][0:2])
		pi.age=a *12  ### convering the year to month as age


		##3 I made thi stratum based on number 1 in stratum type table. 
		## but there are other cobminations too, how people stratify when initialized
		Strstrata=str(row[4]) + ' ' + str(row[5]) + ' ' + str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]) 
		
		
		
		cur2.execute("select id from strata where name = '" + str(Strstrata) + "'")
		row2=cur2.fetchone() 
		# if row2 is None:
		# 	print "khali"
		# else:
		pi.Stratum_id = row2[0]
		#print row2[0]
		
		counter=counter+1
		
	
def Make_TP_Dict():
	global con
	cur1 = con.cursor()
	cur2 = con.cursor()
	cur3 = con.cursor()
	
	
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
	        cur3.execute('SELECT DISTINCT stratum_name, base from transition_probabilities_by_stratum where from_state_id =' +str(val) + ' and to_state_id= ' + str(row2[0]) )
	        for row3 in cur3:
	        	#print row3, str(row3[0])
	        	stratdict[str(row3[0])]=row3[1]

	            
	        TP_dict[val,row2[0]] = stratdict  
	    from_to_state_dict[val]=temp

	return (TP_dict,from_to_state_dict)
	# print "dictionary making time: ",   time.time() - t
	# print "size of : ", sys.getsizeof(TP_dict)


def make_age_group_hash():
	agedict={}

	for i in range(15,80,5):
		val =i+4
		agedict[int(i*12)]="Age " + str(i) + "-" + str(val)

	return agedict	
	### how to find if the age is in the key list to get age group value
	 ##if 15 in agedict.keys():	
	

def increase_val_by_cycleduration(pi, cycle_duration):
	### age, person.cycle, yreas-in-us and monthsSince Tb add up for each cycle
	global Age_Group_Dict
	pi.age=pi.age + cycle_duration
	pi.cycle= pi.cycle+1
	pi.MonthSinceTBInfection= pi.MonthSinceTBInfection + cycle_duration
	#### ?????? YearsinUs is not an value its a string haveing more or less or... if we decided to have it it needs to be pars to get the vaue
	####pi.years_in_us = pi.years_in_us + (cycle_duration/12.0)

	
	if pi.age in Age_Group_Dict.keys():
		pi.age_group =  Age_Group_Dict[pi.age]

	
	

def NewComers():
	f = open("NewComersPerYear.txt",'rU')
	NCdict={}
	### go line by line
	for fi in f:
		fi.strip() # remove the end-of-line
  		t=fi.split('=')
  		NCdict[int(t[0])] =float(t[1].strip())
  	print NCdict	
  	return NCdict



def Interaction_states():
	global con
	cur1 = con.cursor()
	Interaction_states_dict={}
	cur1.execute('select  distinct from_state_id , name from interactions inner join states where  interactions.from_state_id = states.id' )
	for row1 in cur1:
	    Interaction_states_dict[int(row1[0])]=str(row1[1].strip())


	return Interaction_states_dict







if __name__ == "__main__": 
	con = lite.connect('/Users/halehashki/Haleh/TB/limcat-master/database/limcat-zero-index.sqlite')

	PopulationNumber=500
	cycle_duration=1 ### means 1 month duration or 2 or ...
	cycle=62	

	Age_Group_Dict=make_age_group_hash()
	print Age_Group_Dict
	#Make_TP_Dict()
	####TP_dict,from_to_state_dict = Make_TP_Dict()
	#print from_to_state_dict
	#print TP_dict.keys()
	#print from_to_state_dict[5]
	#print from_to_state_dict[10]




	P = [person() for i in range(PopulationNumber)]
	
	# #### for new commers by year
	# NC=NewComers()
	# year=2002   #### this need to be get value in program in cycle loop
	# #print NC[year]
	# Pop_Sample=Population_Sample(NC[year],True,year)

	
	# ### for initial people the program start with
	Pop_Sample=Population_Sample(PopulationNumber,False,0)	
	Initial_Person(Pop_Sample)
	

	##print Interaction_states()
	
	for ci in range(cycle):
		print ci , "------------------------------------------------------------"
		for pi in P:
			increase_val_by_cycleduration(pi, 1)	
			print pi.age, pi.age_group 



			#### add cycle, age,Months_since_TB_Infection, [yearsinus]   values by cycle duration
			### Alex code; Inputs.People[i].Age = Inputs.People[i].Age + (1.0 / 12.0)
			### check the current state to see which path should go, intervention, interaction, trasmission or other









	con.close()
